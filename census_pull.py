from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()
api_key = os.getenv("CENSUS_API_KEY")

url = "https://api.census.gov/data/2023/acs/acs5"
params = {
    "get": "B03003_003E,B01001_001E,B01002_001E,B25003_002E,B25003_001E,B25035_001E,NAME",
    "for": "tract:*",
    "in": "state:11 county:001",
    "key": api_key
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data[1:], columns=data[0])
df.columns = ["Hispanic_Pop", "Total_Pop", "Median_Age", "Owner_Occupied", "Total_Occupied", "Median_Year_Moved_In", "NAME", "state", "county", "tract"]

# Convert to numeric
for col in ["Hispanic_Pop", "Total_Pop", "Median_Age", "Owner_Occupied", "Total_Occupied", "Median_Year_Moved_In"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Calculate derived metrics
df["Hispanic_Pct"] = (df["Hispanic_Pop"] / df["Total_Pop"] * 100).round(1)
df["Owner_Pct"] = (df["Owner_Occupied"] / df["Total_Occupied"] * 100).round(1)
df["Years_Since_Moved_In"] = (2024 - df["Median_Year_Moved_In"]).round(1)

print(df[["NAME", "Hispanic_Pct", "Median_Age", "Owner_Pct", "Years_Since_Moved_In"]].head(10))
print(f"Total tracts: {len(df)}")
df.to_csv("dc_census_tracts.csv", index=False)
print("Saved to dc_census_tracts.csv")
