import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# VISUALIZATION FUNCTIONS


def get_histogram(
    df: pd.DataFrame,
    col: str | list[str],
    bins: int = 30,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = "Frequency",
    clip_lower: float | None = None,
    clip_upper: float | None = None,
    clip_quantile: float | None = None,
    ncols: int = 2,
    figsize: tuple[float, float] | None = None,
    **kwargs,
):
    """
    Function for making histogram :)
    Wraps seaborn histplot with clipping and labeling support.

    Parameters:
    - col: single column name or a list of column names.
    - ncols: number of columns in the subplot grid when plotting multiple columns.
    - figsize: optional figure size. If omitted for multi-column plotting, it is inferred from the grid size.
    """
    cols = [col] if isinstance(col, str) else col

    def _resolve_bound(bound, column_name: str):
        if bound is None:
            return None
        if isinstance(bound, dict):
            return bound.get(column_name)
        if isinstance(bound, pd.Series):
            return bound.get(column_name)
        return bound
    if not cols:
        raise ValueError("Provide at least one column name.")
    if ncols < 1:
        raise ValueError("ncols must be >= 1.")

    if clip_quantile is not None and not 0 < clip_quantile <= 1:
        raise ValueError("clip_quantile must be in (0, 1].")

    sns.set_style("whitegrid")

    if len(cols) == 1:
        series = pd.to_numeric(df[cols[0]], errors="coerce").dropna()
        local_clip_lower = _resolve_bound(clip_lower, cols[0])
        local_clip_upper = _resolve_bound(clip_upper, cols[0])
        if clip_quantile is not None:
            local_clip_upper = series.quantile(clip_quantile)
        if local_clip_lower is not None or local_clip_upper is not None:
            series = series.clip(lower=local_clip_lower, upper=local_clip_upper)

        plt.figure(figsize=figsize or (10, 6))
        sns.histplot(x=series, bins=bins, **kwargs)

        title_suffix = ""
        if clip_quantile is not None:
            title_suffix = f" (clipped at p{clip_quantile * 100:.1f})"
        elif clip_lower is not None or clip_upper is not None:
            title_suffix = " (clipped)"

        plt.title((title or f"Histogram of {cols[0]}") + title_suffix)
        plt.xlabel(xlabel or cols[0])
        plt.ylabel(ylabel or "Frequency")
        plt.show()
        return

    nrows = (len(cols) + ncols - 1) // ncols
    if figsize is None:
        figsize = (6 * ncols, 4 * nrows)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    title_suffix = ""
    if clip_quantile is not None:
        title_suffix = f" (clipped at p{clip_quantile * 100:.1f})"
    elif clip_lower is not None or clip_upper is not None:
        title_suffix = " (clipped)"

    for i, column in enumerate(cols):
        series = pd.to_numeric(df[column], errors="coerce").dropna()
        local_clip_lower = _resolve_bound(clip_lower, column)
        local_clip_upper = _resolve_bound(clip_upper, column)
        if clip_quantile is not None:
            local_clip_upper = series.quantile(clip_quantile)
        if local_clip_lower is not None or local_clip_upper is not None:
            series = series.clip(lower=local_clip_lower, upper=local_clip_upper)

        sns.histplot(x=series, bins=bins, ax=axes[i], **kwargs)
        axes[i].set_title(f"Histogram of {column}" + title_suffix)
        axes[i].set_xlabel(xlabel or column)
        axes[i].set_ylabel(ylabel or "Frequency")

    for j in range(len(cols), len(axes)):
        axes[j].set_visible(False)

    if title:
        fig.suptitle(title)
        fig.tight_layout(rect=(0, 0, 1, 0.97))
    else:
        fig.tight_layout()

    plt.show()


def get_boxplot(
    df: pd.DataFrame,
    col: str | list[str],
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = "Value",
    clip_lower: float | None = None,
    clip_upper: float | None = None,
    clip_quantile: float | None = None,
    ncols: int = 2,
    figsize: tuple[float, float] | None = None,
    **kwargs,
):
    """
    Function for making boxplot :)
    Wraps seaborn boxplot with clipping and labeling support.

    Parameters:
    - col: single column name or a list of column names.
    - ncols: number of columns in the subplot grid when plotting multiple columns.
    - figsize: optional figure size. If omitted for multi-column plotting, it is inferred from the grid size.
    """
    cols = [col] if isinstance(col, str) else col

    def _resolve_bound(bound, column_name: str):
        if bound is None:
            return None
        if isinstance(bound, dict):
            return bound.get(column_name)
        if isinstance(bound, pd.Series):
            return bound.get(column_name)
        return bound
    if not cols:
        raise ValueError("Provide at least one column name.")
    if ncols < 1:
        raise ValueError("ncols must be >= 1.")

    if clip_quantile is not None and not 0 < clip_quantile <= 1:
        raise ValueError("clip_quantile must be in (0, 1].")

    sns.set_style("whitegrid")

    if len(cols) == 1:
        series = pd.to_numeric(df[cols[0]], errors="coerce").dropna()
        local_clip_lower = _resolve_bound(clip_lower, cols[0])
        local_clip_upper = _resolve_bound(clip_upper, cols[0])
        if clip_quantile is not None:
            local_clip_upper = series.quantile(clip_quantile)
        if local_clip_lower is not None or local_clip_upper is not None:
            series = series.clip(lower=local_clip_lower, upper=local_clip_upper)

        plt.figure(figsize=figsize or (10, 6))
        sns.boxplot(x=series, **kwargs)

        title_suffix = ""
        if clip_quantile is not None:
            title_suffix = f" (clipped at p{clip_quantile * 100:.1f})"
        elif clip_lower is not None or clip_upper is not None:
            title_suffix = " (clipped)"

        plt.title((title or f"Boxplot of {cols[0]}") + title_suffix)
        plt.xlabel(xlabel or cols[0])
        plt.ylabel(ylabel or "Value")
        plt.show()
        return

    nrows = (len(cols) + ncols - 1) // ncols
    if figsize is None:
        figsize = (6 * ncols, 4 * nrows)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    title_suffix = ""
    if clip_quantile is not None:
        title_suffix = f" (clipped at p{clip_quantile * 100:.1f})"
    elif clip_lower is not None or clip_upper is not None:
        title_suffix = " (clipped)"

    for i, column in enumerate(cols):
        series = pd.to_numeric(df[column], errors="coerce").dropna()
        local_clip_lower = _resolve_bound(clip_lower, column)
        local_clip_upper = _resolve_bound(clip_upper, column)
        if clip_quantile is not None:
            local_clip_upper = series.quantile(clip_quantile)
        if local_clip_lower is not None or local_clip_upper is not None:
            series = series.clip(lower=local_clip_lower, upper=local_clip_upper)

        sns.boxplot(x=series, ax=axes[i], **kwargs)
        axes[i].set_title(f"Boxplot of {column}" + title_suffix)
        axes[i].set_xlabel(xlabel or column)
        axes[i].set_ylabel(ylabel or "Value")

    for j in range(len(cols), len(axes)):
        axes[j].set_visible(False)

    if title:
        fig.suptitle(title)
        fig.tight_layout(rect=(0, 0, 1, 0.97))
    else:
        fig.tight_layout()

    plt.show()


# MISSING / OUTLIER FUNCTIONS (EDA)


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

    print(f"Outlier Counts (Threshold: {threshold} * IQR)\n{'-'*40}")
    for col, count in outlier_counts.items():
        if count is not None:
            print(
                f"{col}: {count} outliers ({(count / len(df)) * 100:.2f}% of total records)"
            )
        else:
            print(f"{col}: Column not found in DataFrame")
    return outliers
