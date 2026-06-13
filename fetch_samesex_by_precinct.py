"""
Run from ward1intel folder: python3 fetch_samesex_by_precinct.py
Pulls same-sex households by Census tract, area-weighted to Ward 1 precincts.
B11009: Unmarried-partner households by sex of partners
"""
import requests, os
import pandas as pd
import geopandas as gpd
from dotenv import load_dotenv

load_dotenv('/Users/blaw/ward1intel/.env')
API_KEY = os.getenv('CENSUS_API_KEY')
BASE = "https://api.census.gov/data/2023/acs/acs5"

WARD1_PRECINCTS = [20,22,23,24,25,35,36,37,38,39,40,41,42,43,137]

# B11009 variables:
# B11009_001E — Total households
# B11009_002E — Male householder, unmarried partner: male partner (same-sex male)
# B11009_005E — Female householder, unmarried partner: female partner (same-sex female)
# B11001_001E — Total households (for pct calculation)

print("Fetching same-sex household data from Census...")
params = {
    'get': 'NAME,B11009_001E,B11009_002E,B11009_005E,B11001_001E',
    'for': 'tract:*',
    'in': 'state:11 county:001',
    'key': API_KEY
}
r = requests.get(BASE, params=params)
data = r.json()
df = pd.DataFrame(data[1:], columns=data[0])
for col in ['B11009_001E','B11009_002E','B11009_005E','B11001_001E']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['samesex_hh']   = df['B11009_002E'] + df['B11009_005E']
df['total_hh']     = df['B11001_001E']
df['tract']        = df['tract'].str.zfill(6)

print(f"Census tracts pulled: {len(df)}")

# ── Tract boundaries ──────────────────────────────────────────────────────────
print("Loading tract boundaries...")
tract_url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2023/MapServer/8/query?where=STATE%3D%2711%27&outFields=TRACT,GEOID&f=geojson&outSR=4326"
tracts_gdf = gpd.GeoDataFrame.from_features(requests.get(tract_url).json()['features']).set_crs(epsg=4326)
tracts_gdf["tract"] = tracts_gdf["TRACT"].str.zfill(6)
tracts_gdf = tracts_gdf.merge(df[["tract","samesex_hh","total_hh"]], on="tract", how="inner")

# ── Precinct boundaries ───────────────────────────────────────────────────────
print("Loading precinct boundaries...")
prec_url = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Administrative_Other_Boundaries_WebMercator/MapServer/27/query?where=1%3D1&outFields=*&outSR=4326&f=geojson"
prec_gdf = gpd.GeoDataFrame.from_features(requests.get(prec_url).json()['features']).set_crs(epsg=4326)
prec_gdf["Precinct"] = prec_gdf["NAME"].str.extract(r"(\d+)").astype(int)
prec_gdf = prec_gdf[prec_gdf["Precinct"].isin(WARD1_PRECINCTS)].reset_index(drop=True)

# ── Area-weighted spatial join ────────────────────────────────────────────────
print("Area-weighted spatial join...")
tracts_proj = tracts_gdf.to_crs(epsg=32618)
prec_proj   = prec_gdf.to_crs(epsg=32618)
tracts_proj["tract_area"] = tracts_proj.geometry.area

intersected = gpd.overlay(
    prec_proj[["Precinct","geometry"]],
    tracts_proj[["tract","samesex_hh","total_hh","tract_area","geometry"]],
    how="intersection"
)
intersected["int_area"]    = intersected.geometry.area
intersected["area_weight"] = intersected["int_area"] / intersected["tract_area"]
intersected["w_samesex"]   = intersected["samesex_hh"] * intersected["area_weight"]
intersected["w_total_hh"]  = intersected["total_hh"]   * intersected["area_weight"]

result = intersected.groupby("Precinct").agg(
    total_hh   =("w_total_hh","sum"),
    samesex_hh =("w_samesex","sum"),
).reset_index()

result["total_hh"]   = result["total_hh"].round(0).astype(int)
result["samesex_hh"] = result["samesex_hh"].round(0).astype(int)
result["samesex_pct"]= (result["samesex_hh"] / result["total_hh"] * 100).round(1)

print(f"\n=== Ward 1 Same-Sex Households by Precinct ===")
print(result[["Precinct","total_hh","samesex_hh","samesex_pct"]].to_string(index=False))

result.to_csv("ward1_samesex_precinct.csv", index=False)
print("\nSaved ward1_samesex_precinct.csv")
