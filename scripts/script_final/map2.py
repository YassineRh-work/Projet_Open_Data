import pandas as pd
import folium
import json
import requests

# Charger les données
df = pd.read_csv("fichier_final.csv")
df = df.replace('', pd.NA)

# Convertir les colonnes numériques
numerics = ['espérance de vie', 'niveau d’éducation', 'pib/hab', 'idh calculé', 'chômage']
for col in numerics:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Sélection de l'année et de la variable
année_cible = 2020
variable = "idh calculé"
df_année = df[df['année'] == année_cible].copy()

# IMPORTANT : renommer les colonnes pour être compatibles avec folium
df_année.rename(columns={"pays": "Country", variable: "Value"}, inplace=True)

# Charger le GeoJSON des pays (via un lien public ou un fichier local)
url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
geojson_data = requests.get(url).json()

# Créer la carte centrée
m = folium.Map(location=[20, 0], zoom_start=2)

# Ajouter la couche choroplèthe
folium.Choropleth(
    geo_data=geojson_data,
    name="choropleth",
    data=df_année,
    columns=["Country", "Value"],
    key_on="feature.properties.name",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"{variable} ({année_cible})"
).add_to(m)

# Ajouter les info-bulles
folium.LayerControl().add_to(m)

# Sauvegarder la carte en HTML
m.save(f"carte_folium_idh_{année_cible}.html")
print("Carte sauvegardée sous 'carte_folium_idh_2000.html'")
