
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent.parent
data_dir = project_dir / "data"

raw_files = sorted(
    data_dir.glob("iowa_liquor_sales_*.csv")
)

cleaned_file = (
    data_dir / "cleaned"
    / "iowa_liquor_sales_2024_cleaned.csv"
)

raw_rows = 0
raw_sales = 0.0

# Calculate raw totals independently
for file in raw_files:
    for chunk in pd.read_csv(
        file,
        usecols=["sales_dollars"],
        chunksize=100000
    ):
        raw_rows += len(chunk)
        raw_sales += chunk["sales_dollars"].sum()

cleaned_rows = 0
cleaned_sales = 0.0

# Calculate cleaned totals independently
for chunk in pd.read_csv(
    cleaned_file,
    usecols=["sales_dollars"],
    chunksize=100000
):
    cleaned_rows += len(chunk)
    cleaned_sales += chunk["sales_dollars"].sum()

print("\n--- SALES RECONCILIATION ---")
print(f"Raw rows: {raw_rows:,}")
print(f"Cleaned rows: {cleaned_rows:,}")
print(f"Raw sales: ${raw_sales:,.2f}")
print(f"Cleaned sales: ${cleaned_sales:,.2f}")
print(f"Difference: ${cleaned_sales - raw_sales:,.2f}")

print("Rows match:", raw_rows == cleaned_rows)
print(
    "Sales match:",
    abs(cleaned_sales - raw_sales) < 0.01
)
