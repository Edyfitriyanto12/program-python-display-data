import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

st.set_page_config(page_title="Data dari Google Sheet", layout="wide")

# Auto refresh tiap 10 detik
st_autorefresh(interval=10 * 1000, key="auto_refresh")

st.title("🌡️ Monitoring Suhu dari Google Spreadsheet (Realtime)")

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aFLGmvdviHrPQyKeFcD1jdZU9A3g_RJEMP8X_iMCA7s/export?format=csv"

try:
    df = pd.read_csv(spreadsheet_url)

    # Konversi kolom waktu ke datetime
    df['waktu'] = pd.to_datetime(df['Timestamp'], errors='coerce')  # pastikan kolom namanya 'waktu'
    df['suhu'] = pd.to_numeric(df['suhu'], errors='coerce')

    # Ambil waktu sekarang dan 5 menit ke belakang
    now = datetime.now()
    five_minutes_ago = now - timedelta(minutes=5)

    # Tandai baris dengan suhu antara 60-70 dalam 5 menit terakhir
    def highlight_row(row):
        if pd.isna(row['waktu']) or pd.isna(row['suhu']):
            return [''] * len(row)
        if five_minutes_ago <= row['waktu'] <= now and 60 <= row['suhu'] <= 70:
            return ['background-color: orange'] * len(row)
        return [''] * len(row)

    styled_df = df.style.apply(highlight_row, axis=1)

    st.success("✅ Data berhasil dimuat dan ditandai berdasarkan suhu.")
    st.dataframe(styled_df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat mengambil data: {e}")
