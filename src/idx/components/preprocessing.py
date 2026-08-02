"""
sklearn transformers for preprocessing functions
"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from pathlib import Path
from idx.config import (
    COLS_TO_DROP,
    DT_COLS,
    INT_COLS,
    NON_PREDICTIVE_COLS,
    NON_ANALYSIS_COLS,
    NON_NEG_FLAG_COLS,
)
import os
import ssl
import urllib.request
import certifi


class DataCleaner(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for cleaning MLS data.
    Drops specified columns and converts specified columns to datetime and integer types.
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X

        if self.verbose:
            print(f"Original sold_df shape: {sold_df.shape}")
            print(f"Original listings_df shape: {listings_df.shape}")
        sold_drops = [col for col in COLS_TO_DROP if col in sold_df.columns]
        listings_drops = [col for col in COLS_TO_DROP if col in listings_df.columns]

        sold_df = sold_df.drop(columns=sold_drops)
        listings_df = listings_df.drop(columns=listings_drops)
        if self.verbose:
            print(f"Post-drop sold_df shape: {sold_df.shape}")
            print(f"Post-drop listings_df shape: {listings_df.shape}")
        for df in [sold_df, listings_df]:
            for col in DT_COLS:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
            for col in INT_COLS:
                if col in df.columns:
                    df[col] = df[col].astype("Int64")
        if self.verbose:
            print(
                f"{len(DT_COLS)} datetime columns converted and {len(INT_COLS)} integer columns converted."
            )
        sold_df = sold_df.drop(
            columns=[col for col in NON_ANALYSIS_COLS if col in sold_df.columns]
        )
        listings_df = listings_df.drop(
            columns=[col for col in NON_ANALYSIS_COLS if col in listings_df.columns]
        )
        if self.verbose:
            print(
                f"Dropped {len(NON_ANALYSIS_COLS)} non-analysis columns from sold_df and listings_df."
            )
        return sold_df, listings_df


def flagging(df, verbose=True):
    # creates all flag columns for the dataframe
    df = df.copy()

    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

    neg_check = df[NON_NEG_FLAG_COLS] < 0
    df["impossible_measurement_flag"] = neg_check.any(axis=1)
    df["impossible_year_flag"] = df["YearBuilt"] > 2026
    df["listing_after_close_flag"] = df["ListingContractDate"] > df["CloseDate"]
    df["purchase_after_close_flag"] = df["PurchaseContractDate"] > df["CloseDate"]
    df["negative_timeline_flag"] = (
        df["ListingContractDate"] > df["PurchaseContractDate"]
    )
    df["null_coords_flag"] = df[["Latitude", "Longitude"]].isnull().any(axis=1)
    df["placeholder_coords_flag"] = (df["Latitude"] == 0) | (df["Longitude"] == 0)
    in_cali = df["Latitude"].between(32, 42, inclusive="both") & df[
        "Longitude"
    ].between(-124, -114, inclusive="both")
    df["non_cali_coords_flag"] = (~in_cali) & (~df["null_coords_flag"])
    # print
    if verbose:
        print(
            f"Flagged {df['impossible_measurement_flag'].sum()} rows with impossible measurements."
        )
        print(f"Flagged {df['impossible_year_flag'].sum()} rows with impossible year.")
        print(
            f"Flagged {df['listing_after_close_flag'].sum()} rows with listing after close."
        )
        print(
            f"Flagged {df['purchase_after_close_flag'].sum()} rows with purchase after close."
        )
        print(
            f"Flagged {df['negative_timeline_flag'].sum()} rows with negative timeline."
        )
        print(f"Flagged {df['null_coords_flag'].sum()} rows with null coordinates.")
        print(
            f"Flagged {df['placeholder_coords_flag'].sum()} rows with placeholder coordinates."
        )
        print(
            f"Flagged {df['non_cali_coords_flag'].sum()} rows with non-California coordinates."
        )

    return df


class BadDataFlagger(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for flagging bad data in MLS data.
    Flags rows with negative values in specified columns.
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        sold_df = flagging(sold_df, verbose=self.verbose)
        listings_df = flagging(listings_df, verbose=self.verbose)
        print("\n")

        return sold_df, listings_df
