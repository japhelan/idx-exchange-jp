"""pipeline components for data cleaning"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from pathlib import Path

# helper functions


def iqr_outlier_flag(df, subset, multiplier=1.5, remove=False):
    if isinstance(subset, list):
        for col in subset:
            df = iqr_outlier_flag(df, subset=col, multiplier=multiplier, remove=remove)
        return df
    else:
        Q1 = df[subset].quantile(0.25)
        Q3 = df[subset].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - multiplier * IQR
        upper = Q3 + multiplier * IQR
        if remove:
            df = df[(df[subset] >= lower) & (df[subset] <= upper)]
        else:
            df["outlier_flag"] = (df[subset] < lower) | (df[subset] > upper)
        return df


class OutlierFlagger(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for flagging outliers in a specified column of a DataFrame.
    """

    def __init__(self, subset, multiplier=1.5, remove=False, verbose=True):
        self.verbose = verbose
        if subset is None:
            raise ValueError("subset parameter must be provided")
        self.subset = subset
        self.multiplier = multiplier
        self.remove = remove

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        if self.verbose:
            print(
                f"Flagging IQR outliers (range={self.multiplier}*IQR) in columns: {self.subset}. Pre-flag shapes: sold_df: {sold_df.shape}, listings_df: {listings_df.shape}"
            )
        sold_df = iqr_outlier_flag(
            sold_df, subset=self.subset, multiplier=self.multiplier, remove=self.remove
        )
        listings_df = iqr_outlier_flag(
            listings_df,
            subset=self.subset,
            multiplier=self.multiplier,
            remove=self.remove,
        )
        if self.verbose:
            print(
                f"Flagged IQR outliers (range={self.multiplier}*IQR) in columns: {self.subset}. Post-flag shapes: sold_df: {sold_df.shape}, listings_df: {listings_df.shape}"
            )
            print("\n")

        return sold_df, listings_df


class OutlierRemover(BaseEstimator, TransformerMixin):
    """
    Custom sklearn pipeline component for removing outliers in a specified column of a DataFrame.
    """

    def __init__(self, subset, multiplier=1.5, verbose=True):
        self.verbose = verbose
        if subset is None:
            raise ValueError("subset parameter must be provided")
        self.subset = subset
        self.multiplier = multiplier

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        sold_df, listings_df = X
        if self.verbose:
            print(
                f"Removing IQR outliers (range={self.multiplier}*IQR) in columns: {self.subset}. Pre-remove shapes: sold_df: {sold_df.shape}, listings_df: {listings_df.shape}"
            )
        sold_df = iqr_outlier_flag(
            sold_df, subset=self.subset, multiplier=self.multiplier, remove=True
        )
        listings_df = iqr_outlier_flag(
            listings_df, subset=self.subset, multiplier=self.multiplier, remove=True
        )
        if self.verbose:
            print(
                f"Removed IQR outliers (range={self.multiplier}*IQR) in columns: {self.subset}. Post-remove shapes: sold_df: {sold_df.shape}, listings_df: {listings_df.shape}"
            )
            print("\n")

        return sold_df, listings_df
