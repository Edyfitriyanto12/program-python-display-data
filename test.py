import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Auto refresh tiap 10 detik
st_autorefresh(interval=10 * 1000, key="auto_refresh")

st.set_page_config(page_title="Data dari Google Sheet", layout="wide")

st.title("📄 Data dari Google Spreadsheet (Realtime)")

# URL CSV dari spreadsheet kamu
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aFLGmvdviHrPQyKeFcD1jdZU9A3g_RJEMP8X_iMCA7s/export?format=csv"

try:
    df = pd.read_csv(spreadsheet_url,skiprows=2)
    st.success("✅ Data berhasil dimuat dan auto-refresh tiap 10 detik.")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat mengambil data: {e}")
