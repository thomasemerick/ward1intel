import pandas as pd

df = pd.read_csv("ward1_demographics.csv")

# ── SCORING THRESHOLDS (based on actual data distribution) ─
# Hispanic: high = top third (>22%), medium = rest
# Median Age: high = >35, medium = 33-35, low = <33
# Owner Pct: high = >45%, medium = 30-45%, low = <30%
# Tenure: high = >80 years, medium = 65-80, low = <65

def score_hispanic(pct):
    if pct >= 22: return "🔴"
    elif pct >= 15: return "🟡"
    else: return "🟡"

def score_age(age):
    if age >= 36: return "🔴"
    elif age >= 34: return "🟡"
    else: return "🟡"

def score_owner(pct):
    if pct >= 45: return "🔴"
    elif pct >= 32: return "🟡"
    else: return "🟡"

def score_tenure(yrs):
    if yrs >= 80: return "🔴"
    elif yrs >= 67: return "🟡"
    else: return "🟡"

df["Hispanic_Score"] = df["Hispanic_Pct"].apply(score_hispanic)
df["Age_Score"] = df["Median_Age"].apply(score_age)
df["Owner_Score"] = df["Owner_Pct"].apply(score_owner)
df["Tenure_Score"] = df["Years_Since_Moved_In"].apply(score_tenure)

# ── Map scores to universe columns ─────────────────────────
# Hispanic → Hispanic universe
# Age + Owner + Tenure → White_46+ and White_NonLeft
# Owner → Schools (families with kids tend to be owners)
# Tenure → Anti_Nadeau proxy

df["Hispanic_Dot"] = df["Hispanic_Score"]
df["White_46plus_Dot"] = df.apply(
    lambda r: "🔴" if r["Age_Score"] == "🔴" or r["Owner_Score"] == "🔴" else "🟡", axis=1
)
df["White_NonLeft_Dot"] = df["White_46plus_Dot"]
df["Schools_Dot"] = df["Owner_Score"]  # owner = more likely to have kids in school
df["Anti_Nadeau_Dot"] = df["Tenure_Score"]  # longer tenure = knew Nadeau longer

print(df[["Precinct", "Neighborhood", "Hispanic_Dot", "White_46plus_Dot", "Schools_Dot", "Anti_Nadeau_Dot"]])
df.to_csv("ward1_scored.csv", index=False)
print("\nSaved to ward1_scored.csv")
