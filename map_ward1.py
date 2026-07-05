import requests
import geopandas as gpd
import pandas as pd
import folium
import json
import branca.colormap as cm

precincts_data = pd.DataFrame({
    "Precinct": [20, 22, 23, 24, 25, 35, 36, 37, 38, 39, 40, 41, 42, 43, 137],
    "Neighborhood": [
        "LeDroit Park",        # 20
        "U Street",            # 22
        "Columbia Heights",    # 23
        "Adams Morgan",        # 24
        "Adams Morgan",        # 25
        "Adams Morgan",        # 35
        "Columbia Heights",    # 36
        "Pleasant Plains",     # 37
        "Park View",           # 38
        "Mount Pleasant / Columbia Heights",      # 39
        "Mount Pleasant",      # 40
        "Columbia Heights",    # 41
        "Columbia Heights",    # 42
        "Park View",           # 43
        "U Street",            # 137
    ],
    "Registered_Dems": [870, 4038, 2978, 2756, 4068, 3479, 3962, 3336, 2718, 3911, 3322, 3337, 1713, 1751, 1110],
    "Votes_Cast_2024": [199, 1074, 623, 836, 1264, 1021, 882, 638, 633, 1038, 1012, 774, 467, 408, 220],
})
precincts_data["Untapped"] = precincts_data["Registered_Dems"] - precincts_data["Votes_Cast_2024"]
precincts_data["Turnout_pct"] = (precincts_data["Votes_Cast_2024"] / precincts_data["Registered_Dems"] * 100).round(1)

gdf = gpd.read_file("/Users/blaw/ward1intel/precincts.geojson")
gdf = gdf[gdf["ward"] == "1"].copy()
gdf["Precinct"] = gdf["precinct"].astype(int)
merged = gdf.merge(precincts_data, on="Precinct").reset_index(drop=True)

colormap = cm.LinearColormap(
    colors=['#fff5f0', '#fc8a6b', '#de2d26', '#67000d'],
    vmin=merged["Registered_Dems"].min(),
    vmax=merged["Registered_Dems"].max(),
    caption="Total Registered Democrats"
)

m = folium.Map(location=[38.930, -77.032], zoom_start=14, tiles="CartoDB positron")

for _, row in merged.iterrows():
    color = colormap(row["Registered_Dems"])
    tooltip_html = f"""
    <b style="font-size:14px">Precinct {row['Precinct']} — {row['Neighborhood']}</b><br>
    📋 Registered Dems: {row['Registered_Dems']:,}<br>
    📊 2024 Turnout: {row['Turnout_pct']}%
    """
    folium.GeoJson(
        row["geometry"].__geo_interface__,
        style_function=lambda x, c=color: {
            "fillColor": c,
            "color": "white",
            "weight": 2,
            "fillOpacity": 0.8,
        },
        tooltip=folium.Tooltip(tooltip_html)
    ).add_to(m)

    centroid = row["geometry"].centroid
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(
            html=f'<div style="font-size:11px;font-weight:bold;color:#333;text-shadow:1px 1px 2px white,-1px -1px 2px white">P{row["Precinct"]}<br><span style="font-size:9px;font-weight:normal">{row["Neighborhood"]}</span></div>',
            icon_size=(80, 30),
            icon_anchor=(40, 15)
        )
    ).add_to(m)

colormap.add_to(m)
m.save("ward1_heatmap.html")
print("Saved!")
