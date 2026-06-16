import re, json, folium

RESULTS_2022 = {
    20:  {"nadeau": 139, "czapary": 87,  "harris": 45,  "wi": 1,  "total": 272,  "neighborhood": "LeDroit Park"},
    22:  {"nadeau": 636, "czapary": 673, "harris": 291, "wi": 6,  "total": 1606, "neighborhood": "U Street"},
    23:  {"nadeau": 506, "czapary": 317, "harris": 224, "wi": 1,  "total": 1048, "neighborhood": "Columbia Heights"},
    24:  {"nadeau": 537, "czapary": 397, "harris": 204, "wi": 0,  "total": 1138, "neighborhood": "Adams Morgan"},
    25:  {"nadeau": 751, "czapary": 642, "harris": 395, "wi": 4,  "total": 1792, "neighborhood": "Adams Morgan"},
    35:  {"nadeau": 752, "czapary": 379, "harris": 303, "wi": 7,  "total": 1441, "neighborhood": "Adams Morgan"},
    36:  {"nadeau": 623, "czapary": 367, "harris": 326, "wi": 2,  "total": 1318, "neighborhood": "Columbia Heights"},
    37:  {"nadeau": 518, "czapary": 356, "harris": 170, "wi": 0,  "total": 1044, "neighborhood": "Pleasant Plains"},
    38:  {"nadeau": 528, "czapary": 234, "harris": 201, "wi": 3,  "total": 966,  "neighborhood": "Park View"},
    39:  {"nadeau": 740, "czapary": 429, "harris": 397, "wi": 3,  "total": 1569, "neighborhood": "Mt Pleasant / Col Hts"},
    40:  {"nadeau": 803, "czapary": 372, "harris": 314, "wi": 7,  "total": 1496, "neighborhood": "Mount Pleasant"},
    41:  {"nadeau": 581, "czapary": 270, "harris": 205, "wi": 3,  "total": 1059, "neighborhood": "Columbia Heights"},
    42:  {"nadeau": 359, "czapary": 205, "harris": 119, "wi": 1,  "total": 684,  "neighborhood": "Columbia Heights"},
    43:  {"nadeau": 339, "czapary": 153, "harris": 108, "wi": 2,  "total": 602,  "neighborhood": "Park View"},
    137: {"nadeau": 164, "czapary": 211, "harris": 49,  "wi": 0,  "total": 424,  "neighborhood": "U Street"},
}

ID_TO_PRECINCT = {
    "403b0a9c": 137,
    "8eb19023": 43,
    "22377acf": 40,
    "c5fc8c9a": 41,
    "3db5cc8a": 42,
    "96e24bcf": 38,
    "348b8f58": 39,
    "d24302d0": 36,
    "37fb5c90": 37,
    "e4c78185": 20,
    "fcaef408": 35,
    "2b4c6322": 23,
    "c5d92abd": 25,
    "780816cc": 24,
    "a654494a": 22,
}

with open("ward1_heatmap.html", "r", encoding="utf-8") as f:
    raw = f.read()

pattern = re.compile(r'geo_json_([a-f0-9]+)_add\((\{.*?"type":\s*"FeatureCollection"\})\);', re.DOTALL)

precinct_geojsons = {}
for m in pattern.finditer(raw):
    prefix = m.group(1)[:8]
    if prefix in ID_TO_PRECINCT:
        p = ID_TO_PRECINCT[prefix]
        precinct_geojsons[p] = json.loads(m.group(2))
        print(f"  ✓ Precinct {p}")

max_total = max(r["total"] for r in RESULTS_2022.values())

max_winner_votes = max(
    max(r["czapary"], r["nadeau"]) for r in RESULTS_2022.values()
)

def get_color(p):
    r = RESULTS_2022[p]
    sorted_votes = sorted([r["czapary"], r["nadeau"], r["harris"]], reverse=True)
    margin = (sorted_votes[0] - sorted_votes[1]) / r["total"]
    t_scaled = min(margin * 4, 1.0)  # amplify so small margins still show contrast
    if r["czapary"] > r["nadeau"]:
        greens = ["#c8e6c9", "#a5d6a7", "#66bb6a", "#388e3c", "#1b5e20"]
        return greens[min(int(t_scaled * len(greens)), len(greens)-1)]
    else:
        yellows = ["#fff9c4", "#fff176", "#f9a825", "#ef6c00", "#e65100"]
        return yellows[min(int(t_scaled * len(yellows)), len(yellows)-1)]

m = folium.Map(location=[38.928, -77.032], zoom_start=14, tiles="CartoDB positron")

for p, geojson in precinct_geojsons.items():
    r = RESULTS_2022[p]
    color = get_color(p)
    nadeau_pct  = round(r["nadeau"]  / r["total"] * 100)
    czapary_pct = round(r["czapary"] / r["total"] * 100)
    harris_pct  = round(r["harris"]  / r["total"] * 100)
    winner    = "Czapary" if r["czapary"] > r["nadeau"] else "Nadeau"
    win_pct   = czapary_pct if winner == "Czapary" else nadeau_pct
    win_votes = r["czapary"] if winner == "Czapary" else r["nadeau"]
    win_color = "#2e7d32" if winner == "Czapary" else "#e65100"

    tooltip_html = f"""<div style="font-family:sans-serif;min-width:200px">
        <b style="font-size:14px">Precinct {p} — {r['neighborhood']}</b><br>
        <span style="color:{win_color};font-weight:bold">✓ {winner} won — {win_pct}% ({win_votes} votes)</span><br>
        <hr style="margin:4px 0">
        🟡 Nadeau: <b>{r['nadeau']}</b> ({nadeau_pct}%)<br>
        🟢 Czapary: <b>{r['czapary']}</b> ({czapary_pct}%)<br>
        ⚪ Harris: <b>{r['harris']}</b> ({harris_pct}%)<br>
        📊 Total DEM votes: <b>{r['total']}</b>
    </div>"""

    folium.GeoJson(
        geojson,
        style_function=lambda feat, c=color: {"fillColor": c, "color": "white", "weight": 2, "fillOpacity": 0.82},
        tooltip=folium.Tooltip(tooltip_html, sticky=True),
    ).add_to(m)

legend_html = """<div style="position:fixed;bottom:30px;left:30px;z-index:9999;background:white;padding:12px 16px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.25);font-family:sans-serif;font-size:12px;line-height:1.8">
    <b style="font-size:13px">2022 Ward 1 Council Primary</b><br>
    <span style="color:#1b5e20;font-size:16px">■</span> Czapary won (darker = bigger margin over Nadeau)<br>
    <span style="color:#e65100;font-size:16px">■</span> Nadeau won (darker = bigger margin over Czapary)
</div>"""
m.get_root().html.add_child(folium.Element(legend_html))
m.save("ward1_2022_heatmap.html")
print("\n✅ Saved ward1_2022_heatmap.html")
