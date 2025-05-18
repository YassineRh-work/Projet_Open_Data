#!/usr/bin/env python3
import os
import pandas as pd

# 1) Emplacement du script et racine du projet
script_dir   = os.path.dirname(os.path.abspath(__file__))            # .../scripts/life_expectancy
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))  # .../Projet_Open_Data

# 2) Dossiers source et sortie
source_dir = os.path.join(project_root, "sources", "life_expectancy", "World_Bank_Open_Data")
out_dir    = os.path.join(project_root, "result", "life_expectancy")
os.makedirs(out_dir, exist_ok=True)

# 3) Chargement du CSV brut
csv_filename = "API_SP.DYN.LE00.IN_DS2_en_csv_v2_85165.csv"
input_path   = os.path.join(source_dir, csv_filename)
if not os.path.exists(input_path):
    raise FileNotFoundError(f"❌ Fichier introuvable : {input_path}")

df = pd.read_csv(input_path, skiprows=4)

# 4) Sélection des colonnes années (2000–2023)
year_cols = [c for c in df.columns if c.isdigit() and 2000 <= int(c) <= 2023]
if not year_cols:
    raise ValueError("❌ Aucune colonne année ≥ 2000 trouvée dans le CSV.")

# 5) Construction du DataFrame wide
df_wide = df[["Country Name"] + year_cols].copy()
df_wide.rename(columns={"Country Name": "country"}, inplace=True)

# Optionnel : supprimer les pays sans données dans cette période
df_wide.dropna(subset=year_cols, how="all", inplace=True)

# 6) Export vers result/life_expectancy
output_file = "life_expectancy_countries_2000_2023.csv"
output_path = os.path.join(out_dir, output_file)
df_wide.to_csv(output_path, index=False, encoding="utf-8-sig")

# 7) Bilan
print("✅ Fichier généré !")
print(f"  • Pays   : {df_wide.shape[0]} lignes")
print(f"  • Années : {len(year_cols)} colonnes ({min(year_cols)}–{max(year_cols)})")
print(f"  • Chemin : {output_path}")
