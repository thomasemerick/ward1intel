"""
Run from ward1intel folder: python3 add_candidate_markers.py
Embeds images as base64 — works on both localhost and Streamlit Cloud.
"""
import base64, re

candidates = {
    "Jackie Reyes Yanes": {
        "file": "Jackie-Reyes-Yanes.jpg",
        "address": "707 Kenyon St NW",
        "lat": 38.9335,
        "lng": -77.0315,
    },
    "Aparna Raj": {
        "file": "aparna-raj.png",
        "address": "2656 15th St NW",
        "lat": 38.9265,
        "lng": -77.0395,
    },
    "Miguel Trindade Deramo": {
        "file": "Miguel-Trindade-Deramo.jpeg",
        "address": "2420 14th St NW",
        "lat": 38.9198,
        "lng": -77.0305,
    },
    "Rashida Brown": {
        "file": "rashida-brown.jpeg",
        "address": "430 Irving St NW",
        "lat": 38.9268,
        "lng": -77.0190,
    },
    "Terry Lynch": {
        "file": "terry-lynch.jpg",
        "address": "1737 Kenyon St NW",
        "lat": 38.9295,
        "lng": -77.0420,
    },
}

# Read images as base64
for name, info in candidates.items():
    with open(info["file"], "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    ext = info["file"].split(".")[-1].lower()
    info["mime"] = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
    info["b64"] = b64

# Read HTML
with open("ward1_heatmap.html", "r") as f:
    html = f.read()

# Find the map variable name
map_var = re.search(r'var (map_[a-f0-9]+) = L\.map\(', html)
if not map_var:
    print("ERROR: could not find Leaflet map variable")
    exit(1)
map_id = map_var.group(1)
print(f"Found map variable: {map_id}")

# Build JS marker block
js = "\n    // ── Candidate markers ──────────────────────────────────────────\n"
for name, info in candidates.items():
    key = name.split()[0].lower()
    safe = name.replace("'", "\\'")
    js += f"""
    var icon_{key} = L.divIcon({{
        className: '',
        html: '<div style="text-align:center;cursor:pointer"><img src="data:{info["mime"]};base64,{info["b64"]}" style="width:54px;height:54px;border-radius:50%;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.45);object-fit:cover;display:block;margin:0 auto;"><div style="background:rgba(255,255,255,0.93);border-radius:4px;padding:2px 6px;font-size:11px;font-weight:600;color:#1a1a1a;margin-top:3px;white-space:nowrap;box-shadow:0 1px 4px rgba(0,0,0,0.18);">{safe}</div></div>',
        iconSize: [110, 78],
        iconAnchor: [55, 27],
        popupAnchor: [0, -30],
    }});
    L.marker([{info["lat"]}, {info["lng"]}], {{icon: icon_{key}}})
        .addTo({map_id})
        .bindTooltip('<b>{safe}</b><br><span style="font-size:11px;color:#555">{info["address"]}</span>', {{sticky: true}});
"""

# Inject just before </body>
if "</body>" not in html:
    print("ERROR: could not find </body> tag")
    exit(1)

html = html.replace("</body>", f"<script>{js}\n</script>\n</body>")

with open("ward1_heatmap.html", "w") as f:
    f.write(html)

print(f"Done — injected markers for {len(candidates)} candidates into ward1_heatmap.html")
for name, info in candidates.items():
    print(f"  {name}: {info['lat']}, {info['lng']}")
