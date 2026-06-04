import requests
import pandas as pd

NEIGHBORHOOD = {
    20: 'LeDroit Park', 22: 'U Street', 23: 'Columbia Heights',
    24: 'Adams Morgan', 25: 'Adams Morgan', 35: 'Adams Morgan',
    36: 'Columbia Heights', 37: 'Pleasant Plains', 38: 'Park View',
    39: 'Mt Pleasant/Col Hts', 40: 'Mount Pleasant', 41: 'Columbia Heights',
    42: 'Columbia Heights', 43: 'Park View', 137: 'U Street'
}
WARD1_PRECINCTS = set(NEIGHBORHOOD.keys())
YEAR_LAYERS = {2020:2, 2021:3, 2022:4, 2023:5, 2024:6, 2025:7, 2026:41}

# Pull homicide counts by precinct from MPD
def fetch_layer(year, layer_id):
    records = []
    offset = 0
    url = f"https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/MPD/MapServer/{layer_id}/query"
    while True:
        params = {
            'where': "WARD='1'",
            'outFields': 'OFFENSE,VOTING_PRECINCT',
            'returnGeometry': 'false',
            'resultRecordCount': 2000,
            'resultOffset': offset,
            'f': 'json'
        }
        r = requests.get(url, params=params)
        data = r.json()
        features = data.get('features', [])
        if not features: break
        for f in features:
            rec = f['attributes']
            rec['Year'] = year
            records.append(rec)
        if len(features) < 2000: break
        offset += 2000
    return records

print("Fetching crime data...")
all_records = []
for year, layer_id in YEAR_LAYERS.items():
    recs = fetch_layer(year, layer_id)
    print(f"  {year}: {len(recs)} records")
    all_records.extend(recs)

crime_raw = pd.DataFrame(all_records)
crime_raw['Precinct'] = crime_raw['VOTING_PRECINCT'].str.extract(r'(\d+)').astype(float)
crime_raw = crime_raw[crime_raw['Precinct'].isin(WARD1_PRECINCTS)].copy()
crime_raw['Precinct'] = crime_raw['Precinct'].astype(int)

# Aggregate by precinct
homicides = crime_raw[crime_raw['OFFENSE']=='HOMICIDE'].groupby('Precinct').size().reset_index(name='Homicides_2020_2026')
total_crime = crime_raw.groupby('Precinct').size().reset_index(name='Total_Crime_Incidents')

# Load all other sources
biz    = pd.read_csv('ward1_business.csv')[['Precinct','Inactive_Licenses','Stress_Rate']]
an     = pd.read_csv('ward1_antinadeau.csv')[['PrecinctNumber','AntiNadeau_Rate','Czapary_2022','Harris_2022','Total_2022']]
an     = an.rename(columns={'PrecinctNumber':'Precinct'})
nl     = pd.read_csv('ward1_notleftist.csv')[['Precinct','Hispanic_Pct','Black_Pct','White_Pct','Asian_Pct','Other_Pct','Postgrad_Pct']]
scored = pd.read_csv('ward1_scored.csv')[['Precinct','Under18_Pct','White_45plus_Pct','MinorityOther_Score','NotLeftist_Score']]
demo   = pd.read_csv('ward1_demographics.csv')[['Precinct','Owner_Pct']]

# Same-sex % needs total HH — approximate from lgbtq file
# SameSex_HH is raw count, we'll show as count not pct since we don't have HH total saved
# Compute derived columns
an['Czapary_Pct'] = (an['Czapary_2022'] / an['Total_2022'] * 100).round(1)
an['Harris_Pct']  = (an['Harris_2022']  / an['Total_2022'] * 100).round(1)
an['AntiNadeau_Pct'] = (an['AntiNadeau_Rate'] * 100).round(1)
nl['AsianOther_Pct'] = (nl['Asian_Pct'] + nl['Other_Pct']).round(1)
nl['MinorityOther_Pct'] = (nl['Hispanic_Pct'] + nl['Asian_Pct'] + nl['Other_Pct']).round(1)

# Build base
base = pd.DataFrame({'Precinct': sorted(WARD1_PRECINCTS)})
base['Neighborhood'] = base['Precinct'].map(NEIGHBORHOOD)

# Merge everything
base = base.merge(total_crime, on='Precinct', how='left')
base = base.merge(homicides, on='Precinct', how='left')
base = base.merge(biz[['Precinct','Inactive_Licenses','Stress_Rate']], on='Precinct', how='left')
base = base.merge(an[['Precinct','AntiNadeau_Pct','Czapary_Pct','Harris_Pct']], on='Precinct', how='left')
base = base.merge(nl[['Precinct','Hispanic_Pct','Black_Pct','White_Pct','Asian_Pct','AsianOther_Pct','MinorityOther_Pct','Postgrad_Pct']], on='Precinct', how='left')
base = base.merge(scored[['Precinct','Under18_Pct','White_45plus_Pct','NotLeftist_Score']], on='Precinct', how='left')
base = base.merge(demo[['Precinct','Owner_Pct']], on='Precinct', how='left')

# Rename for display
base = base.rename(columns={
    'Total_Crime_Incidents': 'Crime_Incidents',
    'Homicides_2020_2026': 'Homicides',
    'Inactive_Licenses': 'Closed_Licenses',
    'Stress_Rate': 'Business_Stress_Rate',
    'AntiNadeau_Pct': 'Anti_Nadeau_Pct',
    'Czapary_Pct': 'Czapary_Vote_Pct',
    'Harris_Pct': 'Harris_Vote_Pct',
    'White_45plus_Pct': 'White_46plus_Pct',
    'AsianOther_Pct': 'Asian_Other_Pct',
    'MinorityOther_Pct': 'Minrty_NoAlign_Pct',
    'Postgrad_Pct': 'Postgrad_Pct',
    'NotLeftist_Score': 'Not_Leftist_Score',
    'Owner_Pct': 'Homeowner_Pct',
})

base['Business_Stress_Rate'] = (base['Business_Stress_Rate'] * 100).round(1)

base.to_csv('ward1_underlying.csv', index=False)
print(f"\nSaved ward1_underlying.csv")
print(base.to_string(index=False))
