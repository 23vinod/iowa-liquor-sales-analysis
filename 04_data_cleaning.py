
from pathlib import Path
import pandas as pd

# STEP 1: Locate folders
project_dir = Path(__file__).resolve().parent.parent
data_dir = project_dir / "data"
clean_dir = data_dir / "cleaned"

clean_dir.mkdir(exist_ok=True)

# STEP 2: Find original CSV files
csv_files = sorted(
    data_dir.glob("iowa_liquor_sales_*.csv")
)

print("Files found:", len(csv_files))

# STEP 3: Load and combine the five files
df = pd.concat(
    [pd.read_csv(file) for file in csv_files],
    ignore_index=True
)

print("Original rows:", len(df))

# STEP 4: Convert order date to datetime
df["ordered_on"] = pd.to_datetime(
    df["ordered_on"],
    errors="coerce"
)

# STEP 5: Remove completely empty price columns
columns_to_drop = [
    "state_bottle_cost",
    "state_bottle_retail"
]

df = df.drop(columns=columns_to_drop)

# STEP 6: Fill missing location descriptions
location_columns = [
    "store_address",
    "store_city",
    "county_name"
]

for col in location_columns:
    df[col] = df[col].fillna("Unknown")

# STEP 7: Preserve missing ZIP/FIPS identifiers
# Convert to nullable strings instead of replacing
# missing identifiers with zero.
for col in ["store_zip_code", "county_fips_code"]:
    df[col] = (
        pd.to_numeric(df[col], errors="coerce")
        .astype("Int64")
        .astype("string")
    )

# STEP 8: Flag negative sales
df["transaction_type"] = "Positive Sale"

df.loc[
    df["sales_dollars"] < 0,
    "transaction_type"
] = "Negative Adjustment"

# STEP 9: Create year and month columns
df["year"] = df["ordered_on"].dt.year
df["month"] = df["ordered_on"].dt.month

# STEP 10: Save cleaned dataset
output_path = (
    clean_dir / "iowa_liquor_sales_2024_cleaned.csv"
)

df.to_csv(output_path, index=False)

# STEP 11: Validate output
print("\n--- CLEANING SUMMARY ---")
print("Cleaned rows:", len(df))
print("Cleaned columns:", len(df.columns))
print("Missing dates:", df["ordered_on"].isna().sum())

print("\nTransaction types:")
print(df["transaction_type"].value_counts())

print("\nMissing values remaining:")
print(
    df.isna().sum().sort_values(
        ascending=False
    ).head(10)
)

print("\nSaved cleaned data to:")
print(output_path)
