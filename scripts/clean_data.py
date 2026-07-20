"""
script for applying steps performed in data cleaning notebook to a selected dataset
"""

# setup
import pandas as pd
import re
from idx import config
import argparse
import os
from pathlib import Path

COLS_TO_DROP = config.COLS_TO_DROP
DT_COLS = config.DT_COLS
INT_COLS = config.INT_COLS
NON_PREDICTIVE_COLS = config.NON_PREDICTIVE_COLS
NON_ANALYSIS_COLS = config.NON_ANALYSIS_COLS
NON_NEG_FLAG_COLS = config.NON_NEG_FLAG_COLS

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Clean MLS Data")
    parser.add_argument("input_path", type=str, help="The csv path to clean")
    parser.add_argument(
        "--output_path",
        type=str,
        help="The output directory to save the results",
        default=None,
    )
    args = parser.parse_args()

    INPUT_PATH = (
        args.input_path
        if args.input_path
        else os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.csv")
    )
    OUTPUT_PATH = (
        args.output_path
        if args.output_path
        else os.path.join(os.path.dirname(INPUT_PATH), "cleaned_data.csv")
    )

    print(f"Processing file {INPUT_PATH} and saving to {OUTPUT_PATH}.")
    df = pd.read_csv(INPUT_PATH, low_memory=False)

    print(f"Initial info on dataset:\n")
    print(f"{df.shape[0]}", f"rows and {df.shape[1]} columns\n")

    print("Converting proper columns to datetime and integer types...")
    for col in DT_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    print("Datetime conversion complete.\n")
    print("The following columns were converted to datetime:")
    for col in DT_COLS:
        if col in df.columns:
            print(f" - {col}")

    print("\nConverting proper columns to integer types...")
    for col in INT_COLS:
        if col in df.columns:
            df[col] = df[col].astype("Int64")
    print("Integer conversion complete.\n")
    print("The following columns were converted to integer:")
    for col in INT_COLS:
        if col in df.columns:
            print(f" - {col}")

    print("\nDropping duplicate and high missing columns...")
    actual_drops = []
    for col in COLS_TO_DROP:
        if col in df.columns:
            actual_drops.append(col)

    df = df.drop(columns=actual_drops, axis=1)
    print("The following columns were dropped:")
    for col in actual_drops:
        print(f" - {col}")

    print("\nDropping columns that are not useful for analysis...")
    df = df.drop(columns=NON_ANALYSIS_COLS, axis=1)
    print("The following columns were dropped:")
    for col in NON_ANALYSIS_COLS:
        if col in df.columns:
            print(f" - {col}")

    print("\nFlagging impossible measurement values...")
    print("The following columns were checked for negative values:")
    for col in NON_NEG_FLAG_COLS:
        if col in df.columns:
            print(f" - {col}")
    neg_check = df[NON_NEG_FLAG_COLS] < 0

    df["impossible_measurement_flag"] = neg_check.any(axis=1)

    print("\nFlagging impossible dates and timeline values...")
    print("Flagging YearBuilt for future dates...")
    df["impossible_year_flag"] = df["YearBuilt"] > 2026

    print("\nFlagging negative timeline values including...")
    print("ListingContractDate > CloseDate")
    print("PurchaseContractDate > CloseDate")
    print("ListingContractDate > PurchaseContractDate")

    df["listing_after_close_flag"] = df["ListingContractDate"] > df["CloseDate"]
    df["purchase_after_close_flag"] = df["PurchaseContractDate"] > df["CloseDate"]
    df["negative_timeline_flag"] = (
        df["ListingContractDate"] > df["PurchaseContractDate"]
    )

    print("\nFlagging impossible, placeholder, and non-california coordinates...")
    # lat and long checking
    df["null_coords_flag"] = df[["Latitude", "Longitude"]].isnull().any(axis=1)
    df["placeholder_coords_flag"] = (df["Latitude"] == 0) | (df["Longitude"] == 0)
    df["non_cali_coords_flag"] = (
        (df["Latitude"] > 32)
        & (df["Latitude"] < 42)
        & (df["Longitude"] > -124)
        & (df["Longitude"] < -114)
    )

    print("\nCleaning complete. Final info on dataset:\n")
    print(f"{df.shape[0]}", f"rows and {df.shape[1]} columns\n")
    print(f"\nSaving cleaned dataset to output path: {OUTPUT_PATH}...")
    df.to_csv(OUTPUT_PATH, index=False)
