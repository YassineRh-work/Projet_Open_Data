import pandas as pd
import numpy as np

def reshape_indicator(df, indicator_name, col_country='Country Name'):
    years = ['2000', '2005', '2010', '2015', '2020']
    cols_to_keep = [col_country] + [y for y in years if y in df.columns]
    df_filtered = df[cols_to_keep]
    df_melt = df_filtered.melt(id_vars=[col_country], value_vars=years,
                               var_name='année', value_name=indicator_name)
    df_melt.rename(columns={col_country: 'pays'}, inplace=True)
    # Convert year to int
    df_melt['année'] = df_melt['année'].astype(int)
    return df_melt

# Load files (update paths as needed)
df_pib = pd.read_csv('../../result/gdp/gdp_cleaned.csv')
df_education = pd.read_csv('../../result/literacy_rate/literacy_rate_cleaned.csv')
df_esperance = pd.read_csv('../../result/life_expectancy/life_expectancy_countries_2000_2023.csv')
df_chomage = pd.read_csv('../../result/unemployement/unemployement_cleaned.csv')

# Reshape each indicator to long format
df_pib_long = reshape_indicator(df_pib, 'pib/hab')
df_education_long = reshape_indicator(df_education, 'niveau d’éducation')
df_esperance_long = reshape_indicator(df_esperance, 'espérance de vie', col_country='country')
df_chomage_long = reshape_indicator(df_chomage, 'chômage')

# Merge all datasets
df_merge = df_pib_long.merge(df_education_long, on=['pays', 'année'], how='outer') \
                      .merge(df_esperance_long, on=['pays', 'année'], how='outer') \
                      .merge(df_chomage_long, on=['pays', 'année'], how='outer')

# Normalize HDI components (based on UNDP methodology)
def normalize_life_expectancy(v):
    min_val, max_val = 20, 85
    if pd.isna(v) or v < min_val:
        return np.nan
    return (v - min_val) / (max_val - min_val)

def normalize_education(v):
    # Assumes education is a percentage between 0–100%
    min_val, max_val = 0, 100
    if pd.isna(v) or v < min_val:
        return np.nan
    if v > max_val:
        v = max_val
    return v / max_val

def normalize_income(v):
    # Log transformation with UNDP-defined bounds
    min_val, max_val = 100, 75000  # Updated bounds per UNDP
    if pd.isna(v) or v <= min_val:
        return np.nan
    try:
        log_actual = np.log(v)
        log_min = np.log(min_val)
        log_max = np.log(max_val)
        return (log_actual - log_min) / (log_max - log_min)
    except:
        return np.nan

def idh_standard(row):
    try:
        # Get normalized dimensions
        life = normalize_life_expectancy(row['espérance de vie'])
        edu = normalize_education(row['niveau d’éducation'])
        inc = normalize_income(row['pib/hab'])

        # Check if any dimension is missing
        if pd.isna(life) or pd.isna(edu) or pd.isna(inc):
            return np.nan

        # Geometric mean calculation (UNDP method)
        idh = (life * edu * inc) ** (1/3)

        # Round to 3 decimal places as per UNDP standard
        idh = round(idh, 3)

        # Ensure value is between 0 and 1
        return np.clip(idh, 0, 1)
    except Exception as e:
        return np.nan

# Apply HDI calculation
df_merge['idh calculé'] = df_merge.apply(idh_standard, axis=1)

# Reorder columns
df_final = df_merge[['pays', 'année', 'espérance de vie', 'niveau d’éducation', 'pib/hab', 'idh calculé', 'chômage']]

# Export to CSV
df_final.to_csv('fichier_final_idh_norm.csv', index=False)

print("✅ File 'fichier_final_idh_norm.csv'")
