import pandas as pd

files = {
    "Athletes": "data/olympic_athletes_clean.csv",
    "Medals": "data/olympic_medals_clean.csv"
}

athletes = pd.read_csv("data/olympic_athletes_clean.csv")
medals = pd.read_csv("data/olympic_medals_clean.csv")

print("ATHLETES DATASET")
print("Rows:", len(athletes))
print("Duplicate rows:", athletes.duplicated().sum())
print("Year range:", athletes["Year"].min(), "-", athletes["Year"].max())
print("Missing values:", athletes.isnull().sum().sum())

print("\nMEDAL DATASET")
print("Rows:", len(medals))
print("Duplicate rows:", medals.duplicated().sum())
print("Year range:", medals["year"].min(), "-", medals["year"].max())
print("Missing values:", medals.isnull().sum().sum())
for name, path in files.items():
    df = pd.read_csv(path)

    report = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Missing Percentage": (df.isnull().mean() * 100).round(2)
    })

    report = report[report["Missing Count"] > 0]
    report.to_csv(f"data/{name.lower()}_missing_report.csv")

    print(f"\n{name} Missing Values")
    print(report.to_string())

print("\nMissing value reports created.")