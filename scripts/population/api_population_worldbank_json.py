import requests
import pandas as pd

# API settings
indicator = "SP.POP.TOTL"
start_year = 1960
end_year = 2023
url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"

# Parameters
params = {
    "format": "json",
    "date": f"{start_year}:{end_year}",
    "per_page": 20000  # ensure we get all data in one go
}

# Send request
response = requests.get(url, params=params)

# Check success
if response.status_code == 200:
    data = response.json()
    if len(data) == 2 and data[1] is not None:
        records = [
            {
                "country": item["country"]["value"],
                "year": int(item["date"]),
                "population": item["value"]
            }
            for item in data[1] if item["value"] is not None
        ]
    else:
        print("No data found.")
        records = []
else:
    raise Exception(f"Request failed with status code: {response.status_code}")

# Convert to DataFrame
df = pd.DataFrame(records)

# Pivot to get table format: [country, year] → population
df_pivot = df.pivot(index="country", columns="year", values="population")

# Save to CSV
df_pivot.to_csv("population_by_country_year.csv")

df_pivot.to_csv("population_by_country_year.csv")


# Optional: Print preview
print(df_pivot.head())
