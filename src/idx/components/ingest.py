"""
Custom sklearn pipeline component for ingesting MLS data
"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from pathlib import Path
from idx.config import DATA_DIR, RAW_LISTINGS_DIR, RAW_SOLD_DIR
import os


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
                df_list.append(pd.read_csv(file, low_memory=False))
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
        return df_sold, df_listings
