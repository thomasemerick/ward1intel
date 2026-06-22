# Ward 1 Intel — Project Reference

_Auto-generated 2026-06-19 11:38_

This README catalogues every file in the project. Descriptions are hand-written in `generate_readme.py` — rerun that script after adding new files to keep this current.

## ⚠️ Before you do anything else
- `.env` contains API keys. Make sure it's in `.gitignore` and never gets committed or shared.
- `Home_backup*.py` and `Home_new.py` are stale snapshots of `Home.py`. Safe to delete or move to an `/archive` folder once you've confirmed `Home.py` has everything you need.
- `fix_dots.py` is a 0-byte placeholder.
- `ward1_hotspot_map.html` is 5MB — confirm it's still needed before committing to git (GitHub flags files over a few MB).

## 🐍 Python Scripts

| File | Size | Last Modified | Description |
|---|---|---|---|
| `Home.py` | 16KB | 2026-06-16 | Live Streamlit app — Overview, RCV Sim, Issue Survey, Precinct Data tabs. |
| `Home_backup.py` | 68KB | 2026-05-22 | Old snapshot of Home.py — safe to archive/delete. |
| `Home_backup2.py` | 61KB | 2026-05-22 | Old snapshot of Home.py — safe to archive/delete. |
| `Home_backup3.py` | 49KB | 2026-05-24 | Old snapshot of Home.py — safe to archive/delete. |
| `Home_backup_june7.py` | 58KB | 2026-06-08 | Old snapshot of Home.py — safe to archive/delete. |
| `Home_new.py` | 44KB | 2026-05-22 | Old snapshot of Home.py — safe to archive/delete. |
| `add_candidate_markers.py` | 3KB | 2026-06-10 | Adds candidate headshot markers (base64-encoded images) to a Folium map. |
| `census_pull.py` | 1KB | 2026-05-25 | Pulls base Census ACS data via API (uses .env API key). |
| `census_pull_demos.py` | 8KB | 2026-06-09 | Pulls expanded Census demographic breakdowns by tract. |
| `dot_scorer.py` | 2KB | 2026-06-18 | Scores precincts (Hispanic %, median age, homeownership) into high/medium/low tiers. |
| `fetch_age_by_precinct.py` | 5KB | 2026-06-12 | Builds age distribution by precinct, joins to precinct geometry. |
| `fetch_antinadeau.py` | 3KB | 2026-05-25 | Computes an 'anti-Nadeau' lean score per precinct from 2022 results. |
| `fetch_business.py` | 4KB | 2026-05-26 | Pulls DC DLCP business license data, maps closures to precincts via point-in-polygon. |
| `fetch_census_additions.py` | 2KB | 2026-05-25 | Pulls supplemental Census variables not in the base pull. |
| `fetch_census_notleftist.py` | 2KB | 2026-05-26 | Pulls Census data used for the 'not leftist' precinct score. |
| `fetch_crime.py` | 3KB | 2026-05-25 | Pulls MPD crime data by precinct. |
| `fetch_samesex_by_precinct.py` | 4KB | 2026-06-13 | Pulls Census same-sex household data by precinct. |
| `fetch_underlying_table.py` | 5KB | 2026-06-03 | Pulls MPD homicide counts by precinct for the underlying data table. |
| `fix_dots.py` | 0B | 2026-05-28 | EMPTY FILE — placeholder, currently unused. |
| `generate_2022_heatmap.py` | 5KB | 2026-06-16 | Builds the 2022 Nadeau vs Czapary choropleth (green=Czapary, orange=Nadeau). |
| `generate_targeting_map.py` | 3KB | 2026-05-28 | Builds the campaign targeting map with tier-based coloring from Final_Score. |
| `map_ward1.py` | 3KB | 2026-05-24 | Builds base Ward 1 precinct map from Census tract geometry. |
| `precinct_demographics.py` | 2KB | 2026-05-25 | Pulls and joins demographic data to precinct boundaries. |
| `remap_heatmap.py` | 5KB | 2026-06-09 | Utility for re-coloring/re-styling an existing Folium heatmap HTML. |
| `score_precincts.py` | 2KB | 2026-05-25 | Aggregates census data to precinct level (population-weighted) and merges with geo file. |
| `test_url.py` | 277B | 2026-05-23 | Quick script for testing an API/URL endpoint. |

## 📊 Data Files (CSV)

| File | Size | Last Modified | Description |
|---|---|---|---|
| `June_21_2022_Primary_Election_Certified_Results.csv` | 3MB | 2026-05-25 | DCBOE certified results, June 2022 primary (all races, all precincts). |
| `June_4_2024_Primary_Election_Certified_Results.csv` | 1MB | 2026-05-21 | DCBOE certified results, June 2024 primary (all races, all precincts). |
| `census_additions.csv` | 18KB | 2026-05-25 | Supplemental Census variables by tract. |
| `census_notleftist.csv` | 23KB | 2026-05-26 | Census data backing the 'not leftist' precinct score. |
| `dc_census_tracts.csv` | 24KB | 2026-05-25 | Raw DC Census tract reference data. |
| `ward1_age_precinct.csv` | 882B | 2026-06-12 | Age distribution by Ward 1 precinct. |
| `ward1_antinadeau.csv` | 972B | 2026-05-25 | Anti-Nadeau lean score by precinct (derived from 2022 results). |
| `ward1_business.csv` | 796B | 2026-05-26 | Business closures since 2015 by precinct. |
| `ward1_crime.csv` | 606B | 2026-05-25 | MPD crime stats by precinct. |
| `ward1_demographics.csv` | 643B | 2026-05-25 | Core demographic summary by precinct. |
| `ward1_demos_full.csv` | 5KB | 2026-06-09 | Full/expanded demographic table by precinct. |
| `ward1_lgbtq.csv` | 213B | 2026-05-26 | Same-sex household data by precinct. |
| `ward1_notleftist.csv` | 3KB | 2026-05-26 | Precinct-level 'not leftist' score components. |
| `ward1_race_census.csv` | 2KB | 2026-06-09 | Race/ethnicity breakdown by precinct. |
| `ward1_samesex_precinct.csv` | 250B | 2026-06-13 | Same-sex household percentages by precinct. |
| `ward1_scored.csv` | 2KB | 2026-06-04 | Final composite precinct scores (targeting tiers). |
| `ward1_underlying.csv` | 2KB | 2026-06-07 | Master underlying data table — feeds the Precinct Data tab. |

## 🗺️ Generated Maps (HTML)

| File | Size | Last Modified | Description |
|---|---|---|---|
| `ward1_2022_heatmap.html` | 207KB | 2026-06-16 | 2022 Nadeau vs Czapary results choropleth — used in Overview tab. |
| `ward1_heatmap.html` | 250KB | 2026-06-10 | Registered-Dems choropleth with candidate headshot markers — used in Overview tab. |
| `ward1_hotspot_map.html` | 5MB | 2026-05-23 | Large hotspot/density map (5MB) — likely an early or high-res version. |
| `ward1_targeting_map.html` | 211KB | 2026-06-10 | Campaign targeting map (tiered by Final_Score) for outreach planning. |

## 🗺️ Geo Data

| File | Size | Last Modified | Description |
|---|---|---|---|
| `ward1_with_tracts.geojson` | 1MB | 2026-05-25 | *(no description on file — add one in generate_readme.py)* |

## 🖼️ Images

| File | Size | Last Modified | Description |
|---|---|---|---|
| `Jackie-Reyes-Yanes.jpg` | 23KB | 2026-06-10 | Candidate headshot image (used as a map marker). |
| `Miguel-Trindade-Deramo.jpeg` | 20KB | 2026-06-10 | Candidate headshot image (used as a map marker). |
| `aparna-raj.png` | 78KB | 2026-06-10 | Candidate headshot image (used as a map marker). |
| `rashida-brown.jpeg` | 72KB | 2026-06-10 | Candidate headshot image (used as a map marker). |
| `terry-lynch.jpg` | 23KB | 2026-06-10 | Candidate headshot image (used as a map marker). |

## 📁 Other

| File | Size | Last Modified | Description |
|---|---|---|---|
| `.DS_Store` | 6KB | 2026-06-09 | *(no description on file — add one in generate_readme.py)* |
| `.env` | 55B | 2026-05-25 | Environment variables / API keys — DO NOT COMMIT TO GIT OR SHARE. |
| `.gitignore` | 10B | 2026-05-24 | *(no description on file — add one in generate_readme.py)* |
| `README.md` | 13B | 2026-05-22 | This file (auto-generated). |
| `requirements.txt` | 41B | 2026-05-21 | Python package dependencies. |
| `ward1intel_backup.zip` | 2MB | 2026-06-19 | *(no description on file — add one in generate_readme.py)* |

## Suggested pipeline order

1. **Fetch raw data**: `census_pull.py`, `census_pull_demos.py`, `fetch_*.py` scripts pull from Census/MPD/DLCP APIs into CSVs.
2. **Score & aggregate**: `score_precincts.py`, `dot_scorer.py` turn raw CSVs into precinct-level scores (`ward1_scored.csv`, `ward1_underlying.csv`).
3. **Generate maps**: `map_ward1.py`, `generate_targeting_map.py`, `generate_2022_heatmap.py` build the Folium HTML files embedded in Streamlit.
4. **Serve**: `Home.py` reads the CSVs and HTML files and renders the Streamlit app.
