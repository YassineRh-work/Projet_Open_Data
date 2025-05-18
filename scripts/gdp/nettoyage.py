import pandas as pd

# Lecture du fichier
df = pd.read_csv(
    r"C:\Users\yassi\Desktop\APP5\Représentation_données\projet1\Projet_Open_Data\sources\gdp\API_NY.GDP.PCAP.KD.ZG_DS2_en_csv_v2_85132.csv",
    skiprows=3,
    sep=',',
    quotechar='"',
    encoding='utf-8'
)

# Toutes les années disponibles pour traitement
all_years = [str(y) for y in range(1995, 2021)]

# Années cibles pour la sortie
selected_years = ["2000", "2005", "2010", "2015", "2020"]
colonnes_finales = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"] + selected_years

# Colonnes à garder pour traitement
colonnes_traitement = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"] + all_years
df = df[[col for col in colonnes_traitement if col in df.columns]]

# Fonction de remplissage conditionnelle
def fill_target_years_with_past_average(row):
    for year in selected_years:
        if pd.isna(row[year]):
            idx = all_years.index(year)
            prev_years = all_years[max(0, idx - 5):idx]
            prev_values = [row[py] for py in prev_years if py in row and not pd.isna(row[py])]
            if prev_values:
                row[year] = sum(prev_values) / len(prev_values)
    return row

# Appliquer à chaque ligne du DataFrame
df = df.apply(fill_target_years_with_past_average, axis=1)

# Extraire les colonnes finales
df_final = df[colonnes_finales]

# Sauvegarder le fichier final
df_final.to_csv("gdp_cleaned.csv", index=False)
print("✅ Fichier final sauvegardé sous 'indicateur_filtré_annees.csv'")
