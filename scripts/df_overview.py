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
import sys
from pathlib import Path
from idx.utils import get_histogram, get_boxplot, get_missing_report
from idx.config import (
    RAW_LISTINGS_DIR,
    RAW_SOLD_DIR,
    NUMERIC_ANALYSIS_FIELDS,
    DISTRIBUTION_COLS,
)

pd.set_option("display.max_rows", None)


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


parser = argparse.ArgumentParser(description="Overview of a dataframe")
parser.add_argument("input_file", type=str, help="The input csv file path to process")
parser.add_argument(
    "--output-file",
    type=str,
    default=None,
    help="Optional text file path for saving all printed output",
)

args = parser.parse_args()
input_file = args.input_file

if args.output_file:
    output_path = Path(args.output_file)
else:
    input_path = Path(input_file)
    output_path = input_path.with_name(f"{input_path.stem}_overview.txt")

output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as output_handle:
    original_stdout = sys.stdout
    sys.stdout = Tee(sys.stdout, output_handle)
    try:
        print(f"Writing overview output to: {output_path.resolve()}")
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
            "Number of int columns:",
            len(df.select_dtypes(include=["int64"]).columns.tolist()),
        )
        print(
            "Number of object columns:",
            len(
                df.select_dtypes(
                    include=["object"], exclude=["string"]
                ).columns.tolist()
            ),
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
        print(
            "Dataframe after filtering has "
            f"{len(df)} rows and {len(df.columns)} columns."
        )

        print("\n")

        print("Missing Value Report:")
        print("-" * 40)
        print(get_missing_report(df, flag_high_missing=True, threshold=0.9))

        print("\n")

        print("Numeric Distribution Summary:")
        print("-" * 40)
        print(df[DISTRIBUTION_COLS].describe())
    finally:
        sys.stdout = original_stdout
