import requests
import geopandas as gpd
import pandas as pd
import folium
import json

precincts_data = pd.DataFrame({
    "Precinct": [20, 22, 23, 24, 25, 35, 36, 37, 38, 39, 40, 41, 42, 43, 137],
    "Neighborhood": [
        "Columbia Heights", "Columbia Heights", "Mount Pleasant",
        "Mount Pleasant", "Columbia Heights", "Petworth", "Petworth",
        "Park View", "Park View", "Columbia Heights", "U Street",
        "Adams Morgan", "Adams Morgan", "U Street", "Columbia Heights"
    ],
    "Registered_Dems": [870, 4038, 2978, 2756, 4068, 3479, 3962, 3336, 2718, 3911, 3322, 3337, 1713, 1751, 1110],
    "Votes_Cast_2024": [199, 1074, 623, 836, 1264, 1021, 882, 638, 633, 1038, 1012, 774, 467, 408, 220],
})
precincts_data["Untapped"] = precincts_data["Registered_Dems"] - precincts_data["Votes_Cast_2024"]
precincts_data["Turnout_pct"] = (precincts_data["Votes_Cast_2024"] / precincts_data["Registered_Dems"] * 100).round(1)

# Pull GeoJSON — use outSR=4326 to get lat/lon directly
url = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Administrative_Other_Boundaries_WebMercator/MapServer/27/query?where=1%3D1&outFields=*&outSR=4326&f=geojson"
response = requests.get(url)
geojson_data = response.json()

gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])
gdf = gdf.set_crs(epsg=4326)
gdf["Precinct"] = gdf["NAME"].str.extract(r"(\d+)").astype(int)

ward1_precincts = [20, 22, 23, 24, 25, 35, 36, 37, 38, 39, 40, 41, 42, 43, 137]
gdf = gdf[gdf["Precinct"].isin(ward1_precincts)].reset_index(drop=True)

print("Bounds:", gdf.total_bounds)

merged = gdf.merge(precincts_data, on="Precinct").reset_index(drop=True)

# Color scale
max_u = merged["Untapped"].max()
min_u = merged["Untapped"].min()

def get_color(val):
    ratio = (val - min_u) / (max_u - min_u)
    r = int(180 + 75 * ratio)
    g = int(50 * (1 - ratio))
    b = int(50 * (1 - ratio))
    return f'#{r:02x}{g:02x}{b:02x}'

m = folium.Map(location=[38.930, -77.032], zoom_start=14, tiles="CartoDB positron")

for _, row in merged.iterrows():
    color = get_color(row["Untapped"])
    popup_html = f"""
    <b>Precinct {row['Precinct']} — {row['Neighborhood']}</b><br>
    Untapped Voters: <b>{row['Untapped']:,}</b><br>
    2024 Turnout: {row['Turnout_pct']}%<br>
    Registered Dems: {row['Registered_Dems']:,}
    """
    folium.GeoJson(
        row["geometry"].__geo_interface__,
        style_function=lambda x, c=color: {
            "fillColor": c,
            "color": "white",
            "weight": 2,
            "fillOpacity": 0.75,
        },
        tooltip=folium.Tooltip(popup_html)
    ).add_to(m)

m.save("ward1_heatmap.html")
print("Saved!")
