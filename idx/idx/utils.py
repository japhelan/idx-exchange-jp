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
