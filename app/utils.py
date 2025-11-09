import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_country_data(country: str) -> pd.DataFrame:
    """Loads cleaned CSV for the selected country."""
    path = f"data/{country.lower().replace(' ', '_')}_clean.csv"
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        return pd.DataFrame()  # Return empty if file not found

def plot_boxplot(df: pd.DataFrame, metric: str):
    """Creates and returns a seaborn boxplot."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(y=df[metric], color='skyblue', ax=ax)
    ax.set_title(f'{metric} Distribution')
    ax.set_ylabel(metric)
    return fig
