
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent.parent
data_dir = project_dir / "data"

csv_files = sorted(data_dir.glob("iowa_liquor_sales_*.csv"))

# Load all five files
df = pd.concat(
    [pd.read_csv(file) for file in csv_files],
    ignore_index=True
)

print("Total rows:", len(df))

# Check exact duplicate records
exact_duplicates = df.duplicated().sum()

print("Exact duplicate rows:", exact_duplicates)

# Check repeated invoice IDs
repeated_invoices = df["invoice_id"].duplicated().sum()

print("Repeated invoice IDs:", repeated_invoices)

# Check how many unique invoice IDs exist
unique_invoices = df["invoice_id"].nunique()

print("Unique invoice IDs:", unique_invoices)

# Check rows after removing exact duplicates
print(
    "Rows after exact deduplication:",
    len(df.drop_duplicates())
)

# Inspect a sample of repeated invoice IDs
repeated_rows = df[
    df["invoice_id"].duplicated(keep=False)
]

print("\nSample repeated invoice IDs:")
print(
    repeated_rows[
        ["invoice_id", "item_no", "sales_bottles", "sales_dollars"]
    ].head(10).to_string(index=False)
)




print("\n--- FINAL ROW COUNT VERIFICATION ---")

total_rows = 0

for file in csv_files:
    row_count = sum(
        len(chunk)
        for chunk in pd.read_csv(file, chunksize=100000)
    )

    print(file.name, ":", row_count)
    total_rows += row_count

print("Total rows from CSV files:", total_rows)
print("Total rows in combined DataFrame:", len(df))

print(
    "Counts match:",
    total_rows == len(df)
)
