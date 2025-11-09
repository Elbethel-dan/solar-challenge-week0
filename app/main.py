import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from app.utils import load_country_data, plot_boxplot

# ------------------------------
# 🌞 App Configuration
# ------------------------------
st.set_page_config(page_title="Solar Data Dashboard", layout="wide")

st.title("☀️ Solar Energy Insights Dashboard")
st.markdown("Visualize and compare solar irradiance metrics across countries.")

# ------------------------------
# 🌍 Country Selector
# ------------------------------
countries = ["Benin", "Sierra Leone", "Togo"]
selected_country = st.selectbox("Select a country:", countries)

df = load_country_data(selected_country)

if df.empty:
    st.warning(f"No data found for **{selected_country}**. Please check your data folder.")
    st.stop()

# ------------------------------
# 📊 Metric Selector
# ------------------------------
metric = st.selectbox("Select a metric to visualize:", ["GHI", "DNI", "DHI", "Tamb", "RH", "WS", "WSgust"])

# ------------------------------
# 📦 Boxplot
# ------------------------------
st.subheader(f"Boxplot of {metric} for {selected_country}")
fig = plot_boxplot(df, metric)
st.pyplot(fig)

# ------------------------------
# 🏆 Top Regions Table
# ------------------------------
if "Station" in df.columns:
    st.subheader(f"Top 5 Regions in {selected_country} by Average {metric}")
    top_regions = (
        df.groupby("Station")[metric].mean().sort_values(ascending=False).head(5)
    )
    st.dataframe(top_regions)
else:
    st.info("No 'Station' column found — skipping regional breakdown.")

# ------------------------------
# 📈 Optional: Trend over Time
# ------------------------------
if "Timestamp" in df.columns:
    st.subheader(f"Time Series of {metric} Over Time")
    fig2, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x="Timestamp", y=metric, data=df, ax=ax, color="orange")
    plt.xticks(rotation=45)
    st.pyplot(fig2)
else:
    st.info("No timestamp column found — skipping time series plot.")

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.caption("Developed for the Solar Challenge Week 0 🌍 | Streamlit Dashboard Demo")
