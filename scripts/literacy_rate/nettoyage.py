import pandas as pd

# Lecture du fichier avec les bons paramètres
df = pd.read_csv(
    r"API_SE.TER.CUAT.ST.ZS_DS2_en_csv_v2_93935.csv",
    skiprows=3,              # Ignore les 3 premières lignes non utiles
    sep=',',                 # Séparateur explicite
    quotechar='"',           # Pour gérer les champs entre guillemets
    encoding='utf-8'         # Si erreur, essaie 'utf-8-sig' ou 'ISO-8859-1'
)
colonnes_à_garder = ["Country Name", "Country Code", "Indicator Name", "Indicator Code",
                     "2000", "2005", "2010", "2015", "2020"]

# Vérifie que toutes les colonnes existent
colonnes_existantes = [col for col in colonnes_à_garder if col in df.columns]

# Garde seulement les colonnes sélectionnées
df_épuré = df[colonnes_existantes]

# Sauvegarder le résultat
df_épuré.to_csv("indicateur_filtré_annees.csv", index=False)
print("✅ Fichier final sauvegardé sous 'indicateur_filtré_annees.csv'")