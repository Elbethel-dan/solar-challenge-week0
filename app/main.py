# app/main.py
import streamlit as st
from utils import (
    load_all_data, plot_mean_comparison, get_summary_stats,
    plot_daily_profile_multi, filter_by_countries
)

st.markdown(
    """
    <style>
    .stAppHeader {
    background-color: #fff3e7; !important;}
    
    .stApp { background-color: #fff3e7; }
    
    .stApp *, .stMarkdown, h1, h2, h3, h4, h5, h6, label, p, span, div {
    color: black !important;
    font-weight: 500 !important;
    }
    [data-testid="stSidebar"] { 
    background-color: #cdb09e !important;   
    }
    </style>
    """,
    unsafe_allow_html=True
)

# === Page Config ===
st.set_page_config(page_title="West Africa Solar Dashboard", layout="wide")
st.title("☀️ West Africa Solar Potential Dashboard")
st.markdown("Interactive comparison of **Benin, Sierra Leone, and Togo** using cleaned radiation data.")

# === Load Data ===
@st.cache_data
def get_data():
    return load_all_data()

try:
    df = get_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

# === Sidebar Filters ===
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=["Benin", "Sierra Leone", "Togo"],
    default=["Benin", "Sierra Leone", "Togo"]
)

metric = st.sidebar.selectbox("Select Metric", options=['GHI', 'DNI', 'DHI'], index=0)
df_filtered = filter_by_countries(df, selected_countries)

st.subheader("Average GHI, DNI, and DHI by Country")
fig = plot_mean_comparison(df_filtered, metric=metric)
st.pyplot(fig)



# === Summary Table (Below Boxplot, Full Width) ===
st.subheader("Summary Statistics")
summary = get_summary_stats(df_filtered)
st.markdown("<br>", unsafe_allow_html=True)
st.dataframe(summary.style.highlight_max(axis=0, color='#ffcccc'))



st.subheader("Average Daily Solar Profile (GHI, DNI, DHI)")
try:
    fig = plot_daily_profile_multi(df_filtered)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"Daily profile failed: {e}")
    st.info("Check: 'Timestamp' or 'hour' column + valid GHI/DNI/DHI")


# === Footer ===
st.caption("Data: ENERGY DATA | Cleaned & Analyzed | Dashboard: Streamlit")