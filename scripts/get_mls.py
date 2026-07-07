"""
Script from Week 1 for Aggregating MLS Data
Takes in a directory with csv files and aggregates them into a single csv file for sold and listings data.
by Jack Phelan
"""

import pandas as pd
import os
import argparse
from idx.config import DATA_DIR, RAW_LISTINGS_DIR, RAW_SOLD_DIR

INPUT_DIR = DATA_DIR
SOLD_DFS = []
LISTINGS_DFS = []


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    value = value.strip().lower()
    if value in {"true", "t", "1", "yes", "y"}:
        return True
    if value in {"false", "f", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError(
        "Expected a boolean value (true/false, 1/0, yes/no)."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate MLS Data")
    parser.add_argument("input_dir", type=str, help="The input directory to process")
    parser.add_argument(
        "--output_dir",
        type=str,
        help="The output directory to save the results",
        default=None,
    )
    parser.add_argument(
        "--property_type_filter",
        type=str_to_bool,
        help="filter for only residential properties",
        default=False,
    )

    args = parser.parse_args()
    INPUT_DIR = (
        args.input_dir if args.input_dir else os.path.dirname(os.path.abspath(__file__))
    )
    OUTPUT_DIR = (
        args.output_dir if args.output_dir else os.path.join(INPUT_DIR, "output")
    )
    TOTAL_SOLD_RECORDS = 0
    TOTAL_LISTING_RECORDS = 0
    TYPE_FILTER = args.property_type_filter

    print(f"Processing files in {INPUT_DIR} and saving to {OUTPUT_DIR}.")
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".csv"):
            if "Sold" in file:
                SOLD_DFS.append(
                    pd.read_csv(os.path.join(INPUT_DIR, file), low_memory=False)
                )
                TOTAL_SOLD_RECORDS += len(SOLD_DFS[-1])
            elif "Listing" in file:
                LISTINGS_DFS.append(
                    pd.read_csv(os.path.join(INPUT_DIR, file), low_memory=False)
                )
                TOTAL_LISTING_RECORDS += len(LISTINGS_DFS[-1])
    print(f"Found {len(SOLD_DFS)} sold files with {TOTAL_SOLD_RECORDS} records.")
    print(
        f"Found {len(LISTINGS_DFS)} listing files with {TOTAL_LISTING_RECORDS} records."
    )

    SOLD_DF = pd.concat(SOLD_DFS, ignore_index=True)
    LISTINGS_DF = pd.concat(LISTINGS_DFS, ignore_index=True)
    print(
        f"Aggregated {len(SOLD_DF)} sold records and {len(LISTINGS_DF)} listing records."
    )

    if TYPE_FILTER == True:
        SOLD_DF = SOLD_DF[SOLD_DF["PropertyType"] == "Residential"]
        LISTINGS_DF = LISTINGS_DF[LISTINGS_DF["PropertyType"] == "Residential"]
        print(
            f"Filtered to {len(SOLD_DF)} sold records and {len(LISTINGS_DF)} listing records for Residential properties."
        )
        SOLD_DF.to_csv(os.path.join(OUTPUT_DIR, "sold_filtered.csv"), index=False)
        LISTINGS_DF.to_csv(
            os.path.join(OUTPUT_DIR, "listings_filtered.csv"), index=False
        )
    else:
        SOLD_DF.to_csv(os.path.join(OUTPUT_DIR, "sold.csv"), index=False)
        LISTINGS_DF.to_csv(os.path.join(OUTPUT_DIR, "listings.csv"), index=False)

    print(f"Saved aggregated data to {OUTPUT_DIR}.")


def sold():
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".csv"):
            if "Sold" in file:
                SOLD_DFS.append(
                    pd.read_csv(os.path.join(INPUT_DIR, file), low_memory=False)
                )
    SOLD_DF = pd.concat(SOLD_DFS, ignore_index=True)
    return SOLD_DF


def listings():
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".csv"):
            if "Listing" in file:
                LISTINGS_DFS.append(
                    pd.read_csv(os.path.join(INPUT_DIR, file), low_memory=False)
                )
    LISTINGS_DF = pd.concat(LISTINGS_DFS, ignore_index=True)
    return LISTINGS_DF
