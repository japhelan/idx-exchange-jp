import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_histogram(
    df: pd.DataFrame,
    col: str,
    bins: int = 30,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = "Frequency",
    clip_lower: float | None = None,
    clip_upper: float | None = None,
    clip_quantile: float | None = None,
    **kwargs,
):
    """
    Function for making histogram :)
    """
    series = pd.to_numeric(df[col], errors="coerce").dropna()

    if clip_quantile is not None:
        if not 0 < clip_quantile <= 1:
            raise ValueError("clip_quantile must be in (0, 1].")
        clip_upper = series.quantile(clip_quantile)

    if clip_lower is not None or clip_upper is not None:
        series = series.clip(lower=clip_lower, upper=clip_upper)

    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(x=series, bins=bins, **kwargs)
    title_suffix = ""
    if clip_quantile is not None:
        title_suffix = f" (clipped at p{clip_quantile * 100:.1f})"
    elif clip_lower is not None or clip_upper is not None:
        title_suffix = " (clipped)"
    plt.title((title or f"Histogram of {col}") + title_suffix)
    plt.xlabel(xlabel or col)
    plt.ylabel(ylabel or "Frequency")
    plt.show()


def get_boxplot(
    df: pd.DataFrame,
    col: str,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = "Value",
    clip_lower: float | None = None,
    clip_upper: float | None = None,
    clip_quantile: float | None = None,
    **kwargs,
):
    """
    Function for making boxplot :)
    """
    series = pd.to_numeric(df[col], errors="coerce").dropna()

    if clip_quantile is not None:
        if not 0 < clip_quantile <= 1:
            raise ValueError("clip_quantile must be in (0, 1].")
        clip_upper = series.quantile(clip_quantile)

    if clip_lower is not None or clip_upper is not None:
        series = series.clip(lower=clip_lower, upper=clip_upper)

    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=series, **kwargs)
    title_suffix = ""
    if clip_quantile is not None:
        title_suffix = f" (clipped at p{clip_quantile * 100:.1f})"
    elif clip_lower is not None or clip_upper is not None:
        title_suffix = " (clipped)"
    plt.title((title or f"Boxplot of {col}") + title_suffix)
    plt.xlabel(xlabel or col)
    plt.ylabel(ylabel or "Value")
    plt.show()


def get_missing_report(df, index_col=None, flag_high_missing=False, threshold=0.9):
    """
    Returns a DataFrame with the count and percentage of missing values for each column in the input DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame to analyze.
    index_col (str, optional): The column to set as the index of the returned DataFrame. Defaults to None.
    flag_high_missing (bool, optional): Whether to flag columns with high missing values. Defaults to False.
    threshold (float, optional): The threshold for flagging high missing values. Defaults to 0.9.

    Returns:
    pd.DataFrame: A DataFrame containing the count and percentage of missing values for each column.
    """
    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100
    missing_report = pd.DataFrame(
        {
            "column": df.columns,
            "missing_count": missing_count,
            "pct_missing": missing_percentage,
        }
    )
    if index_col:
        missing_report.set_index(index_col, inplace=True)
    else:
        missing_report.reset_index(drop=True, inplace=True)
    if flag_high_missing:
        missing_report["high_missing"] = missing_report["pct_missing"] > (
            threshold * 100
        )
    return missing_report.sort_values(by="missing_count", ascending=False)


def get_iqr_outliers(df, cols, threshold=1.5, **kwargs):
    """
    Returns a DataFrame with the count of outliers for each specified column in the input DataFrame based on the IQR method.

    Parameters:
    df (pd.DataFrame): The input DataFrame to analyze.
    cols (list): A list of column names to check for outliers.
    threshold (float, optional): The multiplier for the IQR to define outliers. Defaults to 1.5.

    Returns:
    pd.DataFrame: A DataFrame containing the count of outliers for each specified column.
    """
    outlier_counts = {}
    outliers = pd.DataFrame()  # Initialize an empty DataFrame to store outliers
    for col in cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - (threshold * IQR)
            upper_bound = Q3 + (threshold * IQR)
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_counts[col] = len(outliers)

        else:
            outlier_counts[col] = None  # Column not found

    print(f"Outlier Counts\n{'-'*40}")
    for col, count in outlier_counts.items():
        if count is not None:
            print(
                f"{col}: {count} outliers ({(count / len(df)) * 100:.2f}% of total records)"
            )
        else:
            print(f"{col}: Column not found in DataFrame")
    return outliers
