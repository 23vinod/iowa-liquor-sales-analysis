
import pandas as pd
from pathlib import Path

# Locate the project folder
project_dir = Path(__file__).resolve().parent.parent

# Load cleaned data
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
print("Net sales: ${:,.2f}".format(df["sales_dollars"].sum()))



print("\n=== PRODUCT CONSISTENCY ===")

product_check = (
    df.groupby("item_no")
    .agg(
        descriptions=("im_desc", "nunique"),
        sizes=("bottle_volume_ml", "nunique"),
        categories=("category_name", "nunique"),
        vendors=("vendor_number", "nunique")
    )
)

conflicts = product_check[
    (product_check["descriptions"] > 1)
    | (product_check["sizes"] > 1)
    | (product_check["categories"] > 1)
    | (product_check["vendors"] > 1)
]

print("Unique item numbers:", len(product_check))
print("Items with conflicting attributes:", len(conflicts))

print("\nSample conflicts:")
print(conflicts.head(10).to_string())



print("\n=== NEGATIVE ADJUSTMENTS ===")

negative = df[df["sales_dollars"] < 0].copy()

print("Negative transactions:", len(negative))
print(
    "Adjustment total: ${:,.2f}".format(
        negative["sales_dollars"].sum()
    )
)

# Negative adjustments by category
category_adjustments = (
    negative.groupby("category_name", dropna=False)
    .agg(
        transactions=("sales_dollars", "size"),
        adjustment_dollars=("sales_dollars", "sum")
    )
    .sort_values("adjustment_dollars")
)

print("\nTop 10 categories by adjustment magnitude:")
print(category_adjustments.head(10).to_string())

# Negative adjustments by month
negative["month"] = negative["ordered_on"].dt.to_period("M")

monthly_adjustments = (
    negative.groupby("month")["sales_dollars"]
    .sum()
)

print("\nMonthly adjustments:")
print(monthly_adjustments.to_string())



print("\n=== GEOGRAPHIC DATA QUALITY ===")

geo_columns = [
    "store_zip_code",
    "county_fips_code"
]

for col in geo_columns:
    missing = df[col].isna().sum()

    print(
        f"{col}: {missing:,} missing "
        f"({missing / len(df) * 100:.4f}%)"
    )

# Rows missing at least one geographic field
missing_geo = df[
    df[geo_columns].isna().any(axis=1)
]

print("\nRows with missing geography:", len(missing_geo))

print(
    "Net sales affected: ${:,.2f}".format(
        missing_geo["sales_dollars"].sum()
    )
)




print("\n=== KPI VALIDATION ===")

total_sales = df["sales_dollars"].sum()
total_bottles = df["sales_bottles"].sum()
total_liters = df["sales_liters"].sum()

print(f"Net sales: ${total_sales:,.2f}")
print(f"Net bottles: {total_bottles:,.0f}")
print(f"Net liters: {total_liters:,.2f}")

# Revenue by bottle size
size_sales = (
    df.groupby("bottle_volume_ml", dropna=False)
    ["sales_dollars"]
    .sum()
)

revenue_share = (
    size_sales / total_sales * 100
)

print("\nSum of bottle-size revenue shares:")
print(f"{revenue_share.sum():.6f}%")

# Compare reported liters to bottle-derived liters
calculated_liters = (
    df["sales_bottles"]
    * df["bottle_volume_ml"]
    / 1000
)

liter_difference = (
    df["sales_liters"] - calculated_liters
)

print("\nTotal reported vs calculated liters difference:")
print(f"{liter_difference.sum():,.4f}")

print("Rows with liter differences greater than 0.01:")
print((liter_difference.abs() > 0.01).sum())




print("\n=== SAVING QUALITY REPORTS ===")

output_dir = project_dir / "outputs"
output_dir.mkdir(exist_ok=True)

# Save product conflicts
conflicts.to_csv(
    output_dir / "product_consistency_issues.csv"
)

# Save category adjustments
category_adjustments.to_csv(
    output_dir / "negative_adjustments_by_category.csv"
)

# Save monthly adjustments
monthly_adjustments.to_csv(
    output_dir / "negative_adjustments_by_month.csv"
)

# Save missing geography rows for review
missing_geo.to_csv(
    output_dir / "missing_geography_records.csv",
    index=False
)

# Save bottle-size revenue share validation
revenue_share.rename("revenue_share_pct").to_csv(
    output_dir / "bottle_size_revenue_share_check.csv"
)

print("Final quality reports saved successfully!")




print("\n=== CONFLICT TYPE SUMMARY ===")

for col in ["descriptions", "sizes", "categories", "vendors"]:
    count = (product_check[col] > 1).sum()
    print(f"Items with multiple {col}: {count}")

print("\n=== SAMPLE CATEGORY CONFLICT ===")

sample_items = conflicts[
    conflicts["categories"] > 1
].head(5).index

sample = (
    df[df["item_no"].isin(sample_items)]
    [[
        "item_no",
        "im_desc",
        "bottle_volume_ml",
        "category_name",
        "vendor_name"
    ]]
    .drop_duplicates()
    .sort_values("item_no")
)

print(sample.to_string(index=False))