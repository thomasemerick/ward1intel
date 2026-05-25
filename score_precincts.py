import pandas as pd
import geopandas as gpd

# ── Load data ─────────────────────────────────────────────
census = pd.read_csv("dc_census_tracts.csv")
census["Years_Since_Moved_In"] = census["Years_Since_Moved_In"].clip(0, 100)
census["tract"] = census["tract"].astype(str).str.zfill(6)

joined = gpd.read_file("ward1_with_tracts.geojson")
joined["TRACT"] = joined["TRACT"].astype(str).str.zfill(6)

# ── Merge census data onto joined file ────────────────────
merged = joined.merge(census, left_on="TRACT", right_on="tract", how="left")

# ── Aggregate to precinct level (population-weighted) ─────
def wavg(group, col, weight="Total_Pop"):
    w = group[weight].fillna(0)
    if w.sum() == 0:
        return None
    return (group[col] * w).sum() / w.sum()

results = []
for precinct, group in merged.groupby("Precinct"):
    results.append({
        "Precinct": precinct,
        "Hispanic_Pct": round(wavg(group, "Hispanic_Pct"), 1),
        "Median_Age": round(wavg(group, "Median_Age"), 1),
        "Owner_Pct": round(wavg(group, "Owner_Pct"), 1),
        "Years_Since_Moved_In": round(wavg(group, "Years_Since_Moved_In"), 1),
    })

results_df = pd.DataFrame(results).sort_values("Precinct")

# ── Add neighborhood names ────────────────────────────────
neighborhoods = {
    20: "LeDroit Park", 22: "U Street", 23: "Columbia Heights",
    24: "Adams Morgan", 25: "Adams Morgan", 35: "Adams Morgan",
    36: "Columbia Heights", 37: "Pleasant Plains", 38: "Park View",
    39: "Mount Pleasant/Columbia Heights", 40: "Mount Pleasant",
    41: "Columbia Heights", 42: "Columbia Heights",
    43: "Park View", 137: "U Street"
}
results_df["Neighborhood"] = results_df["Precinct"].map(neighborhoods)

print(results_df[["Precinct", "Neighborhood", "Hispanic_Pct", "Median_Age", "Owner_Pct", "Years_Since_Moved_In"]])
results_df.to_csv("ward1_demographics.csv", index=False)
print("\nSaved to ward1_demographics.csv")
