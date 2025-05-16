import requests
import pandas as pd

# 1) Code OData pour "Life expectancy at birth (years)"
indicator_code = "WHOSIS_000001"  # celui qui fonctionne en OData

# 2) Construire URL et paramètres de filtrage
base_url = f"https://ghoapi.azureedge.net/api/{indicator_code}"
params = {
    # On précise le type de dimension et la valeur BTSX
    "$filter": "Dim1Type eq 'SEX' and Dim1 eq 'BTSX'",
    "$format": "json",
    "$top": "50000"
}

# 3) Appel à l'API
resp = requests.get(base_url, params=params)
resp.raise_for_status()
payload = resp.json()

# 4) Extraction des champs utiles
records = []
for item in payload.get("value", []):
    country = item.get("SpatialDimName") or item.get("SpatialDim")
    year    = item.get("TimeDim")
    val     = item.get("NumericValue") if item.get("NumericValue") is not None else item.get("Value")
    if country and year is not None and val is not None:
        records.append({
            "country": country,
            "year": int(year),
            "life_expectancy": float(val)
        })

# 5) DataFrame, tri, export CSV
df = pd.DataFrame(records)
if df.empty:
    print("⚠️ Aucune donnée récupérée. Vérifiez le filter.")
else:
    df = df.sort_values(by=["country", "year"]).reset_index(drop=True)
    output_file = "who_life_expectancy_by_country_year.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ {len(df)} enregistrements sauvés dans «{output_file}»")
