import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_histogram(df: pd.DataFrame, col: str, bins: int = 30, **kwargs):
    sns.histplot(data=df, x=col, bins=bins, **kwargs)
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()
