import pandas as pd
import folium
import webbrowser
import json
import requests

# Load your data (replace with your actual CSV path)
df = pd.read_csv('idh_values.csv')


# Filter to a year to visualize (change this to 2000, 2005, 2010, 2015, 2020 etc)
year = '2015'
df_year = df[df['année'] == year].copy()

# Load GeoJSON for countries (online source)
geojson_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
geojson_data = requests.get(geojson_url).json()

# Map country names in your data to GeoJSON country IDs
# Note: Your country names must match those in the GeoJSON file properties 'name'
name_to_id = {feature['properties']['name']: feature['id'] for feature in geojson_data['features']}

# Add GeoJSON ids to your dataframe
df_year['id'] = df_year['pays'].map(name_to_id)

# Drop rows where mapping failed (no matching geojson country)
df_year = df_year.dropna(subset=['id'])

# Convert 'idh calculé' to numeric (in case it's string or contains NaNs)
df_year['idh calculé'] = pd.to_numeric(df_year['idh calculé'], errors='coerce')

# Create a Folium map (centered roughly in the middle of the world)
m = folium.Map(location=[20, 0], zoom_start=2)

# Add Choropleth layer for IDH values
folium.Choropleth(
    geo_data=geojson_data,
    name='IDH Choropleth',
    data=df_year,
    columns=['id', 'idh calculé'],
    key_on='feature.id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name=f'IDH Calculé in {year}',
    nan_fill_color='white'  # countries with no data shown white
).add_to(m)

# Save to an HTML file and open in browser
html_file = f'idh_map_{year}.html'
m.save(html_file)
webbrowser.open(html_file)
