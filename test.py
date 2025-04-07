import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# HARUS PALING ATAS setelah import
st.set_page_config(page_title="Data dari Google Sheet", layout="wide")

# Auto-refresh tiap 10 detik
st_autorefresh(interval=10 * 1000, key="auto_refresh")

st.title("📄 Data dari Google Spreadsheet (Realtime)")

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aFLGmvdviHrPQyKeFcD1jdZU9A3g_RJEMP8X_iMCA7s/export?format=csv"

try:
    df = pd.read_csv(spreadsheet_url)
    st.success("✅ Data berhasil dimuat dan auto-refresh tiap 10 detik.")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat mengambil data: {e}")
