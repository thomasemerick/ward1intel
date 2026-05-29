import geopandas as gpd
import folium
import json
import pandas as pd

# Tier assignments based on Final_Score ranking
TIERS = {
    39: (1, "#c0392b", "🥇 #1"),
    22: (1, "#c0392b", "🥇 #2"),
    25: (1, "#c0392b", "🥇 #3"),
    36: (2, "#e67e22", "🥈 #4"),
    35: (2, "#e67e22", "🥈 #5"),
    41: (2, "#e67e22", "🥈 #6"),
    37: (2, "#e67e22", "🥈 #7"),
    40: (3, "#f39c12", "🥉 #8"),
    24: (3, "#f39c12", "🥉 #9"),
    38: (3, "#f39c12", "🥉 #10"),
    42: (3, "#f39c12", "🥉 #11"),
    23: (4, "#f7dc6f", "  #12"),
    137:(4, "#f7dc6f", "  #13"),
    43: (4, "#f7dc6f", "  #14"),
    20: (4, "#f7dc6f", "  #15"),
}

NEIGHBORHOOD = {
    20: 'LeDroit Park', 22: 'U Street', 23: 'Columbia Heights',
    24: 'Adams Morgan', 25: 'Adams Morgan', 35: 'Adams Morgan',
    36: 'Columbia Heights', 37: 'Pleasant Plains', 38: 'Park View',
    39: 'Mt Pleasant/Col Hts', 40: 'Mount Pleasant', 41: 'Columbia Heights',
    42: 'Columbia Heights', 43: 'Park View', 137: 'U Street'
}

# Load and dissolve precinct boundaries
gdf = gpd.read_file('ward1_with_tracts.geojson')
precincts = gdf[['Precinct','geometry']].dissolve(by='Precinct').reset_index()
precincts = precincts.to_crs('EPSG:4326')

# Center map on Ward 1
center = [38.9255, -77.033]
m = folium.Map(
    location=center,
    zoom_start=14,
    zoom_control=False,
    scrollWheelZoom=False,
    dragging=False,
    tiles='CartoDB positron'
)

# Draw precincts
for _, row in precincts.iterrows():
    p = int(row.Precinct)
    if p not in TIERS:
        continue
    tier, color, rank = TIERS[p]
    geo = row.geometry.__geo_interface__

    folium.GeoJson(
        geo,
        style_function=lambda x, c=color: {
            'fillColor': c,
            'color': 'white',
            'weight': 2,
            'fillOpacity': 0.85,
        },
        tooltip=folium.Tooltip(f"P{p} — {NEIGHBORHOOD[p]}<br>{rank}"),
    ).add_to(m)

    # Add precinct label at centroid
    centroid = row.geometry.centroid
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(
            html=f'<div style="font-size:11px;font-weight:bold;color:white;text-shadow:1px 1px 2px #000;text-align:center;white-space:nowrap;">P{p}</div>',
            icon_size=(40, 20),
            icon_anchor=(20, 10),
        )
    ).add_to(m)

# Legend
legend_html = """
<div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:white;
     padding:12px 16px;border-radius:8px;box-shadow:2px 2px 6px rgba(0,0,0,0.3);font-family:Arial;font-size:13px;">
  <b>Targeting Tier</b><br>
  <span style="color:#c0392b;">&#9632;</span> Tier 1 — Gold (P39, P22, P25)<br>
  <span style="color:#e67e22;">&#9632;</span> Tier 2 — Silver (P36, P35, P41, P37)<br>
  <span style="color:#f39c12;">&#9632;</span> Tier 3 — Bronze (P40, P24, P38, P42)<br>
  <span style="color:#f7dc6f;">&#9632;</span> Tier 4 — Monitor (P23, P137, P43, P20)
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

m.save('ward1_targeting_map.html')
print("Saved ward1_targeting_map.html")
