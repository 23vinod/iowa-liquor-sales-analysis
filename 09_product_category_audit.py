
from pathlib import Path
import pandas as pd

# Locate the project folder
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

# Identify products with multiple categories
category_counts = (
    df.groupby("item_no")["category_name"]
    .nunique(dropna=False)
)

conflict_items = category_counts[
    category_counts > 1
].index

# Preserve the original transactions
audit = df[
    df["item_no"].isin(conflict_items)
].copy()

# Group by product, category and month
audit["month"] = (
    audit["ordered_on"]
    .dt.to_period("M")
    .astype(str)
)

category_history = (
    audit.groupby(
        ["item_no", "im_desc", "category_name", "month"],
        dropna=False
    )
    .agg(
        transactions=("invoice_id", "size"),
        net_sales=("sales_dollars", "sum"),
        first_date=("ordered_on", "min"),
        last_date=("ordered_on", "max")
    )
    .reset_index()
    .sort_values(["item_no", "month", "category_name"])
)

# Display example product
print("\n=== CATEGORY HISTORY: ITEM 10785 ===")

print(
    category_history[
        category_history["item_no"] == 10785
    ].to_string(index=False)
)

# Summarize financial exposure
affected_sales = audit["sales_dollars"].sum()
total_sales = df["sales_dollars"].sum()

print("\n=== CATEGORY CONFLICT EXPOSURE ===")
print("Affected item numbers:", len(conflict_items))
print(f"Net sales on affected items: ${affected_sales:,.2f}")
print(f"Share of total sales: {affected_sales / total_sales * 100:.2f}%")

# Save audit report
output_dir = project_dir / "outputs"
output_dir.mkdir(exist_ok=True)

category_history.to_csv(
    output_dir / "category_conflict_audit.csv",
    index=False
)

print("\nCategory audit saved successfully!")
