import pandas as pd

# Load your CSV file (adjust path if needed)
df = pd.read_csv('fichier_final.csv')

# Select only pays, année and idh calculé columns
idh_values = df[['pays', 'année', 'idh calculé']]

idh_values.to_csv('idh_values.csv', index=False)
