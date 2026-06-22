"""
generate_readme.py

Scans the ward1intel project folder and writes a README.md cataloguing
every Python script, CSV, HTML output, and asset, with a one-line
description pulled from each file's docstring/comments/structure.

Run from the project root:
    python generate_readme.py
"""

import os
from pathlib import Path
from datetime import datetime

ROOT = Path(".")

# Manual descriptions — edit these as the project evolves.
# Fill in or override the auto-detected guess below.
DESCRIPTIONS = {
    # Core app
    "Home.py": "Live Streamlit app — Overview, RCV Sim, Issue Survey, Precinct Data tabs.",
    "Home_backup.py": "Old snapshot of Home.py — safe to archive/delete.",
    "Home_backup2.py": "Old snapshot of Home.py — safe to archive/delete.",
    "Home_backup3.py": "Old snapshot of Home.py — safe to archive/delete.",
    "Home_backup_june7.py": "Old snapshot of Home.py — safe to archive/delete.",
    "Home_new.py": "Old snapshot of Home.py — safe to archive/delete.",

    # Data fetch scripts
    "census_pull.py": "Pulls base Census ACS data via API (uses .env API key).",
    "census_pull_demos.py": "Pulls expanded Census demographic breakdowns by tract.",
    "fetch_age_by_precinct.py": "Builds age distribution by precinct, joins to precinct geometry.",
    "fetch_antinadeau.py": "Computes an 'anti-Nadeau' lean score per precinct from 2022 results.",
    "fetch_business.py": "Pulls DC DLCP business license data, maps closures to precincts via point-in-polygon.",
    "fetch_census_additions.py": "Pulls supplemental Census variables not in the base pull.",
    "fetch_census_notleftist.py": "Pulls Census data used for the 'not leftist' precinct score.",
    "fetch_crime.py": "Pulls MPD crime data by precinct.",
    "fetch_samesex_by_precinct.py": "Pulls Census same-sex household data by precinct.",
    "fetch_underlying_table.py": "Pulls MPD homicide counts by precinct for the underlying data table.",

    # Scoring / analysis
    "dot_scorer.py": "Scores precincts (Hispanic %, median age, homeownership) into high/medium/low tiers.",
    "score_precincts.py": "Aggregates census data to precinct level (population-weighted) and merges with geo file.",
    "precinct_demographics.py": "Pulls and joins demographic data to precinct boundaries.",

    # Map generation
    "map_ward1.py": "Builds base Ward 1 precinct map from Census tract geometry.",
    "generate_targeting_map.py": "Builds the campaign targeting map with tier-based coloring from Final_Score.",
    "generate_2022_heatmap.py": "Builds the 2022 Nadeau vs Czapary choropleth (green=Czapary, orange=Nadeau).",
    "remap_heatmap.py": "Utility for re-coloring/re-styling an existing Folium heatmap HTML.",
    "add_candidate_markers.py": "Adds candidate headshot markers (base64-encoded images) to a Folium map.",
    "fix_dots.py": "EMPTY FILE — placeholder, currently unused.",

    # Misc / testing
    "test_url.py": "Quick script for testing an API/URL endpoint.",

    # Config
    "requirements.txt": "Python package dependencies.",
    ".env": "Environment variables / API keys — DO NOT COMMIT TO GIT OR SHARE.",
    "README.md": "This file (auto-generated).",
}

CSV_DESCRIPTIONS = {
    "census_additions.csv": "Supplemental Census variables by tract.",
    "census_notleftist.csv": "Census data backing the 'not leftist' precinct score.",
    "dc_census_tracts.csv": "Raw DC Census tract reference data.",
    "June_21_2022_Primary_Election_Certified_Results.csv": "DCBOE certified results, June 2022 primary (all races, all precincts).",
    "June_4_2024_Primary_Election_Certified_Results.csv": "DCBOE certified results, June 2024 primary (all races, all precincts).",
    "ward1_age_precinct.csv": "Age distribution by Ward 1 precinct.",
    "ward1_antinadeau.csv": "Anti-Nadeau lean score by precinct (derived from 2022 results).",
    "ward1_business.csv": "Business closures since 2015 by precinct.",
    "ward1_crime.csv": "MPD crime stats by precinct.",
    "ward1_demographics.csv": "Core demographic summary by precinct.",
    "ward1_demos_full.csv": "Full/expanded demographic table by precinct.",
    "ward1_lgbtq.csv": "Same-sex household data by precinct.",
    "ward1_notleftist.csv": "Precinct-level 'not leftist' score components.",
    "ward1_race_census.csv": "Race/ethnicity breakdown by precinct.",
    "ward1_samesex_precinct.csv": "Same-sex household percentages by precinct.",
    "ward1_scored.csv": "Final composite precinct scores (targeting tiers).",
    "ward1_underlying.csv": "Master underlying data table — feeds the Precinct Data tab.",
}

HTML_DESCRIPTIONS = {
    "ward1_heatmap.html": "Registered-Dems choropleth with candidate headshot markers — used in Overview tab.",
    "ward1_2022_heatmap.html": "2022 Nadeau vs Czapary results choropleth — used in Overview tab.",
    "ward1_targeting_map.html": "Campaign targeting map (tiered by Final_Score) for outreach planning.",
    "ward1_hotspot_map.html": "Large hotspot/density map (5MB) — likely an early or high-res version.",
}

IMAGE_FILES = {".jpg", ".jpeg", ".png"}


def describe_file(name: str) -> str:
    if name in DESCRIPTIONS:
        return DESCRIPTIONS[name]
    if name in CSV_DESCRIPTIONS:
        return CSV_DESCRIPTIONS[name]
    if name in HTML_DESCRIPTIONS:
        return HTML_DESCRIPTIONS[name]
    ext = Path(name).suffix.lower()
    if ext in IMAGE_FILES:
        return "Candidate headshot image (used as a map marker)."
    return "*(no description on file — add one in generate_readme.py)*"


def human_size(num_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f}{unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f}TB"


def main():
    files = sorted(p for p in ROOT.iterdir() if p.is_file() and p.name != "generate_readme.py")

    py_files   = [f for f in files if f.suffix == ".py"]
    csv_files  = [f for f in files if f.suffix == ".csv"]
    html_files = [f for f in files if f.suffix == ".html"]
    img_files  = [f for f in files if f.suffix.lower() in IMAGE_FILES]
    geo_files  = [f for f in files if f.suffix == ".geojson"]
    other      = [f for f in files if f not in py_files + csv_files + html_files + img_files + geo_files]

    lines = []
    lines.append("# Ward 1 Intel — Project Reference\n")
    lines.append(f"_Auto-generated {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
    lines.append(
        "This README catalogues every file in the project. Descriptions are "
        "hand-written in `generate_readme.py` — rerun that script after adding "
        "new files to keep this current.\n"
    )

    lines.append("## ⚠️ Before you do anything else")
    lines.append(
        "- `.env` contains API keys. Make sure it's in `.gitignore` and never gets "
        "committed or shared.\n"
        "- `Home_backup*.py` and `Home_new.py` are stale snapshots of `Home.py`. "
        "Safe to delete or move to an `/archive` folder once you've confirmed "
        "`Home.py` has everything you need.\n"
        "- `fix_dots.py` is a 0-byte placeholder.\n"
        "- `ward1_hotspot_map.html` is 5MB — confirm it's still needed before "
        "committing to git (GitHub flags files over a few MB).\n"
    )

    def section(title, file_list, desc_lookup_fn):
        out = [f"## {title}\n"]
        out.append("| File | Size | Last Modified | Description |")
        out.append("|---|---|---|---|")
        for f in file_list:
            stat = f.stat()
            size = human_size(stat.st_size)
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
            desc = desc_lookup_fn(f.name)
            out.append(f"| `{f.name}` | {size} | {mtime} | {desc} |")
        out.append("")
        return "\n".join(out)

    lines.append(section("🐍 Python Scripts", py_files, describe_file))
    lines.append(section("📊 Data Files (CSV)", csv_files, describe_file))
    lines.append(section("🗺️ Generated Maps (HTML)", html_files, describe_file))
    lines.append(section("🗺️ Geo Data", geo_files, describe_file))
    lines.append(section("🖼️ Images", img_files, describe_file))
    if other:
        lines.append(section("📁 Other", other, describe_file))

    lines.append("## Suggested pipeline order\n")
    lines.append(
        "1. **Fetch raw data**: `census_pull.py`, `census_pull_demos.py`, "
        "`fetch_*.py` scripts pull from Census/MPD/DLCP APIs into CSVs.\n"
        "2. **Score & aggregate**: `score_precincts.py`, `dot_scorer.py` turn "
        "raw CSVs into precinct-level scores (`ward1_scored.csv`, "
        "`ward1_underlying.csv`).\n"
        "3. **Generate maps**: `map_ward1.py`, `generate_targeting_map.py`, "
        "`generate_2022_heatmap.py` build the Folium HTML files embedded in "
        "Streamlit.\n"
        "4. **Serve**: `Home.py` reads the CSVs and HTML files and renders the "
        "Streamlit app.\n"
    )

    readme_text = "\n".join(lines)
    with open("README.md", "w") as f:
        f.write(readme_text)

    print(f"✅ Wrote README.md ({len(files)} files catalogued)")


if __name__ == "__main__":
    main()
