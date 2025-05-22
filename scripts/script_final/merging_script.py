import pandas as pd
import numpy as np

def reshape_indicator(df, indicator_name, col_country='Country Name'):
    years = ['2000', '2005', '2010', '2015', '2020']
    cols_to_keep = [col_country] + [y for y in years if y in df.columns]
    df_filtered = df[cols_to_keep]
    df_melt = df_filtered.melt(id_vars=[col_country], value_vars=years,
                               var_name='année', value_name=indicator_name)
    df_melt.rename(columns={col_country: 'pays'}, inplace=True)
    return df_melt

# Charger fichiers
df_pib = pd.read_csv(r'C:\Users\yassi\Desktop\APP5\Représentation_données\projet1\Projet_Open_Data\result\gdp\gdp_cleaned.csv')
df_education = pd.read_csv(r'C:\Users\yassi\Desktop\APP5\Représentation_données\projet1\Projet_Open_Data\result\literacy_rate\literacy_rate_cleaned.csv')
df_esperance = pd.read_csv(r'C:\Users\yassi\Desktop\APP5\Représentation_données\projet1\Projet_Open_Data\result\life_expectancy\life_expectancy_countries_2000_2023.csv')
df_chomage = pd.read_csv(r'C:\Users\yassi\Desktop\APP5\Représentation_données\projet1\Projet_Open_Data\result\unemployement\unemployement_cleaned.csv')

# Reshape
df_pib_long = reshape_indicator(df_pib, 'pib/hab')
df_education_long = reshape_indicator(df_education, 'niveau d’éducation')
df_esperance_long = reshape_indicator(df_esperance, 'espérance de vie', col_country='country')
df_chomage_long = reshape_indicator(df_chomage, 'chômage')

# Merge
df_merge = df_pib_long.merge(df_education_long, on=['pays', 'année'], how='outer') \
                      .merge(df_esperance_long, on=['pays', 'année'], how='outer') \
                      .merge(df_chomage_long, on=['pays', 'année'], how='outer')

# Calcul IDH sans normalisation (moyenne arithmétique des 3 indicateurs bruts)
def idh_calc_no_norm(row):
    vals = [row['espérance de vie'], row['niveau d’éducation'], row['pib/hab']]
    # Ignorer les lignes avec NaN dans les indicateurs
    if any(pd.isna(v) for v in vals):
        return np.nan
    return sum(vals) / len(vals)

df_merge['idh calculé'] = df_merge.apply(idh_calc_no_norm, axis=1)

# Réorganiser colonnes
df_final = df_merge[['pays', 'année', 'espérance de vie', 'niveau d’éducation', 'pib/hab', 'idh calculé', 'chômage']]

# Export final
df_final.to_csv('fichier_final3.csv', index=False)
