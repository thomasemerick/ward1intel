import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# --- Config ---
BASE_URL = "https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/DCRA/FeatureServer/0/query"
OUTPUT_FILE = "ward1_business.csv"
RED_THRESHOLD = 6.0

NEIGHBORHOOD = {
    20: 'LeDroit Park', 22: 'U Street', 23: 'Columbia Heights',
    24: 'Adams Morgan', 25: 'Adams Morgan', 35: 'Adams Morgan',
    36: 'Columbia Heights', 37: 'Pleasant Plains', 38: 'Park View',
    39: 'Mt Pleasant/Col Hts', 40: 'Mount Pleasant', 41: 'Columbia Heights',
    42: 'Columbia Heights', 43: 'Park View', 137: 'U Street'
}
WARD1_PRECINCTS = set(NEIGHBORHOOD.keys())

ACTIVE_STATUSES   = {'Active', 'Ready to Renew'}
INACTIVE_STATUSES = {'Closed', 'Expired', 'Lapsed', 'Abandoned', 'Revoked', 'Cancelled'}

# --- Paginated fetch ---
def fetch_all():
    records = []
    offset = 0
    page_size = 2000
    while True:
        params = {
            'where': "WARD='Ward 1'",
            'outFields': 'LICENSESTATUS,LATITUDE,LONGITUDE',
            'returnGeometry': 'false',
            'resultRecordCount': page_size,
            'resultOffset': offset,
            'f': 'json'
        }
        r = requests.get(BASE_URL, params=params)
        data = r.json()
        if 'error' in data:
            print(f"API error: {data['error']}")
            break
        features = data.get('features', [])
        if not features:
            break
        for f in features:
            records.append(f['attributes'])
        print(f"  Fetched {offset + len(features)} records...")
        if len(features) < page_size:
            break
        offset += page_size
    return pd.DataFrame(records)

print("Fetching DLCP business licenses for Ward 1...")
df = fetch_all()
print(f"Total records: {len(df)}")

# Drop records without coordinates
df = df.dropna(subset=['LATITUDE','LONGITUDE'])
df = df[df['LATITUDE'] != 0]
print(f"Records with coordinates: {len(df)}")

# --- Spatial join to precincts ---
print("Loading precinct boundaries...")
precincts_gdf = gpd.read_file('ward1_with_tracts.geojson')[['Precinct','geometry']].dissolve(by='Precinct').reset_index()

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['LONGITUDE'], df['LATITUDE']), crs='EPSG:4326')
precincts_gdf = precincts_gdf.to_crs('EPSG:4326')

joined = gpd.sjoin(gdf, precincts_gdf, how='left', predicate='within')
joined = joined[joined['Precinct'].isin(WARD1_PRECINCTS)]
print(f"Records matched to Ward 1 precincts: {len(joined)}")

# --- Score by precinct ---
results = []
for p in sorted(WARD1_PRECINCTS):
    grp = joined[joined['Precinct'] == p]
    active   = grp['LICENSESTATUS'].isin(ACTIVE_STATUSES).sum()
    inactive = grp['LICENSESTATUS'].isin(INACTIVE_STATUSES).sum()
    total    = active + inactive
    # Economic stress = closure rate (higher = more stress = higher targeting score)
    stress_rate = inactive / total if total > 0 else 0
    results.append({
        'Precinct': p,
        'Neighborhood': NEIGHBORHOOD[p],
        'Active_Licenses': int(active),
        'Inactive_Licenses': int(inactive),
        'Total_Licenses': int(total),
        'Stress_Rate': round(stress_rate, 4),
    })

out = pd.DataFrame(results)
mn, mx = out['Stress_Rate'].min(), out['Stress_Rate'].max()
out['Business_Score'] = ((out['Stress_Rate'] - mn) / (mx - mn) * 10).round(1)
out['Business_Dot'] = out['Business_Score'].apply(lambda x: '🔴' if x >= RED_THRESHOLD else '🟡')
out = out.sort_values('Business_Score', ascending=False)

out.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved {OUTPUT_FILE}")
print(out[['Precinct','Neighborhood','Active_Licenses','Inactive_Licenses','Stress_Rate','Business_Score','Business_Dot']].to_string(index=False))
