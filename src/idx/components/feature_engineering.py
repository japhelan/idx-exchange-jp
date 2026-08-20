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
import geopandas as gpd
from shapely.geometry import Point


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


def geo_merge(
    df, gdf, lon_col="Longitude", lat_col="Latitude", district_col="DistrictNa"
):
    """
    Merges a DataFrame with a GeoDataFrame based on geographic coordinates.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data to merge.
    gdf (gpd.GeoDataFrame): The GeoDataFrame containing the geographic data.
    lon_col (str): The name of the longitude column in df.
    lat_col (str): The name of the latitude column in df.
    district_col (str): The name of the district column in gdf.

    Returns:
    pd.DataFrame: A DataFrame with the merged data, including the district information.
    """

    # Create a GeoDataFrame from the input DataFrame
    df["geometry"] = df.apply(lambda row: Point(row[lon_col], row[lat_col]), axis=1)
    df_gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

    # Perform spatial join
    merged_gdf = gpd.sjoin(
        df_gdf, gdf[[district_col, "geometry"]], how="left", predicate="within"
    )

    # Drop the geometry column and return as a regular DataFrame
    merged_df = merged_gdf.drop(columns=["geometry"])

    return merged_df


class CreateMarketMetrics(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for creating market metrics from MLS data.
    Creates new features based on existing columns in the MLS data.
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        if self.verbose:
            print(
                f"Pre-feature engineering column count for sold_df and listings_df: {sold_df.shape[1]} and {listings_df.shape[1]}"
            )
        sold_df = feature_engineering(sold_df)
        listings_df = feature_engineering(listings_df)
        if self.verbose:
            print(
                f"Post-feature engineering column count for sold_df and listings_df: {sold_df.shape[1]} and {listings_df.shape[1]}"
            )

        return sold_df, listings_df


class CleanUpTransformer(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for cleaning up the data.
    Drops unnecessary columns and handles missing values.
    at some point just roll this into the other transformer for dropping
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        # Drop unnecessary columns
        drop_cols = [
            "TaxYear",
            "BuildingAreaTotal",
            "LotSizeDimensions",
            "StreetNumberNumeric",
            "MainLevelBedrooms",
        ]
        listings_df = listings_df.drop(columns=drop_cols, errors="ignore")
        sold_df = sold_df.drop(columns=drop_cols, errors="ignore")
        if self.verbose:
            print(
                f"Dropped columns: {drop_cols}. New shapes: sold_df: {sold_df.shape}, listings_df: {listings_df.shape}"
            )

        return sold_df, listings_df


class NullDropper(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for dropping rows with null values in specified columns.
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        if self.verbose:
            print(
                f"Dropping nulls from columns: ['Latitude', 'Longitude', 'OriginalListPrice', 'ClosePrice']. Pre-null drop shapes: sold_df: {sold_df.shape}, listings_df: {listings_df.shape}"
            )
        sold_df = sold_df.dropna(
            subset=["Latitude", "Longitude", "OriginalListPrice", "ClosePrice"]
        )
        listings_df = listings_df.dropna(
            subset=["Latitude", "Longitude", "OriginalListPrice"]
        )
        if self.verbose:
            print(
                f"Post-null drop shapes: sold_df: {sold_df.shape}, listings_df: {listings_df.shape}"
            )

        return sold_df, listings_df


class DistrictMerger(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for merging district information into the MLS data.
    Merges district information based on the county or parish of the property.
    """

    def __init__(self, district_gdf, verbose=True):
        self.verbose = verbose
        if district_gdf is None:
            district_gdf = gpd.read_file("../data/raw/district/DistrictAreas2425.shp")
        self.district_gdf = district_gdf.to_crs(epsg=4326)

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        if self.verbose:
            print(
                f"Merging geographic district information. Pre-merge shapes: sold_df: {sold_df.shape}, listings_df: {listings_df.shape}"
            )
        sold_df = geo_merge(
            sold_df, lon_col="Longitude", lat_col="Latitude", gdf=self.district_gdf
        )
        listings_df = geo_merge(
            listings_df, lon_col="Longitude", lat_col="Latitude", gdf=self.district_gdf
        )

        if self.verbose:
            print(
                f"Post-merge shapes: sold_df: {sold_df.shape}, listings_df: {listings_df.shape}"
            )
            print("\n")

        return sold_df, listings_df
