# app/utils.py
import pandas as pd
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Auto-detect project root and data directory
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


FILES = {
    "Benin": DATA_DIR / "benin_data_cleaned.csv",
    "Sierra Leone": DATA_DIR / "sierra-leone_data_cleaned.csv",
    "Togo": DATA_DIR / "togo_data_cleaned.csv"
}

RAD_COLS = ['GHI', 'DNI', 'DHI']

#Load & Combine All Data 
def load_all_data() -> pd.DataFrame:
    dfs = []
    for country, path in FILES.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing data file: {path}")
        df = pd.read_csv(path)
        df["Country"] = country
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    for col in RAD_COLS:
        if col in combined.columns:
            combined[col] = pd.to_numeric(combined[col], errors='coerce')
    return combined

# Filter by Countries 
def filter_by_countries(df: pd.DataFrame, countries: List[str]) -> pd.DataFrame:
    return df[df["Country"].isin(countries)].copy()

# Mean Comparison Bar Chart
def plot_mean_comparison(df: pd.DataFrame, metric: str = 'GHI') -> plt.Figure:
    """
    Bar chart: Mean of selected metric (GHI, DNI, or DHI) per country.
    """
    if metric not in ['GHI', 'DNI', 'DHI']:
        raise ValueError("metric must be GHI, DNI, or DHI")
    
    # Calculate mean for selected metric
    means = df.groupby("Country")[metric].mean().round(1)
    means = means.reindex(['Benin', 'Togo', 'Sierra Leone'])  # Fixed order
    
    # Color map
    colors = {
        'GHI': '#e74c3c',
        'DNI': '#f39c12',
        'DHI': '#3498db'
    }
    
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(means.index, means.values, color=colors[metric], alpha=0.9)
    
    ax.set_xlabel("Country", fontsize=12)
    ax.set_ylabel(f"Mean {metric} (W/m²)", fontsize=12)
    ax.set_title(f"Average {metric} by Country", fontweight='bold', fontsize=14)
    ax.grid(True, axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 8,
                f'{h}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    return fig

# Summary Statistics 
def get_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.groupby("Country")[RAD_COLS].agg(['mean', 'median', 'std']).round(2)
    stats.columns = pd.MultiIndex.from_tuples(
        [(col[0].upper(), col[1].capitalize()) for col in stats.columns]
    )
    stats = stats.sort_values(('GHI', 'Mean'), ascending=False)
    return stats


# Interactive Daily Profile Plot
def plot_daily_profile_multi(df: pd.DataFrame) -> plt.Figure:

    df = df.copy()
    
    # === Extract Hour ===
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df['Hour'] = df['Timestamp'].dt.hour
    elif 'hour' in df.columns:
        df['Hour'] = df['hour'].astype(int)
    else:
        raise ValueError("Need 'Timestamp' or 'hour' column for daily profile.")
    
    df = df.dropna(subset=['Hour', 'GHI', 'DNI', 'DHI'])
    
    # === Melt to long format: metric, value, country, hour ===
    melted = df.melt(
        id_vars=['Country', 'Hour'],
        value_vars=['GHI', 'DNI', 'DHI'],
        var_name='Metric',
        value_name='Value'
    )
    
    # === Compute mean per country, hour, metric ===
    daily = melted.groupby(['Country', 'Hour', 'Metric'])['Value'].mean().reset_index()
    
    # === Plot ===
    fig, ax = plt.subplots(figsize=(11, 6))
    
    colors = {'GHI': '#e74c3c', 'DNI': '#f39c12', 'DHI': '#3498db'}
    markers = {'GHI': 'o', 'DNI': 's', 'DHI': '^'}
    
    for country in daily['Country'].unique():
        country_data = daily[daily['Country'] == country]
        for metric in ['GHI', 'DNI', 'DHI']:
            data = country_data[country_data['Metric'] == metric]
            ax.plot(
                data['Hour'], data['Value'],
                label=f"{country} – {metric}",
                color=colors[metric],
                marker=markers[metric],
                linewidth=2.2,
                markersize=4,
                alpha=0.9
            )
    
    ax.set_title("Average Daily Solar Profile (GHI, DNI, DHI)", fontweight='bold', fontsize=15)
    ax.set_xlabel("Hour of Day (Local Time)", fontsize=12)
    ax.set_ylabel("Irradiance (W/m²)", fontsize=12)
    ax.set_xticks(range(0, 24, 2))
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.tight_layout()
    
    return fig


