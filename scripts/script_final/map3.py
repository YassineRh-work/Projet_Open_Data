import pandas as pd
import folium
import requests

# --- Chargement des données principales ---
df = pd.read_csv("fichier_final.csv")
df = df.replace('', pd.NA)

numerics = ['espérance de vie', 'niveau d’éducation', 'pib/hab', 'idh calculé', 'chômage']
for col in numerics:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Chargement et nettoyage du fichier de coordonnées ---
coords_df = pd.read_csv("https://gist.githubusercontent.com/tadast/8827699/raw/61b2107766d6fd51e2bd02d9f78f6be081340efc/countries_codes_and_coordinates.csv")

coords_df.rename(columns={
    "Country": "Country",
    "Latitude (average)": "latitude",
    "Longitude (average)": "longitude"
}, inplace=True)

coords_df['latitude'] = coords_df['latitude'].astype(str).str.strip().str.replace('"', '').astype(float)
coords_df['longitude'] = coords_df['longitude'].astype(str).str.strip().str.replace('"', '').astype(float)

# --- Chargement GeoJSON ---
url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
geojson_data = requests.get(url).json()

# Liste des années à traiter
annees = [2000, 2005, 2010, 2015, 2020]

for année_cible in annees:
    df_année = df[df['année'] == année_cible].copy()
    df_année.rename(columns={"pays": "Country", "idh calculé": "Value"}, inplace=True)
    
    # Fusion coordonnées
    df_année = pd.merge(df_année, coords_df[['Country', 'latitude', 'longitude']], on='Country', how='left')

    # Création carte
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Couche choroplèthe
    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=df_année,
        columns=["Country", "Value"],
        key_on="feature.properties.name",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"IDH calculé ({année_cible})"
    ).add_to(m)

    # Marqueurs avec popup
    for _, row in df_année.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            popup_html = f"""
            <strong>{row['Country']}</strong><br>
            Espérance de vie : {row['espérance de vie']}<br>
            Niveau d’éducation : {row['niveau d’éducation']}<br>
            PIB/hab : {row['pib/hab']}<br>
            IDH calculé : {row['Value']}<br>
            Chômage : {row['chômage']}
            """
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

    folium.LayerControl().add_to(m)

    # Sauvegarde du fichier
    filename = f"carte_idh_avec_marqueurs_{année_cible}.html"
    m.save(filename)
    print(f"Carte sauvegardée sous '{filename}'")
