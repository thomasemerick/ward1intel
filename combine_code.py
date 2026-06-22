"""
combine_code.py — concatenates every .py file in the project into one
reviewable markdown doc, in pipeline order, with filenames as headers.

Run from project root: python3 combine_code.py
Output: all_code.md
"""

from pathlib import Path

ROOT = Path(".")

# Order matters for readability — fetch -> score -> map -> serve
ORDER = [
    "census_pull.py",
    "census_pull_demos.py",
    "fetch_age_by_precinct.py",
    "fetch_antinadeau.py",
    "fetch_business.py",
    "fetch_census_additions.py",
    "fetch_census_notleftist.py",
    "fetch_crime.py",
    "fetch_samesex_by_precinct.py",
    "fetch_underlying_table.py",
    "precinct_demographics.py",
    "score_precincts.py",
    "dot_scorer.py",
    "map_ward1.py",
    "generate_targeting_map.py",
    "generate_2022_heatmap.py",
    "remap_heatmap.py",
    "add_candidate_markers.py",
    "Home.py",
]

EXCLUDE = {"combine_code.py", "generate_readme.py", "fix_dots.py", "test_url.py"}

all_py = sorted(p.name for p in ROOT.glob("*.py"))
ordered = [f for f in ORDER if f in all_py]
remaining = [f for f in all_py if f not in ORDER and f not in EXCLUDE]
final_list = ordered + sorted(remaining)

lines = ["# Ward 1 Intel — All Code (combined for review)\n"]
lines.append(f"_{len(final_list)} files, in pipeline order: fetch → score → map → serve_\n")
lines.append("## Table of Contents\n")
for f in final_list:
    anchor = f.lower().replace(".", "").replace("_", "-")
    lines.append(f"- [{f}](#{anchor})")
lines.append("")

for f in final_list:
    content = (ROOT / f).read_text(encoding="utf-8", errors="replace")
    lines.append(f"\n---\n")
    lines.append(f"## {f}\n")
    lines.append("```python")
    lines.append(content)
    lines.append("```")

Path("all_code.md").write_text("\n".join(lines), encoding="utf-8")
print(f"✅ Wrote all_code.md ({len(final_list)} files combined)")
