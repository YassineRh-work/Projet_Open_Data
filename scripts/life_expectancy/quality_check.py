#!/usr/bin/env python3
import os
import pandas as pd

# 1) Locate the cleaned CSV in result/life_expectancy
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
csv_path = os.path.join(project_root, "result", "life_expectancy", "life_expectancy_countries_2000_2023.csv")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"❌ Clean file not found at: {csv_path}")

# 2) Load it
df = pd.read_csv(csv_path)

# 3) Define the years to check
years = ["2000", "2005", "2010", "2015", "2020"]

# 4) Compute missing–value counts
missing = df[years].isnull().sum()
total_countries = len(df)
all_defined = (missing == 0).all()

# 5) Print a neat summary to stdout
print("\n=== Life-Expectancy Data Quality Check ===")
print(f"File: {csv_path}")
print(f"Total countries: {total_countries}\n")
print("Year   Missing_Count   All_Defined")
print("----   -------------   -----------")
for yr in years:
    print(f"{yr:4}   {int(missing[yr]):13}   {str(missing[yr]==0):>11}")
print(f"\nAll five years defined for every country?  {all_defined}\n")

# 6) Optionally list any countries missing any of those years
if not all_defined:
    bad = df[df[years].isnull().any(axis=1)]["country"].tolist()
    print("Countries with missing data:")
    for country in bad:
        print(f" - {country}")
