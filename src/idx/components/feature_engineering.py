"""
feature engineering components
"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from pathlib import Path
from idx.config import DATA_DIR, RAW_LISTINGS_DIR, RAW_SOLD_DIR
import os
import ssl
import urllib.request
import certifi


# fe helper functions
def make_price_ratio(df):
    df = df.copy()
    df["price_ratio"] = df["ClosePrice"] / df["OriginalListPrice"]
    return df


def make_price_per_sqft(df):
    df = df.copy()
    df["price_per_sqft"] = df["ClosePrice"] / df["LivingArea"]
    return df


def make_days_on_market(df):
    df = df.copy()
    df["days_on_market"] = (
        pd.to_datetime(df["CloseDate"]) - pd.to_datetime(df["ListingContractDate"])
    ).dt.days
    return df


def make_yr_month(df):
    df = df.copy()
    df["yr_month"] = pd.to_datetime(df["CloseDate"]).dt.to_period("M")
    return df


def make_listing_to_contract_days(df):
    df = df.copy()
    df["listing_to_contract_days"] = (
        pd.to_datetime(df["PurchaseContractDate"])
        - pd.to_datetime(df["ListingContractDate"])
    ).dt.days
    return df


def make_contract_to_close_days(df):
    df = df.copy()
    df["contract_to_close_days"] = (
        pd.to_datetime(df["CloseDate"]) - pd.to_datetime(df["PurchaseContractDate"])
    ).dt.days
    return df


# call func for all
def feature_engineering(df):
    # Example feature engineering steps
    df = make_price_ratio(df)
    df = make_price_per_sqft(df)
    df = make_days_on_market(df)
    df = make_yr_month(df)
    df = make_listing_to_contract_days(df)
    df = make_contract_to_close_days(df)

    return df


class CreateMarketMetrics(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for creating market metrics from MLS data.
    Creates new features based on existing columns in the MLS data.
    """

    def __init__(self):
        pass

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        sold_df = feature_engineering(sold_df)
        listings_df = feature_engineering(listings_df)
        return sold_df, listings_df
