
from pathlib import Path
import pandas as pd

# Locate the project and data folders
project_dir = Path(__file__).resolve().parent.parent
data_dir = project_dir / "data"

csv_files = sorted(data_dir.glob("iowa_liquor_sales_*.csv"))

for file in csv_files:
    print(f"\n--- {file.name} ---")

    rows = 0
    invalid_dates = 0
    outside_2024 = 0
    negative_sales = 0
    zero_sales = 0
    first_date = None
    last_date = None

    # Process in smaller batches to save memory
    for chunk in pd.read_csv(file, chunksize=100000):
        rows += len(chunk)

        dates = pd.to_datetime(
            chunk["ordered_on"], errors="coerce"
        )

        invalid_dates += dates.isna().sum()
        outside_2024 += (
            dates.notna() & (dates.dt.year != 2024)
        ).sum()

        negative_sales += (chunk["sales_dollars"] < 0).sum()
        zero_sales += (chunk["sales_dollars"] == 0).sum()

        if dates.notna().any():
            minimum = dates.min()
            maximum = dates.max()

            first_date = (
                minimum if first_date is None
                else min(first_date, minimum)
            )
            last_date = (
                maximum if last_date is None
                else max(last_date, maximum)
            )

    print("Rows:", rows)
    print("First date:", first_date)
    print("Last date:", last_date)
    print("Invalid dates:", invalid_dates)
    print("Dates outside 2024:", outside_2024)
    print("Negative sales:", negative_sales)
    print("Zero sales:", zero_sales)
