"""
Run this once to regenerate ward1_heatmap.html colored by Registered Dems.
Place this script next to ward1_heatmap.html and run: python remap_heatmap.py
"""

import re

reg_dems = {
    20: 870, 22: 4038, 23: 2978, 24: 2756, 25: 4068,
    35: 3479, 36: 3962, 37: 3336, 38: 2718, 39: 3911,
    40: 3322, 41: 3337, 42: 1713, 43: 1751, 137: 1110,
}

with open("ward1_heatmap.html", "r") as f:
    html = f.read()

# ── 1. Update tooltip label ────────────────────────────────────────────────
# Old label in each tooltip: "🎯 Untapped Voters: <b>NNN</b>"
# New label:                  "📋 Registered Dems: <b>NNN</b>"
# We'll swap the primary stat shown to Reg Dems and demote untapped to secondary.

# Pattern used in each tooltip block:
# 🎯 Untapped Voters: <b>NNN</b><br>
# 📊 2024 Turnout: XX.X%<br>
# 📋 Registered Dems: N,NNN

def replace_tooltip(m):
    block = m.group(0)
    # Extract values
    untapped = re.search(r'Untapped Voters: <b>([\d,]+)</b>', block).group(1)
    turnout  = re.search(r'2024 Turnout: <b?>([\d.]+%)</?b?>', block)
    turnout  = turnout.group(1) if turnout else re.search(r'Turnout: ([\d.]+%)', block).group(1)
    reg      = re.search(r'Registered Dems: ([\d,]+)', block).group(1)

    new_block = block
    # Replace the three stat lines with Reg Dems first
    new_block = re.sub(
        r'🎯 Untapped Voters: <b>[\d,]+</b><br>\s*'
        r'📊 2024 Turnout: [\d.]+%<br>\s*'
        r'📋 Registered Dems: [\d,]+',
        f'📋 Registered Dems: <b>{reg}</b><br>\n    📊 2024 Turnout: {turnout}<br>\n    🎯 Untapped Voters: {untapped}',
        new_block
    )
    return new_block

html = re.sub(
    r'🎯 Untapped Voters.*?Registered Dems: [\d,]+',
    replace_tooltip,
    html,
    flags=re.DOTALL
)

# ── 2. Rebuild the color scale domain/range around Registered Dems ─────────
min_rd = min(reg_dems.values())   # 870
max_rd = max(reg_dems.values())   # 4068

# Build a 500-step sequential red palette matching the original style
import colorsys

def hex_color(t):
    """t in [0,1]: 0 = lightest (#fff5f0), 1 = darkest (#67000d)"""
    # Interpolate in RGB space between the two endpoints
    light = (1.0, 245/255, 240/255)
    dark  = (103/255, 0, 13/255)
    r = light[0] + t * (dark[0] - light[0])
    g = light[1] + t * (dark[1] - light[1])
    b = light[2] + t * (dark[2] - light[2])
    return '#{:02x}{:02x}{:02x}ff'.format(int(r*255), int(g*255), int(b*255))

N = 500
domain_vals = [min_rd + i * (max_rd - min_rd) / N for i in range(1, N+1)]
range_vals  = [hex_color(i / N) for i in range(N+1)]

domain_str = ', '.join(f'{v:.1f}' for v in domain_vals)
range_str  = ', '.join(f"'{c}'" for c in range_vals)

# Replace the existing .domain([...]) inside color_map
html = re.sub(
    r'\.domain\(\[671\.0,.*?3080\.0\]\)',
    f'.domain([{domain_str}])',
    html, flags=re.DOTALL
)

# Replace the existing .range([...]) inside color_map
html = re.sub(
    r"\.range\(\['#fff5f0ff'.*?'#67000dff'\]\)",
    f'.range([{range_str}])',
    html, flags=re.DOTALL
)

# Replace x linear domain
html = re.sub(
    r'\.domain\(\[671\.0, 3080\.0\]\)',
    f'.domain([{min_rd}, {max_rd}])',
    html
)

# Replace tickValues
html = re.sub(
    r'\.tickValues\(\[671\.0, 1474\.0, 2277\.0, 3080\.0\]\)',
    f'.tickValues([{min_rd}, {round(min_rd + (max_rd-min_rd)/3)}, {round(min_rd + 2*(max_rd-min_rd)/3)}, {max_rd}])',
    html
)

# Replace legend caption text
html = html.replace(
    "Untapped Registered Democrats (didn\\u0027t vote in 2024 primary)",
    "Total Registered Democrats by Precinct"
)

# ── 3. Update fillColor for each precinct to match new scale ──────────────
# The fillColors are hardcoded hex values. Remap them based on reg_dems rank.
precinct_order_by_untapped = [39, 36, 22, 41, 37, 25, 38, 35, 23, 40, 42, 24, 43, 137, 20]

# Map precinct → color based on reg_dems value
def precinct_color(p):
    t = (reg_dems[p] - min_rd) / (max_rd - min_rd)
    return hex_color(t)

# The HTML has one geo_json styler per precinct with a hardcoded fillColor.
# Precincts appear in a known order in the file. We'll patch each styler block.
precinct_fill_map = {p: precinct_color(p) for p in reg_dems}

# Each styler looks like: "fillColor": "#xxxxxxff"
# We patch them sequentially in precinct order of appearance in the file.
# Order of precinct appearance in the original HTML (from tooltips):
appearance_order = [137, 43, 40, 41, 42, 38, 39, 36, 37, 20, 35, 23, 25, 24, 22]

fill_pattern = re.compile(r'("fillColor": ")#[0-9a-fA-F]{6,8}(ff")')
matches = list(fill_pattern.finditer(html))

if len(matches) == len(appearance_order):
    offset = 0
    for i, p in enumerate(appearance_order):
        m = matches[i]
        new_color = precinct_fill_map[p]
        new_str = m.group(1) + new_color + '"'
        start = m.start() + offset
        end   = m.end()   + offset
        html  = html[:start] + new_str + html[end:]
        offset += len(new_str) - (m.end() - m.start())
    print(f"Patched {len(matches)} fillColor values.")
else:
    print(f"Warning: found {len(matches)} fillColor matches, expected {len(appearance_order)}. Skipping fill patch.")

with open("ward1_heatmap.html", "w") as f:
    f.write(html)

print("Done — ward1_heatmap.html updated to show Registered Dems.")
