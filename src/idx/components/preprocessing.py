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

    def __init__(self):
        pass

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X

        sold_drops = [col for col in COLS_TO_DROP if col in sold_df.columns]
        listings_drops = [col for col in COLS_TO_DROP if col in listings_df.columns]

        sold_df = sold_df.drop(columns=sold_drops)
        listings_df = listings_df.drop(columns=listings_drops)
        for df in [sold_df, listings_df]:
            for col in DT_COLS:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
            for col in INT_COLS:
                if col in df.columns:
                    df[col] = df[col].astype("Int64")
        sold_df = sold_df.drop(
            columns=[col for col in NON_ANALYSIS_COLS if col in sold_df.columns]
        )
        listings_df = listings_df.drop(
            columns=[col for col in NON_ANALYSIS_COLS if col in listings_df.columns]
        )
        return sold_df, listings_df


def flagging(df):
    # creates all flag columns for the dataframe
    df = df.copy()
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
    df["non_cali_coords_flag"] = (
        (df["Latitude"] > 32)
        & (df["Latitude"] < 42)
        & (df["Longitude"] > -124)
        & (df["Longitude"] < -114)
    )
    return df


class BadDataFlagger(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for flagging bad data in MLS data.
    Flags rows with negative values in specified columns.
    """

    def __init__(self):
        pass

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        sold_df = flagging(sold_df)
        listings_df = flagging(listings_df)
        return sold_df, listings_df
