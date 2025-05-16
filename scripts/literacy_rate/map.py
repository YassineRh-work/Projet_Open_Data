import pandas as pd
import folium
import webbrowser
import json

# Load your filtered dataset
df = pd.read_csv("indicateur_filtré_annees.csv")

# Choose the year to visualize
year = "2020"

# Load GeoJSON
with open("world-countries.json", "r", encoding="utf-8") as f:
    geo_data = json.load(f)

# Create a folium map centered globally
m = folium.Map(location=[20, 0], zoom_start=2)

# Create choropleth map
folium.Choropleth(
    geo_data=geo_data,
    name="choropleth",
    data=df,
    columns=["Country Code", year],
    key_on="feature.id",  # must match ISO3 code
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"% Population aged 15–64 ({year})",
).add_to(m)

# Add country labels with tooltips
for _, row in df.iterrows():
    folium.Tooltip(f"{row['Country Name']}: {row[year]}%").add_to(
        folium.CircleMarker(
            location=[0, 0],  # No lat/lon but useful if we extend
            radius=0,  # Invisible; just tooltip fallback
        )
    )

# Save and open the map
output_file = f"map_population_{year}.html"
m.save(output_file)
webbrowser.open(output_file)

print(f"🌍 Map saved as {output_file} and opened in your browser.")
