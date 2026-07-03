"""
Script for giving an overview of a dataframe; missing values, datatypes, and basic statistics.
By Jack Phelan

GOALS:

Submit a .py script:
- documenting unique property types found
- the filtering logic applied
- null-count summary table
- Include a missing value report flagging any columns above 90% null.
- Produce a numeric distribution summary (min, max, mean, median, percentiles) for ClosePrice, LivingArea, and DaysOnMarket.
- Save the filtered dataset as a new CSV.


"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
from idx.utils import get_histogram, get_boxplot, get_missing_report
from idx.config import (
    RAW_LISTINGS_DIR,
    RAW_SOLD_DIR,
    NUMERIC_ANALYSIS_FIELDS,
    DISTRIBUTION_COLS,
)

parser = argparse.ArgumentParser(description="Overview of a dataframe")
parser.add_argument("input_file", type=str, help="The input csv file path to process")

args = parser.parse_args()

input_file = args.input_file

df = pd.read_csv(input_file, low_memory=False)
print("\n")
print("Dataframe found with " f"{len(df)} rows and {len(df.columns)} columns.")
print("\n")
print("Column Breakdown:")
print("-" * 40)
print(
    "Number of float columns:",
    len(df.select_dtypes(include=["float64"]).columns.tolist()),
)
print(
    "Number of int columns:", len(df.select_dtypes(include=["int64"]).columns.tolist())
)
print(
    "Number of object columns:",
    len(df.select_dtypes(include=["object"], exclude=["string"]).columns.tolist()),
)
print(
    "Number of string columns:",
    len(df.select_dtypes(include=["string"]).columns.tolist()),
)
print("\n")

PROPERTY_TYPE_FLAG = "PropertyType" in df.columns
print("Checking if filtered on PropertyType...\n")
print("PropertyType unique values:")
if not PROPERTY_TYPE_FLAG:
    print("PropertyType column not found in dataframe.")
else:
    print(df["PropertyType"].unique())

if PROPERTY_TYPE_FLAG and df["PropertyType"].nunique() > 1:
    target_property_type = "Residential"
    before_count = len(df)
    print(
        f"Multiple property types found. Now filtering to only include '{target_property_type}' property types..."
    )
    df = df[df["PropertyType"].astype(str).str.strip() == target_property_type]
    after_count = len(df)
    print(f"Filtered rows: {before_count} -> {after_count}")

print("\n")

print("PropertyType values after filtering:")
if PROPERTY_TYPE_FLAG:
    print(df["PropertyType"].unique())
else:
    print("PropertyType column not found in dataframe.")
print("\n")
print("Dataframe after filtering has " f"{len(df)} rows and {len(df.columns)} columns.")

print("\n")

print("Missing Value Report:")
print("-" * 40)
print(get_missing_report(df, flag_high_missing=True, threshold=0.9))

print("\n")

print("Numeric Distribution Summary:")
print("-" * 40)
print(df[DISTRIBUTION_COLS].describe())
