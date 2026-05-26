import requests
import pandas as pd

# --- Config ---
BASE_URL = "https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/MPD/MapServer/{layer}/query"
OUTPUT_FILE = "ward1_crime.csv"
RED_THRESHOLD = 6.0

YEAR_LAYERS = {2020: 2, 2021: 3, 2022: 4, 2023: 5, 2024: 6, 2025: 7, 2026: 41}

NEIGHBORHOOD = {
    20: 'LeDroit Park', 22: 'U Street', 23: 'Columbia Heights',
    24: 'Adams Morgan', 25: 'Adams Morgan', 35: 'Adams Morgan',
    36: 'Columbia Heights', 37: 'Pleasant Plains', 38: 'Park View',
    39: 'Mt Pleasant/Col Hts', 40: 'Mount Pleasant', 41: 'Columbia Heights',
    42: 'Columbia Heights', 43: 'Park View', 137: 'U Street'
}

WARD1_PRECINCTS = set(NEIGHBORHOOD.keys())

OFFENSE_WEIGHTS = {
    'HOMICIDE': 2,
    'ROBBERY': 1,
    'SEX ABUSE': 1,
    'ASSAULT W/DANGEROUS WEAPON': 1,
    'BURGLARY': 1,
    'THEFT F/AUTO': 1,
    'MOTOR VEHICLE THEFT': 1,
    'THEFT/OTHER': 1,
    'ARSON': 1,
}

def fetch_layer(year, layer_id):
    records = []
    offset = 0
    page_size = 2000
    url = BASE_URL.format(layer=layer_id)
    while True:
        params = {
            'where': "WARD='1'",
            'outFields': 'OFFENSE,VOTING_PRECINCT',
            'returnGeometry': 'false',
            'resultRecordCount': page_size,
            'resultOffset': offset,
            'f': 'json'
        }
        r = requests.get(url, params=params)
        data = r.json()
        if 'error' in data:
            print(f"  Error on {year}: {data['error']}")
            break
        features = data.get('features', [])
        if not features:
            break
        for f in features:
            rec = f['attributes']
            rec['Year'] = year
            records.append(rec)
        if len(features) < page_size:
            break
        offset += page_size
    return records

all_records = []
for year, layer_id in YEAR_LAYERS.items():
    recs = fetch_layer(year, layer_id)
    print(f"  {year} (layer {layer_id}): {len(recs)} records")
    all_records.extend(recs)

print(f"Total records: {len(all_records)}\n")
df = pd.DataFrame(all_records)

# --- Parse precinct ---
df['Precinct'] = df['VOTING_PRECINCT'].str.extract(r'(\d+)').astype(float)
df = df[df['Precinct'].isin(WARD1_PRECINCTS)].copy()
df['Precinct'] = df['Precinct'].astype(int)
print(f"Ward 1 precinct records: {len(df)}")
print(f"Offense types: {sorted(df['OFFENSE'].unique())}\n")

# --- Weight and aggregate ---
df['Weight'] = df['OFFENSE'].map(OFFENSE_WEIGHTS).fillna(1)

by_precinct = df.groupby('Precinct').agg(
    Total_Incidents=('OFFENSE', 'count'),
    Weighted_Score=('Weight', 'sum')
).reset_index()

for p in WARD1_PRECINCTS:
    if p not in by_precinct['Precinct'].values:
        by_precinct = pd.concat([
            by_precinct,
            pd.DataFrame([{'Precinct': p, 'Total_Incidents': 0, 'Weighted_Score': 0}])
        ], ignore_index=True)

by_precinct['Neighborhood'] = by_precinct['Precinct'].map(NEIGHBORHOOD)

# Normalize to 0-10
min_s, max_s = by_precinct['Weighted_Score'].min(), by_precinct['Weighted_Score'].max()
by_precinct['Crime_Score'] = ((by_precinct['Weighted_Score'] - min_s) / (max_s - min_s) * 10).round(1)
by_precinct['Crime_Dot'] = by_precinct['Crime_Score'].apply(lambda x: '🔴' if x >= RED_THRESHOLD else '🟡')

by_precinct = by_precinct.sort_values('Crime_Score', ascending=False)

by_precinct.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {OUTPUT_FILE}\n")
print(by_precinct[['Precinct','Neighborhood','Total_Incidents','Weighted_Score','Crime_Score','Crime_Dot']].to_string(index=False))
