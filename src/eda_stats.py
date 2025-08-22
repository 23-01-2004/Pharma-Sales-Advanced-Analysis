import pandas as pd
import matplotlib.pyplot as plt

def summary_statistics(df):
    """Return summary statistics of the dataset"""
    return pd.DataFrame(df.describe())

def plot_numerical_distributions(df):
    """Plot histograms for all numerical features"""
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    if len(num_cols) == 0:
        return None
    
    fig = df[num_cols].hist(
        bins=30,
        figsize=(15, 10),
        color='lightblue'
    )
    plt.suptitle("Numerical Distributions")
    plt.grid()
    plt.tight_layout()
    return plt
