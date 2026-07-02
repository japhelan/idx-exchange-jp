"""
Script for giving an overview of a dataframe; missing values, datatypes, and basic statistics.
By Jack Phelan
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
from idx.utils import get_histogram, get_boxplot, get_missing_report
from idx.config import RAW_LISTINGS_DIR, RAW_SOLD_DIR

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

print("Missing Value Report:")
print("-" * 40)
print(get_missing_report(df, flag_high_missing=True, threshold=0.9))

print("\n")

# Check property categories
print(df["PropertyType"].unique())
