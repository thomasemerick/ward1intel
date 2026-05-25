from dotenv import load_dotenv
import os
import requests
import pandas as pd
import geopandas as gpd
import json

# ── Load census data ──────────────────────────────────────
df = pd.read_csv("dc_census_tracts.csv")
df["Years_Since_Moved_In"] = df["Years_Since_Moved_In"].clip(0, 100)

# ── Pull census tract boundaries ──────────────────────────
tract_url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2023/MapServer/8/query?where=STATE%3D%2711%27&outFields=TRACT,GEOID&f=geojson&outSR=4326"
response = requests.get(tract_url)
tracts_gdf = gpd.GeoDataFrame.from_features(response.json()['features'])
tracts_gdf = tracts_gdf.set_crs(epsg=4326)
print(f"Tract boundaries loaded: {len(tracts_gdf)}")
print(tracts_gdf.columns.tolist())

# ── Pull Ward 1 precinct boundaries ──────────────────────
precinct_url = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Administrative_Other_Boundaries_WebMercator/MapServer/27/query?where=1%3D1&outFields=*&outSR=4326&f=geojson"
response2 = requests.get(precinct_url)
precincts_gdf = gpd.GeoDataFrame.from_features(response2.json()['features'])
precincts_gdf = precincts_gdf.set_crs(epsg=4326)
precincts_gdf["Precinct"] = precincts_gdf["NAME"].str.extract(r"(\d+)").astype(int)

ward1_precincts = [20, 22, 23, 24, 25, 35, 36, 37, 38, 39, 40, 41, 42, 43, 137]
precincts_gdf = precincts_gdf[precincts_gdf["Precinct"].isin(ward1_precincts)].reset_index(drop=True)
print(f"Ward 1 precincts: {len(precincts_gdf)}")

# ── Spatial join ──────────────────────────────────────────
joined = gpd.sjoin(precincts_gdf, tracts_gdf, how="left", predicate="intersects")
print(joined[["Precinct", "TRACT"]].head(20))
joined.to_file("ward1_with_tracts.geojson", driver="GeoJSON")
print("Saved ward1_with_tracts.geojson")
