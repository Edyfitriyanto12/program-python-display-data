import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data dari Google Sheet", layout="wide")

st.title("📄 Data dari Google Spreadsheet")

# URL CSV dari Spreadsheet kamu
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aFLGmvdviHrPQyKeFcD1jdZU9A3g_RJEMP8X_iMCA7s/export?format=csv"

try:
    # Ambil data dari spreadsheet
    df = pd.read_csv(spreadsheet_url)

    st.success("✅ Data berhasil dimuat!")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat mengambil data: {e}")
