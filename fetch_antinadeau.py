import pandas as pd
import math

# --- Config ---
ELECTION_FILE = "June_21_2022_Primary_Election_Certified_Results.csv"
OUTPUT_FILE = "ward1_antinadeau.csv"
RED_THRESHOLD = 6.0

NEIGHBORHOOD = {
    20: 'LeDroit Park', 22: 'U Street', 23: 'Columbia Heights',
    24: 'Adams Morgan', 25: 'Adams Morgan', 35: 'Adams Morgan',
    36: 'Columbia Heights', 37: 'Pleasant Plains', 38: 'Park View',
    39: 'Mt Pleasant/Col Hts', 40: 'Mount Pleasant', 41: 'Columbia Heights',
    42: 'Columbia Heights', 43: 'Park View', 137: 'U Street'
}

WARD1_PRECINCTS = set(NEIGHBORHOOD.keys())

# --- Load ---
df = pd.read_csv(ELECTION_FILE)

# Filter to Ward 1 council DEM race only
mask = df['ContestName'] == 'DEM MEMBER OF THE COUNCIL OF THE DISTRICT OF COLUMBIA WARD ONE'
df = df[mask].copy()

# Drop over/under votes
df = df[~df['Candidate'].isin(['OVER VOTES', 'UNDER VOTES'])]

# Keep only Ward 1 precincts
df = df[df['PrecinctNumber'].isin(WARD1_PRECINCTS)]

# --- Pivot ---
pivot = df.pivot_table(index='PrecinctNumber', columns='Candidate', values='Votes', aggfunc='sum').fillna(0)

results = []
for p in sorted(WARD1_PRECINCTS):
    if p not in pivot.index:
        continue
    row = pivot.loc[p]
    nadeau  = row.get('Brianne K. Nadeau', 0)
    czapary = row.get('Salah Czapary', 0)
    harris  = row.get('Sabel Harris', 0)
    writein = row.get('Write-in', 0)

    total      = nadeau + czapary + harris + writein
    anti_votes = czapary + harris + writein
    anti_rate  = anti_votes / total if total > 0 else 0

    # Weighted volume: Czapary x2, Harris x1, writein x1
    anti_weighted_vol = (czapary * 2) + harris + writein

    # Score: rate is primary, log(weighted volume) breaks ties
    score_raw = anti_rate * math.log(anti_weighted_vol) if anti_weighted_vol > 0 else 0

    results.append({
        'PrecinctNumber': p,
        'Neighborhood': NEIGHBORHOOD[p],
        'Nadeau_2022': int(nadeau),
        'Czapary_2022': int(czapary),
        'Harris_2022': int(harris),
        'Total_2022': int(total),
        'AntiNadeau_Rate': round(anti_rate, 4),
        'AntiNadeau_WeightedVol': int(anti_weighted_vol),
        'score_raw': score_raw,
    })

out = pd.DataFrame(results)

# Normalize score to 0-10
min_s, max_s = out['score_raw'].min(), out['score_raw'].max()
out['AntiNadeau_Score'] = ((out['score_raw'] - min_s) / (max_s - min_s) * 10).round(1)
out['AntiNadeau_Dot'] = out['AntiNadeau_Score'].apply(lambda x: 'red' if x >= RED_THRESHOLD else 'yellow')

out = out.drop(columns=['score_raw']).sort_values('AntiNadeau_Score', ascending=False)

# --- Output ---
out.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {OUTPUT_FILE}\n")
print(out[['PrecinctNumber','Neighborhood','AntiNadeau_Rate','AntiNadeau_WeightedVol','AntiNadeau_Score','AntiNadeau_Dot']].to_string(index=False))

print(f"\nWard totals — Nadeau: {int(out.Nadeau_2022.sum())} Czapary: {int(out.Czapary_2022.sum())} Harris: {int(out.Harris_2022.sum())}")
print(f"Red precincts: {sorted(out[out.AntiNadeau_Dot=='red'].PrecinctNumber.tolist())}")
