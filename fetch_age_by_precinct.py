"""
Run from ward1intel folder: python3 fetch_age_by_precinct.py
Pulls 18-44 vs 45+ by Census tract, spatially joins to Ward 1 precincts,
outputs ward1_age_precinct.csv
"""
import requests, json, os
import pandas as pd
import geopandas as gpd
from dotenv import load_dotenv

load_dotenv('/Users/blaw/ward1intel/.env')
API_KEY = os.getenv('CENSUS_API_KEY')
BASE = "https://api.census.gov/data/2023/acs/acs5"

WARD1_PRECINCTS = [20,22,23,24,25,35,36,37,38,39,40,41,42,43,137]

# ── Census pull ───────────────────────────────────────────────────────────────
vars_18_44 = [
    "B01001_007E","B01001_008E","B01001_009E","B01001_010E",
    "B01001_011E","B01001_012E","B01001_013E","B01001_014E",
    "B01001_031E","B01001_032E","B01001_033E","B01001_034E",
    "B01001_035E","B01001_036E","B01001_037E","B01001_038E",
]
vars_45_up = [
    "B01001_015E","B01001_016E","B01001_017E","B01001_018E","B01001_019E",
    "B01001_020E","B01001_021E","B01001_022E","B01001_023E","B01001_024E","B01001_025E",
    "B01001_039E","B01001_040E","B01001_041E","B01001_042E","B01001_043E",
    "B01001_044E","B01001_045E","B01001_046E","B01001_047E","B01001_048E","B01001_049E",
]

def fetch(variables):
    params = {
        'get': 'NAME,' + ','.join(variables),
        'for': 'tract:*',
        'in': 'state:11 county:001',
        'key': API_KEY
    }
    r = requests.get(BASE, params=params)
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    for v in variables:
        df[v] = pd.to_numeric(df[v], errors='coerce')
    return df

print("Fetching age data from Census...")
df1 = fetch(["B01001_001E"] + vars_18_44[:14])
df2 = fetch(vars_18_44[14:] + vars_45_up[:18])
df3 = fetch(vars_45_up[18:])

drop = ["NAME","state","county"]
df = df1.merge(df2.drop(columns=drop), on="tract").merge(df3.drop(columns=drop), on="tract")

df["pop_18_44"] = df[vars_18_44].sum(axis=1)
df["pop_45_up"] = df[vars_45_up].sum(axis=1)
df["pop_total"] = df["B01001_001E"]
df["GEOID"]     = "14000US11001" + df["tract"]  # match geojson GEOID format

print(f"Census tracts pulled: {len(df)}")

# ── Load tract geometries ─────────────────────────────────────────────────────
print("Loading tract boundaries...")
tract_url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2023/MapServer/8/query?where=STATE%3D%2711%27&outFields=TRACT,GEOID&f=geojson&outSR=4326"
tracts_gdf = gpd.GeoDataFrame.from_features(requests.get(tract_url).json()['features']).set_crs(epsg=4326)
tracts_gdf["tract"] = tracts_gdf["TRACT"].str.zfill(6)
tracts_gdf = tracts_gdf.merge(df[["tract","pop_total","pop_18_44","pop_45_up"]], on="tract", how="inner")
print(f"Tracts with age data: {len(tracts_gdf)}")

# ── Load precinct boundaries ──────────────────────────────────────────────────
print("Loading precinct boundaries...")
prec_url = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Administrative_Other_Boundaries_WebMercator/MapServer/27/query?where=1%3D1&outFields=*&outSR=4326&f=geojson"
prec_gdf = gpd.GeoDataFrame.from_features(requests.get(prec_url).json()['features']).set_crs(epsg=4326)
prec_gdf["Precinct"] = prec_gdf["NAME"].str.extract(r"(\d+)").astype(int)
prec_gdf = prec_gdf[prec_gdf["Precinct"].isin(WARD1_PRECINCTS)].reset_index(drop=True)

# ── Area-weighted spatial join ────────────────────────────────────────────────
print("Doing area-weighted spatial join...")
tracts_proj = tracts_gdf.to_crs(epsg=32618)
prec_proj   = prec_gdf.to_crs(epsg=32618)

tracts_proj["tract_area"] = tracts_proj.geometry.area
intersected = gpd.overlay(prec_proj[["Precinct","geometry"]], 
                           tracts_proj[["tract","pop_total","pop_18_44","pop_45_up","tract_area","geometry"]], 
                           how="intersection")
intersected["int_area"]   = intersected.geometry.area
intersected["area_weight"] = intersected["int_area"] / intersected["tract_area"]
intersected["w_18_44"]    = intersected["pop_18_44"] * intersected["area_weight"]
intersected["w_45_up"]    = intersected["pop_45_up"] * intersected["area_weight"]
intersected["w_total"]    = intersected["pop_total"] * intersected["area_weight"]

result = intersected.groupby("Precinct").agg(
    pop_total=("w_total","sum"),
    pop_18_44=("w_18_44","sum"),
    pop_45_up=("w_45_up","sum"),
).reset_index()

result["pct_18_44"] = (result["pop_18_44"] / result["pop_total"] * 100).round(1)
result["pct_45_up"] = (result["pop_45_up"] / result["pop_total"] * 100).round(1)
result["pop_total"] = result["pop_total"].round(0).astype(int)

print(f"\n=== Ward 1 Age Splits by Precinct ===")
print(result[["Precinct","pop_total","pct_18_44","pct_45_up"]].to_string(index=False))

result.to_csv("ward1_age_precinct.csv", index=False)
print("\nSaved ward1_age_precinct.csv")
