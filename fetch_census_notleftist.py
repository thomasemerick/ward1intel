import requests
import pandas as pd
import json
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

print("Pulling Asian, Black, postgrad...")
df = fetch_vars([
    'B03002_012E',  # Asian alone non-Hispanic
    'B03002_004E',  # Black alone non-Hispanic
    'B03002_001E',  # Total race denominator
    'B15003_023E',  # Master's
    'B15003_024E',  # Professional
    'B15003_025E',  # Doctorate
    'B01003_001E',  # Total pop
])

df['Asian_Pop']     = df['B03002_012E']
df['Black_Pop']     = df['B03002_004E']
df['Race_Total']    = df['B03002_001E']
df['Total_Pop']     = df['B01003_001E']
df['Postgrad_Pop']  = df['B15003_023E'] + df['B15003_024E'] + df['B15003_025E']

df['Asian_Pct']     = (df['Asian_Pop'] / df['Total_Pop'] * 100).round(1)
df['Black_Pct']     = (df['Black_Pop'] / df['Total_Pop'] * 100).round(1)
df['Postgrad_Pct']  = (df['Postgrad_Pop'] / df['Total_Pop'] * 100).round(1)

df['tract'] = df['tract'].str.lstrip('0')

out = df[['tract','NAME','Asian_Pop','Asian_Pct','Black_Pop','Black_Pct','Postgrad_Pop','Postgrad_Pct','Total_Pop']].copy()
out.to_csv('census_notleftist.csv', index=False)
print(f"Saved census_notleftist.csv — {len(out)} tracts")
print(out[['tract','Asian_Pct','Black_Pct','Postgrad_Pct']].head(10).to_string(index=False))
