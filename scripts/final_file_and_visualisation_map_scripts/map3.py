import pandas as pd
import folium
import requests
import unicodedata

def standardize_country_names(df):
    """Standardize country names to match GeoJSON format"""
    country_mapping = {
        "United States": "United States of America",
        "Turkiye": "Turkey",
        "Russian Federation": "Russia",
        "Czech Republic": "Czechia",
        "Korea, Rep.": "South Korea",
        "Iran, Islamic Rep.": "Iran",
        "Egypt, Arab Rep.": "Egypt",
        "Slovak Republic": "Slovakia",
        "Congo, Dem. Rep.": "Democratic Republic of the Congo",
        "Yemen, Rep.": "Yemen",
        "Venezuela, RB": "Venezuela"
    }
    return df.replace({"Country": country_mapping})

# --- Load main data file ---
df = pd.read_csv("fichier_final_idh_norm.csv")
df = df.replace('', pd.NA)

# Convert selected columns to numeric
numerics = ['espérance de vie', 'niveau d’éducation', 'pib/hab', 'idh calculé', 'chômage']
for col in numerics:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Load and clean coordinates file ---
coords_df = pd.read_csv("https://gist.githubusercontent.com/tadast/8827699/raw/61b2107766d6fd51e2bd02d9f78f6be081340efc/countries_codes_and_coordinates.csv")

coords_df.rename(columns={
    "Country": "Country",
    "Latitude (average)": "latitude",
    "Longitude (average)": "longitude"
}, inplace=True)

coords_df['latitude'] = coords_df['latitude'].astype(str).str.strip().str.replace('"', '').astype(float)
coords_df['longitude'] = coords_df['longitude'].astype(str).str.strip().str.replace('"', '').astype(float)

# --- Load GeoJSON ---
url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
geojson_data = requests.get(url).json()

# Extract country names from GeoJSON for validation
geojson_countries = [feature['properties']['name'] for feature in geojson_data['features']]

# List of target years
years = [2000, 2005, 2010, 2015, 2020]

for target_year in years:
    df_year = df[df['année'] == target_year].copy()
    df_year.rename(columns={"pays": "Country", "idh calculé": "Value"}, inplace=True)
    
    # Standardize country names
    df_year = standardize_country_names(df_year)
    
    # Normalize country names (remove extra whitespace and unicode inconsistencies)
    df_year['Country'] = df_year['Country'].astype(str).apply(
        lambda x: unicodedata.normalize("NFKD", x).strip()
    )

    # Merge with coordinates
    df_year = pd.merge(df_year, coords_df[['Country', 'latitude', 'longitude']], on='Country', how='left')

    # Create base map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add choropleth layer
    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=df_year,
        columns=["Country", "Value"],
        key_on="feature.properties.name",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_opacity=0.4,
        legend_name=f"Calculated HDI ({target_year})"
    ).add_to(m)

    # Add popup markers
    for _, row in df_year.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            popup_html = f"""
            <strong>{row['Country']}</strong><br>
            Life Expectancy: {row['espérance de vie']:.2f}<br>
            Education Level: {row['niveau d’éducation']:.2f} %<br>
            GDP per Capita: {row['pib/hab']:.2f}<br>
            Calculated HDI: {row['Value']:.3f}<br>
            Unemployment: {row['chômage']:.2f} %
            """
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

    folium.LayerControl().add_to(m)

    # Save map to file
    filename = f"carte_idh_avec_marqueurs_{target_year}.html"
    m.save(filename)
    print(f"Map saved as '{filename}'")
