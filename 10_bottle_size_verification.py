
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent.parent

file_path = (
    project_dir
    / "data"
    / "cleaned"
    / "iowa_liquor_sales_2024_cleaned.csv"
)

df = pd.read_csv(
    file_path,
    parse_dates=["ordered_on"],
    low_memory=False
)

print("=== DATA LOADED ===")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

# Count distinct bottle sizes for each item
size_counts = (
    df.groupby("item_no")["bottle_volume_ml"]
    .nunique(dropna=False)
)

conflict_items = size_counts[
    size_counts > 1
].index

print("\n=== BOTTLE SIZE CONFLICTS ===")
print("Affected item numbers:", len(conflict_items))

# Display the different recorded sizes
size_conflicts = (
    df[df["item_no"].isin(conflict_items)]
    .groupby(
        ["item_no", "im_desc", "bottle_volume_ml"],
        dropna=False
    )
    .agg(
        transactions=("invoice_id", "size"),
        net_sales=("sales_dollars", "sum"),
        bottles=("sales_bottles", "sum")
    )
    .reset_index()
    .sort_values(["item_no", "bottle_volume_ml"])
)

print(size_conflicts.to_string(index=False))




# Calculate expected liters from bottle size
df["calculated_liters"] = (
    df["sales_bottles"]
    * df["bottle_volume_ml"]
    / 1000
)

# Compare with reported liters
df["liters_difference"] = (
    df["sales_liters"]
    - df["calculated_liters"]
)

print("\n=== LITERS RECONCILIATION ===")

reported = df["sales_liters"].sum()
calculated = df["calculated_liters"].sum()
difference = reported - calculated

print(f"Reported liters: {reported:,.2f}")
print(f"Calculated liters: {calculated:,.2f}")
print(f"Difference: {difference:,.2f}")

# Check discrepancies at different thresholds
for threshold in [0.001, 0.01, 0.1, 1.0]:
    count = (
        df["liters_difference"].abs() > threshold
    ).sum()

    print(
        f"Rows with difference > {threshold}: {count:,}"
    )

# Show the most significant individual differences
largest_differences = (
    df.loc[
        df["liters_difference"].abs().nlargest(10).index,
        [
            "invoice_id",
            "item_no",
            "sales_bottles",
            "bottle_volume_ml",
            "sales_liters",
            "calculated_liters",
            "liters_difference"
        ]
    ]
)

print("\n=== LARGEST ROW DIFFERENCES ===")
print(largest_differences.to_string(index=False))




print("\n=== BOTTLE SIZE PERFORMANCE ===")

size_report = (
    df.groupby("bottle_volume_ml", dropna=False)
    .agg(
        net_sales=("sales_dollars", "sum"),
        bottles_sold=("sales_bottles", "sum"),
        reported_liters=("sales_liters", "sum"),
        calculated_liters=("calculated_liters", "sum"),
        unique_products=("item_no", "nunique")
    )
    .reset_index()
)

total_sales = df["sales_dollars"].sum()

size_report["revenue_share_pct"] = (
    size_report["net_sales"] / total_sales * 100
)

size_report = size_report.sort_values(
    "net_sales",
    ascending=False
)

print(
    size_report.head(10).to_string(
        index=False,
        float_format=lambda x: f"{x:,.2f}"
    )
)

print("\n=== RECONCILIATION ===")

print(
    "Revenue shares total:",
    round(size_report["revenue_share_pct"].sum(), 6)
)

print(
    "Sales match:",
    abs(size_report["net_sales"].sum() - total_sales) < 0.01
)

print(
    "Bottles match:",
    size_report["bottles_sold"].sum()
    == df["sales_bottles"].sum()
)


output_dir = project_dir / "outputs"
output_dir.mkdir(exist_ok=True)

size_conflicts.to_csv(
    output_dir / "bottle_size_conflicts.csv",
    index=False
)

size_report.to_csv(
    output_dir / "verified_bottle_size_report.csv",
    index=False
)

largest_differences.to_csv(
    output_dir / "liters_discrepancy_samples.csv",
    index=False
)

print("\n=== REPORTS SAVED ===")
print("Bottle-size conflict report saved.")
print("Verified bottle-size report saved.")
print("Liters discrepancy samples saved.")
