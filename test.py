import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from pyecharts import options as opts
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts
from datetime import datetime

# HARUS PALING ATAS setelah import
st.set_page_config(page_title="Data dari Google Sheet", layout="wide")

# Auto-refresh tiap 10 detik
st_autorefresh(interval=10 * 1000, key="auto_refresh")

st.title("📊 Monitoring Suhu Real-time")

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aFLGmvdviHrPQyKeFcD1jdZU9A3g_RJEMP8X_iMCA7s/export?format=csv"

def highlight_temp(row):
    """Fungsi untuk memberikan warna biru transparan pada seluruh baris jika suhu antara 60-70°C"""
    highlight = False
    for col in row.index:
        if 'suhu' in col.lower() or 'temp' in col.lower():
            try:
                temp = float(row[col])
                if 60 <= temp <= 70:
                    highlight = True
                    break
            except (ValueError, TypeError):
                pass
    
    if highlight:
        return ['background-color: rgba(100, 149, 237, 0.6); font-weight: bold;'] * len(row)
    else:
        return [''] * len(row)

def parse_timestamp(timestamp_str):
    """Fungsi untuk mengkonversi string timestamp ke format datetime yang seragam"""
    try:
        # Coba format dengan AM/PM
        if isinstance(timestamp_str, str):
            if 'AM' in timestamp_str or 'PM' in timestamp_str:
                return datetime.strptime(timestamp_str, '%m/%d/%Y, %I:%M:%S %p')
            # Coba format 24 jam
            else:
                return datetime.strptime(timestamp_str, '%m/%d/%Y, %H:%M:%S')
        elif isinstance(timestamp_str, datetime):
            return timestamp_str
        elif pd.notnull(timestamp_str):
            return pd.to_datetime(timestamp_str)
    except ValueError as e:
        st.warning(f"Gagal parsing timestamp: {timestamp_str}. Error: {e}")
        return None

def create_temperature_chart(df):
    """Membuat grafik line chart untuk suhu dan output fuzzy"""
    # Cari kolom timestamp (case insensitive)
    timestamp_cols = [col for col in df.columns if 'timestamp' in col.lower()]
    
    if not timestamp_cols:
        st.error("Kolom timestamp tidak ditemukan dalam data!")
        st.warning(f"Kolom yang tersedia: {list(df.columns)}")
        return None
    
    timestamp_col = timestamp_cols[0]  # Ambil kolom pertama yang mengandung 'timestamp'
    
    # Konversi timestamp ke format datetime
    df['parsed_timestamp'] = df[timestamp_col].apply(parse_timestamp)
    
    # Drop baris dengan timestamp tidak valid
    df = df.dropna(subset=['parsed_timestamp'])
    
    if df.empty:
        st.error("Tidak ada data dengan timestamp valid!")
        return None
    
    # Urutkan berdasarkan timestamp
    df = df.sort_values('parsed_timestamp')
    
    # Format timestamp untuk display di grafik
    timestamps = df['parsed_timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    
    # Temukan semua kolom suhu
    temp_columns = [col for col in df.columns if 'suhu' in col.lower() or 'temp' in col.lower()]
    
    # Temukan kolom output fuzzy
    fuzzy_columns = [col for col in df.columns if 'fuzzy' in col.lower() or 'output' in col.lower()]
    
    # Buat line chart
    line_chart = (
        Line()
        .add_xaxis(timestamps)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Trend Suhu dan Output Fuzzy"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(
                feature={
                    "saveAsImage": {},
                    "dataView": {},
                    "restore": {},
                    "dataZoom": {},
                    "magicType": {"show": True, "type": ["line", "bar"]},
                }
            ),
            xaxis_opts=opts.AxisOpts(
                name="Timestamp",
                axislabel_opts=opts.LabelOpts(rotate=45)),
            yaxis_opts=opts.AxisOpts(
                name="Suhu (°C) dan Output Fuzzy",
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            datazoom_opts=[opts.DataZoomOpts()]
        )
    )
    
    # Tambahkan series untuk suhu
    for col in temp_columns:
        if col != timestamp_col:  # Hindari memplot kolom timestamp sebagai suhu
            line_chart.add_yaxis(
                series_name=col,
                y_axis=df[col].tolist(),
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="Max"),
                        opts.MarkPointItem(type_="min", name="Min"),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[
                        opts.MarkLineItem(type_="average", name="Average"),
                        opts.MarkLineItem(y=60, name="Batas Bawah"),
                        opts.MarkLineItem(y=70, name="Batas Atas"),
                    ]
                ),
            )
    
    # Tambahkan series untuk output fuzzy
    for col in fuzzy_columns:
        line_chart.add_yaxis(
            series_name=col,
            y_axis=df[col].tolist(),
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=3, type_="dashed"),
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color="#FF6347"),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Max"),
                    opts.MarkPointItem(type_="min", name="Min"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="Average")]
            ),
        )
    
    return line_chart

try:
    df = pd.read_csv(spreadsheet_url)
    st.success("✅ Data berhasil dimuat dan auto-refresh tiap 10 detik.")
    
    # Tampilkan kolom yang tersedia untuk debugging
    st.write(f"Kolom yang tersedia: {list(df.columns)}")
    
    # Tampilkan grafik
    st.header("📈 Visualisasi Grafik Suhu")
    chart = create_temperature_chart(df)
    if chart:
        st_pyecharts(chart, height="500px")
    
    # Tampilkan tabel data
    st.header("📄 Data Tabel")
    # df_display = df.drop(columns=[timestamp_col])  # atau ['Timestamp']
    styled_df = df.style.apply(highlight_temp, axis=1)
    st.dataframe(styled_df, use_container_width=True)
    
    # Tambahkan penjelasan
    st.markdown("""
    <style>
        .highlight-example {
            background-color: rgba(100, 149, 237, 0.6);
            padding: 5px;
            border-radius: 3px;
            font-weight: bold;
        }
    </style>
    <p>Baris dengan <span class="highlight-example">warna biru transparan</span> menunjukkan terdapat suhu antara 60-70°C pada salah satu sensor</p>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat mengambil data: {e}")

