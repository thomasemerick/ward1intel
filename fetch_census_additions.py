import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv('/Users/blaw/ward1intel/.env')
API_KEY = os.getenv('CENSUS_API_KEY')
BASE = "https://api.census.gov/data/2023/acs/acs5"

def fetch_vars(var_list):
    params = {
        'get': 'NAME,' + ','.join(var_list),
        'for': 'tract:*',
        'in': 'state:11 county:001',
        'key': API_KEY
    }
    r = requests.get(BASE, params=params)
    if r.status_code != 200:
        print(f"Error: {r.text[:200]}")
        return None
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    for v in var_list:
        df[v] = pd.to_numeric(df[v], errors='coerce')
    return df

# Male 45+: 012-016, Female 45+: 027-031
print("Pulling White 45+ male...")
df1 = fetch_vars(['B01001A_012E','B01001A_013E','B01001A_014E','B01001A_015E','B01001A_016E'])

print("Pulling White 45+ female + totals...")
df2 = fetch_vars(['B01001A_027E','B01001A_028E','B01001A_029E','B01001A_030E','B01001A_031E',
                  'B01001A_001E','B09001_001E','B01003_001E'])

df = df1.merge(df2, on=['NAME','state','county','tract'])

male_cols   = ['B01001A_012E','B01001A_013E','B01001A_014E','B01001A_015E','B01001A_016E']
female_cols = ['B01001A_027E','B01001A_028E','B01001A_029E','B01001A_030E','B01001A_031E']

df['White_45plus']     = df[male_cols + female_cols].sum(axis=1)
df['Total_Pop']        = df['B01003_001E']
df['White_45plus_Pct'] = (df['White_45plus'] / df['Total_Pop'] * 100).round(1)
df['Under18']          = df['B09001_001E']
df['Under18_Pct']      = (df['Under18'] / df['Total_Pop'] * 100).round(1)

df['tract'] = df['tract'].str.lstrip('0')

out = df[['tract','NAME','White_45plus','White_45plus_Pct','Under18','Under18_Pct','Total_Pop']].copy()
out.to_csv('census_additions.csv', index=False)
print(f"\nSaved census_additions.csv — {len(out)} tracts")
print(out[['tract','White_45plus_Pct','Under18_Pct']].head(10).to_string(index=False))
