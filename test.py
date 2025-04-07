import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# HARUS PALING ATAS setelah import
st.set_page_config(page_title="Data dari Google Sheet", layout="wide")

# Auto-refresh tiap 10 detik
st_autorefresh(interval=10 * 1000, key="auto_refresh")

st.title("📄 Data dari Google Spreadsheet (Realtime)")

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aFLGmvdviHrPQyKeFcD1jdZU9A3g_RJEMP8X_iMCA7s/export?format=csv"

def highlight_temp(row):
    """Fungsi untuk memberikan warna pada baris dengan suhu antara 60-70°C"""
    style = []
    for col in row.index:
        # Jika kolom berisi suhu (asumsi nama kolom mengandung 'suhu' atau 'temp')
        if 'suhu' in col.lower() or 'temp' in col.lower():
            try:
                temp = float(row[col])
                if 60 <= temp <= 70:
                    style.append('background-color: #FFA07A; font-weight: bold;')
                    continue
            except (ValueError, TypeError):
                pass
        style.append('')
    return style

try:
    df = pd.read_csv(spreadsheet_url)
    st.success("✅ Data berhasil dimuat dan auto-refresh tiap 10 detik.")
    
    # Terapkan styling
    styled_df = df.style.apply(highlight_temp, axis=1)
    
    # Tampilkan dataframe dengan styling
    st.dataframe(styled_df, use_container_width=True)
    
    # Tambahkan penjelasan
    st.markdown("""
    <style>
        .highlight-example {
            background-color: #FFA07A;
            padding: 5px;
            border-radius: 3px;
            font-weight: bold;
        }
    </style>
    <p>Baris dengan <span class="highlight-example">warna oranye</span> menunjukkan suhu antara 60-70°C</p>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat mengambil data: {e}")
