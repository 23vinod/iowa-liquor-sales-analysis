
from pathlib import Path
import pandas as pd

# Step 1: Locate the project folder
project_dir = Path(__file__).resolve().parent.parent

# Step 2: Locate the CSV file inside data
csv_path = project_dir / "data" / "iowa_liquor_sales_0001.csv"

# Step 3: Load the CSV file
df = pd.read_csv(csv_path)

# Step 4: Display the first five rows
print(df.head())

# Step 5: Check the dataset dimensions
print("Dataset shape:", df.shape)

# Step 6: Check column names and data types
df.info()

# Step 7: Check missing values
print(df.isnull().sum().sort_values(ascending=False).head(15))



# Find all CSV files in the data folder
csv_files = sorted((project_dir / "data").glob("iowa_liquor_sales_*.csv"))

print("Files found:", len(csv_files))

# Inspect the number of columns in each file
for file in csv_files:
    sample = pd.read_csv(file, nrows=5)
    print(file.name, sample.shape[1], "columns")



# Check all five CSV files
for file in csv_files:
    temp = pd.read_csv(file)

    print("\nFile:", file.name)
    print("Rows:", len(temp))
    print("Columns:", len(temp.columns))
    print("Total Sales: $", round(temp["sales_dollars"].sum(), 2))

    print("Missing Values:")
    print(temp.isnull().sum().sort_values(
        ascending=False
    ).head(5))

    del temp





# Verify that all files have matching columns
column_lists = [
    pd.read_csv(file, nrows=0).columns.tolist()
    for file in csv_files
]

same_columns = all(
    columns == column_lists[0]
    for columns in column_lists
)

print("All files have matching columns:", same_columns)
