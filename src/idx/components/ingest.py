"""
Custom sklearn pipeline component for ingesting MLS data and helper functions
"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from pathlib import Path
import os
import ssl
import urllib.request
import certifi


def read_mls_dir(input_dir: Path, filter: str) -> pd.DataFrame:
    """
    Reads all CSV files in the specified directory and concatenates them into a single DataFrame.
    Args:
        input_dir (Path): The directory containing the CSV files.
        filter (str): A string to filter the files by name. If None, all CSV files will be read.
    Returns:
        pd.DataFrame: A DataFrame containing the concatenated data from all the CSV files.
    """

    df_list = []
    for file in input_dir.iterdir():
        if file.suffix == ".csv":
            if filter is None or filter in file.name:
                temp_df = pd.read_csv(file, low_memory=False)
                temp_df["source_file"] = (
                    file.name
                )  # Add a new column with the source file name
                df_list.append(temp_df)
    print(f"Read {len(df_list)} files from {input_dir} with filter '{filter}'")
    print("\n")

    return pd.concat(df_list, ignore_index=True)


class MLSIngestor(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for ingesting MLS scripts.
    Reads both sold and listings data from the specified input directory and concatenates them into a single DataFrame.
    """

    def __init__(self, input_path: str):
        self.input_path = input_path

    def fit(self, X=None, y=None):
        return self

    def transform(self, X=None):
        df_sold = read_mls_dir(Path(self.input_path), "Sold")
        df_listings = read_mls_dir(Path(self.input_path), "Listing")
        X = df_sold, df_listings
        return X


class FredMerger(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for merging FRED data with MLS data.
    Merges the FRED data with the MLS data on the specified date column.
    """

    def __init__(self):
        # reading mortgage data in to be used in transform
        self.context = ssl.create_default_context(cafile=certifi.where())
        self.mortgage_cols = ["date", "rate_30yr_fixed"]
        URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
        with urllib.request.urlopen(URL, context=self.context) as response:
            mortgage = pd.read_csv(response, parse_dates=["observation_date"])
        mortgage.columns = self.mortgage_cols
        self.fred_data = mortgage
        mortgage["year_month"] = mortgage["date"].dt.to_period("M")
        self.mortgage_monthly = (
            mortgage.groupby("year_month")["rate_30yr_fixed"].mean().reset_index()
        )

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        sold_df["year_month"] = pd.to_datetime(sold_df["CloseDate"]).dt.to_period("M")
        listings_df["year_month"] = pd.to_datetime(
            listings_df["ListingContractDate"]
        ).dt.to_period("M")
        sold_with_rates = sold_df.merge(
            self.mortgage_monthly, on="year_month", how="left"
        )
        listings_with_rates = listings_df.merge(
            self.mortgage_monthly, on="year_month", how="left"
        )
        print(f"Merged FRED data with sold data: {sold_with_rates.shape[0]} rows")
        print(
            f"Merged FRED data with listings data: {listings_with_rates.shape[0]} rows"
        )
        print("\n")
        return sold_with_rates, listings_with_rates
