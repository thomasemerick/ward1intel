from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()
api_key = os.getenv("CENSUS_API_KEY")

WARD1_TRACTS = [
    "002101", "002102", "002201", "002202",
    "002301", "002302", "002400", "002501",
    "002503", "002504", "002600", "002702",
    "002703", "002704",
]

BASE_URL = "https://api.census.gov/data/2023/acs/acs5"
GEO = {"for": "tract:*", "in": "state:11 county:001", "key": api_key}

def fetch(variables):
    params = {"get": "NAME," + ",".join(variables), **GEO}
    r = requests.get(BASE_URL, params=params)
    if r.status_code != 200 or not r.text.strip():
        print(f"API error {r.status_code}: {r.text[:200]}")
        return None
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df[df["tract"].isin(WARD1_TRACTS)].copy()

# ── Call 1: Race + Sex + total pop ──────────────────────────────────────────
df1 = fetch([
    "B01001_001E",  # Total pop
    "B01001_002E",  # Male total
    "B01001_026E",  # Female total
    "B02001_002E",  # White alone
    "B02001_003E",  # Black alone
    "B02001_004E",  # AIAN
    "B02001_005E",  # Asian alone
    "B02001_006E",  # NHPI
    "B02001_007E",  # Other race
    "B02001_008E",  # Two+ races
    "B03003_003E",  # Hispanic/Latino
])

# ── Call 2: Age (male) ───────────────────────────────────────────────────────
df2 = fetch([
    "B01001_003E","B01001_004E","B01001_005E","B01001_006E",  # M under 18
    "B01001_007E","B01001_008E","B01001_009E","B01001_010E",  # M 18-24
    "B01001_011E","B01001_012E","B01001_013E","B01001_014E",  # M 25-44
    "B01001_015E","B01001_016E","B01001_017E","B01001_018E","B01001_019E",  # M 45-64
    "B01001_020E","B01001_021E","B01001_022E","B01001_023E",
    "B01001_024E","B01001_025E",  # M 65+
])

# ── Call 3: Age (female) ─────────────────────────────────────────────────────
df3 = fetch([
    "B01001_027E","B01001_028E","B01001_029E","B01001_030E",  # F under 18
    "B01001_031E","B01001_032E","B01001_033E","B01001_034E",  # F 18-24
    "B01001_035E","B01001_036E","B01001_037E","B01001_038E",  # F 25-44
    "B01001_039E","B01001_040E","B01001_041E","B01001_042E","B01001_043E",  # F 45-64
    "B01001_044E","B01001_045E","B01001_046E","B01001_047E",
    "B01001_048E","B01001_049E",  # F 65+
])

# ── Call 4: Education ────────────────────────────────────────────────────────
df4 = fetch([
    "B15003_001E",  # Total 25+
    "B15003_002E","B15003_003E","B15003_004E","B15003_005E",
    "B15003_006E","B15003_007E","B15003_008E","B15003_009E",  # less than HS
    "B15003_017E","B15003_018E",  # HS diploma / GED
    "B15003_019E","B15003_020E",  # some college
    "B15003_021E",  # associate's
    "B15003_022E",  # bachelor's
    "B15003_023E","B15003_024E","B15003_025E",  # postgrad
])

# ── Merge all on tract ────────────────────────────────────────────────────────
df = df1.copy()
for d in [df2, df3, df4]:
    drop = [c for c in ["NAME","state","county"] if c in d.columns]
    df = df.merge(d.drop(columns=drop), on="tract", how="left")

# Convert numeric
skip = {"NAME","state","county","tract"}
for col in df.columns:
    if col not in skip:
        df[col] = pd.to_numeric(df[col], errors="coerce")

total = df["B01001_001E"].sum()

# ── Race ──────────────────────────────────────────────────────────────────────
df["NonHisp_White"] = (df["B02001_002E"] - df["B03003_003E"]).clip(lower=0)
race = {
    "Hispanic/Latino":   df["B03003_003E"].sum(),
    "Non-Hisp White":    df["NonHisp_White"].sum(),
    "Black":             df["B02001_003E"].sum(),
    "Asian":             df["B02001_005E"].sum(),
    "Other/Multiracial": (df[["B02001_004E","B02001_006E",
                               "B02001_007E","B02001_008E"]].sum(axis=1)).sum(),
}

# ── Age ───────────────────────────────────────────────────────────────────────
u18  = df[["B01001_003E","B01001_004E","B01001_005E","B01001_006E",
           "B01001_027E","B01001_028E","B01001_029E","B01001_030E"]].sum(axis=1).sum()
a1844= df[["B01001_007E","B01001_008E","B01001_009E","B01001_010E",
           "B01001_011E","B01001_012E","B01001_013E","B01001_014E",
           "B01001_031E","B01001_032E","B01001_033E","B01001_034E",
           "B01001_035E","B01001_036E","B01001_037E","B01001_038E"]].sum(axis=1).sum()
a4564= df[["B01001_015E","B01001_016E","B01001_017E","B01001_018E","B01001_019E",
           "B01001_039E","B01001_040E","B01001_041E","B01001_042E","B01001_043E"]].sum(axis=1).sum()
a65p = df[["B01001_020E","B01001_021E","B01001_022E","B01001_023E","B01001_024E","B01001_025E",
           "B01001_044E","B01001_045E","B01001_046E","B01001_047E","B01001_048E","B01001_049E"]].sum(axis=1).sum()

age = {"Under 18": u18, "18–44": a1844, "45–64": a4564, "65+": a65p}

# ── Gender ────────────────────────────────────────────────────────────────────
gender = {"Male": df["B01001_002E"].sum(), "Female": df["B01001_026E"].sum()}

# ── Education ─────────────────────────────────────────────────────────────────
edu_total  = df["B15003_001E"].sum()
no_hs      = df[["B15003_002E","B15003_003E","B15003_004E","B15003_005E",
                  "B15003_006E","B15003_007E","B15003_008E","B15003_009E"]].sum(axis=1).sum()
hs_ged     = df[["B15003_017E","B15003_018E"]].sum(axis=1).sum()
some_col   = df[["B15003_019E","B15003_020E"]].sum(axis=1).sum()
associates = df["B15003_021E"].sum()
bachelors  = df["B15003_022E"].sum()
postgrad   = df[["B15003_023E","B15003_024E","B15003_025E"]].sum(axis=1).sum()

edu = {
    "Less than HS":      no_hs,
    "HS diploma / GED":  hs_ged,
    "Some college":      some_col,
    "Associate's":       associates,
    "Bachelor's":        bachelors,
    "Postgraduate":      postgrad,
}

# ── Print ─────────────────────────────────────────────────────────────────────
print(f"\n=== Ward 1 Demographics — ACS 2023 5-yr ===")
print(f"Total population: {total:,}\n")

print("── Race/Ethnicity ──")
for k, v in race.items():
    print(f"  {k:<22} {v/total*100:5.1f}%  ({int(v):,})")

print("\n── Age ──")
for k, v in age.items():
    print(f"  {k:<10} {v/total*100:5.1f}%  ({int(v):,})")

print("\n── Gender ──")
for k, v in gender.items():
    print(f"  {k:<8} {v/total*100:5.1f}%  ({int(v):,})")

print("\n── Education (pop 25+) ──")
for k, v in edu.items():
    print(f"  {k:<22} {v/edu_total*100:5.1f}%  ({int(v):,})")

df.to_csv("ward1_demos_full.csv", index=False)
print("\nSaved to ward1_demos_full.csv")
