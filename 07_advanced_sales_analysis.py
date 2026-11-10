
from pathlib import Path
import pandas as pd

# STEP 1: Load the cleaned dataset
project_dir = Path(__file__).resolve().parent.parent

file_path = (
    project_dir / "data" / "cleaned"
    / "iowa_liquor_sales_2024_cleaned.csv"
)

df = pd.read_csv(
    file_path,
    parse_dates=["ordered_on"]
)

total_sales = df["sales_dollars"].sum()

print(f"Total net sales: ${total_sales:,.2f}")

# STEP 2: Top 10 products by revenue
top_products = (
    df.groupby(["item_no", "im_desc"], dropna=False)
      .agg(
          net_sales=("sales_dollars", "sum"),
          bottles=("sales_bottles", "sum")
      )
      .sort_values("net_sales", ascending=False)
      .head(10)
)

print("\n--- TOP 10 PRODUCTS ---")
print(top_products.to_string())

# STEP 3: Top 10 retail stores
top_stores = (
    df.groupby(["store_no", "store_name"], dropna=False)
      .agg(
          net_sales=("sales_dollars", "sum"),
          bottles=("sales_bottles", "sum")
      )
      .sort_values("net_sales", ascending=False)
      .head(10)
)

top_stores["sales_share_pct"] = (
    top_stores["net_sales"] / total_sales * 100
)

print("\n--- TOP 10 STORES ---")
print(top_stores.to_string())

# STEP 4: Retailer concentration
store_sales = (
    df.groupby("store_no")["sales_dollars"]
      .sum()
      .sort_values(ascending=False)
)

top_10_share = (
    store_sales.head(10).sum() / total_sales * 100
)

print(f"\nTop 10 store revenue share: {top_10_share:.2f}%")

# STEP 5: County sales performance
county_sales = (
    df.groupby("county_name", dropna=False)
      .agg(
          net_sales=("sales_dollars", "sum"),
          bottles=("sales_bottles", "sum"),
          stores=("store_no", "nunique")
      )
      .sort_values("net_sales", ascending=False)
)

print("\n--- TOP 10 COUNTIES ---")
print(county_sales.head(10).to_string())

# STEP 6: Monthly sales and growth
monthly_sales = (
    df.groupby(df["ordered_on"].dt.to_period("M"))
      ["sales_dollars"]
      .sum()
      .reset_index(name="net_sales")
)

monthly_sales["monthly_growth_pct"] = (
    monthly_sales["net_sales"].pct_change() * 100
)

print("\n--- MONTHLY SALES GROWTH ---")
print(monthly_sales.to_string(index=False))




# STEP 7: Detailed product performance

product_details = (
    df.groupby(
        [
            "item_no",
            "im_desc",
            "category_name",
            "bottle_volume_ml",
            "pack"
        ],
        dropna=False
    )
    .agg(
        bottles_sold=("sales_bottles", "sum"),
        volume_liters=("sales_liters", "sum"),
        net_sales=("sales_dollars", "sum")
    )
    .reset_index()
)

# Convert bottle size into a readable label
product_details["size"] = (
    product_details["bottle_volume_ml"]
    .astype("Int64")
    .astype(str) + " mL"
)

# Sort by highest revenue
top_10_detailed = (
    product_details
    .sort_values("net_sales", ascending=False)
    .head(10)
)

print("\n--- TOP 10 PRODUCTS WITH SIZE AND CATEGORY ---")


# Make the report easier to read

report = top_10_detailed[
    [
        "item_no",
        "im_desc",
        "size",
        "category_name",
        "pack",
        "bottles_sold",
        "net_sales"
    ]
].copy()

report["net_sales"] = report["net_sales"].map(
    lambda x: f"${x:,.2f}"
)

report["bottles_sold"] = report["bottles_sold"].map(
    lambda x: f"{x:,}"
)

print("\n--- PRODUCT PERFORMANCE REPORT ---")
print(report.to_string(index=False))



# STEP 8: Bottle size performance

size_analysis = (
    df.groupby("bottle_volume_ml", dropna=False)
      .agg(
          total_revenue=("sales_dollars", "sum"),
          total_bottles=("sales_bottles", "sum"),
          total_liters=("sales_liters", "sum"),
          unique_products=("item_no", "nunique")
      )
      .reset_index()
)

size_analysis["revenue_share_pct"] = (
    size_analysis["total_revenue"]
    / df["sales_dollars"].sum() * 100
)

size_analysis = size_analysis.sort_values(
    "total_revenue",
    ascending=False
)

print("\n--- BOTTLE SIZE PERFORMANCE ---")
print(size_analysis.head(15).to_string(index=False))

# Save for dashboard
output_dir = project_dir / "outputs"
output_dir.mkdir(exist_ok=True)

size_analysis.to_csv(
    output_dir / "bottle_size_analysis.csv",
    index=False
)

print("\nBottle size report saved!")




# Save the full product-level analysis
output_dir = project_dir / "outputs"
output_dir.mkdir(exist_ok=True)

product_details.to_csv(
    output_dir / "product_details.csv",
    index=False
)

print("Detailed product report saved successfully!")
