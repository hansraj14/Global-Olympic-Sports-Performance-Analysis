
import os
import pandas as pd

os.makedirs("data", exist_ok=True)

athletes = pd.read_csv("data/athletes_raw.csv")
medals = pd.read_csv("data/medals_raw.csv")

athletes.columns = athletes.columns.str.strip()
medals.columns = medals.columns.str.strip()

athletes = athletes.drop_duplicates()
medals = medals.drop_duplicates()

athletes["Year"] = pd.to_numeric(athletes["Year"], errors="coerce")
medals["year"] = pd.to_numeric(medals["year"], errors="coerce")

athletes = athletes[athletes["Year"].between(1992, 2026)].copy()
medals = medals[medals["year"].between(1992, 2026)].copy()

for col in ["Name", "Team", "NOC", "Games", "Season", "City", "Sport", "Event"]:
    if col in athletes.columns:
        athletes[col] = athletes[col].astype("string").str.strip()

athletes["Medal"] = athletes["Medal"].fillna("No Medal")

for col in ["gold", "silver", "bronze", "total"]:
    medals[col] = pd.to_numeric(medals[col], errors="coerce")

athletes.to_csv("data/olympic_athletes_clean.csv", index=False)
medals.to_csv("data/olympic_medals_clean.csv", index=False)

athlete_report = pd.DataFrame({
    "missing_count": athletes.isnull().sum(),
    "missing_percent": (athletes.isnull().mean() * 100).round(2)
})
athlete_report.to_csv("data/athletes_missing_report.csv")

medal_report = pd.DataFrame({
    "missing_count": medals.isnull().sum(),
    "missing_percent": (medals.isnull().mean() * 100).round(2)
})
medal_report.to_csv("data/medals_missing_report.csv")

valid_totals = (
    medals["gold"] + medals["silver"] + medals["bronze"]
    == medals["total"]
)

audit = {
    "athlete_rows": len(athletes),
    "medal_rows": len(medals),
    "athlete_duplicates": int(athletes.duplicated().sum()),
    "medal_duplicates": int(medals.duplicated().sum()),
    "athlete_missing_values": int(athletes.isnull().sum().sum()),
    "medal_missing_values": int(medals.isnull().sum().sum()),
    "athlete_min_year": athletes["Year"].min(),
    "athlete_max_year": athletes["Year"].max(),
    "medal_min_year": medals["year"].min(),
    "medal_max_year": medals["year"].max(),
    "medal_total_mismatches": int((~valid_totals).sum())
}

pd.Series(audit, name="value").to_csv("data/validation_report.csv")

print("FINAL DATA PREPARATION COMPLETED")
for key, value in audit.items():
    print(f"{key}: {value}")
