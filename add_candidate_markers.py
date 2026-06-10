"""
Run from ward1intel folder: python3 add_candidate_markers.py
Injects circular headshot markers for all 5 candidates into ward1_heatmap.html
"""
import base64, re

candidates = {
    "Jackie Reyes Yanes": {
        "file": "Jackie-Reyes-Yanes.jpg",
        "address": "707 Kenyon St NW",
        "lat": 38.9317,
        "lng": -77.0284,
    },
    "Aparna Raj": {
        "file": "aparna-raj.png",
        "address": "2656 15th St NW",
        "lat": 38.9282,
        "lng": -77.0371,
    },
    "Miguel Trindade Deramo": {
        "file": "Miguel-Trindade-Deramo.jpeg",
        "address": "2420 14th St NW",
        "lat": 38.9253,
        "lng": -77.0322,
    },
    "Rashida Brown": {
        "file": "rashida-brown.jpeg",
        "address": "430 Irving St NW",
        "lat": 38.9279,
        "lng": -77.0241,
    },
    "Terry Lynch": {
        "file": "terry-lynch.jpg",
        "address": "1737 Kenyon St NW",
        "lat": 38.9308,
        "lng": -77.0340,
    },
}

# Read images as base64
for name, info in candidates.items():
    with open(info["file"], "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    ext = info["file"].split(".")[-1].lower()
    info["mime"] = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
    info["b64"] = b64

# Build JS to inject before </script> at end of file
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
        .addTo(map_f26062cc2f9c7363a8bf91f68bbefdef)
        .bindTooltip('<b>{safe}</b><br><span style="font-size:11px;color:#555">{info["address"]}</span>', {{sticky: true}});
"""

# Inject before the last </script>
with open("ward1_heatmap.html", "r") as f:
    html = f.read()

# Insert just before closing </script> tag at end
insert_point = html.rfind("</script>")
if insert_point == -1:
    print("ERROR: could not find </script> tag")
    exit(1)

html = html[:insert_point] + js + "\n" + html[insert_point:]

with open("ward1_heatmap.html", "w") as f:
    f.write(html)

print(f"Done — injected markers for {len(candidates)} candidates into ward1_heatmap.html")
for name, info in candidates.items():
    print(f"  {name}: {info['lat']}, {info['lng']}")
