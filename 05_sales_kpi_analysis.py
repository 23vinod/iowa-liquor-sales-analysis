
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent.parent

file_path = (
    project_dir / "data" / "cleaned"
    / "iowa_liquor_sales_2024_cleaned.csv"
)

df = pd.read_csv(file_path, parse_dates=["ordered_on"])

# 1. Total net sales
net_sales = df["sales_dollars"].sum()

# 2. Positive sales and negative adjustments
positive_sales = df.loc[
    df["sales_dollars"] > 0, "sales_dollars"
].sum()

negative_adjustments = df.loc[
    df["sales_dollars"] < 0, "sales_dollars"
].sum()

# 3. Total net bottles and liters
total_bottles = df["sales_bottles"].sum()
total_liters = df["sales_liters"].sum()

# 4. Number of unique stores and products
unique_stores = df["store_no"].nunique()
unique_products = df["item_no"].nunique()

print("\n--- SALES KPI SUMMARY ---")
print(f"Net sales: ${net_sales:,.2f}")
print(f"Positive sales: ${positive_sales:,.2f}")
print(f"Negative adjustments: ${negative_adjustments:,.2f}")
print(f"Net bottles: {total_bottles:,}")
print(f"Net liters: {total_liters:,.2f}")
print(f"Unique stores: {unique_stores:,}")
print(f"Unique products: {unique_products:,}")

# 5. Top 10 products by net sales
top_products = (
    df.groupby(["item_no", "im_desc"], dropna=False)
      ["sales_dollars"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\n--- TOP 10 PRODUCTS ---")
print(top_products)

# 6. Top 10 stores by net sales
top_stores = (
    df.groupby(["store_no", "store_name"], dropna=False)
      ["sales_dollars"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\n--- TOP 10 STORES ---")
print(top_stores)

# 7. Monthly sales
monthly_sales = (
    df.groupby(df["ordered_on"].dt.to_period("M"))
      ["sales_dollars"]
      .sum()
)

print("\n--- MONTHLY NET SALES ---")
print(monthly_sales)
