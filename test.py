import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from pyecharts import options as opts
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts

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

def create_temperature_chart(df):
    """Membuat grafik line chart untuk suhu"""
    # Asumsi kolom timestamp ada di dataframe
    timestamps = df['timestamp'].tolist() if 'timestamp' in df.columns else df.index.astype(str).tolist()
    
    # Temukan semua kolom suhu
    temp_columns = [col for col in df.columns if 'suhu' in col.lower() or 'temp' in col.lower()]
    
    # Buat line chart
    line_chart = (
        Line()
        .add_xaxis(timestamps)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Trend Suhu"),
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
            xaxis_opts=opts.AxisOpts(name="Waktu"),
            yaxis_opts=opts.AxisOpts(
                name="Suhu (°C)",
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
    )
    
    # Tambahkan setiap kolom suhu sebagai series terpisah
    for col in temp_columns:
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
    
    return line_chart

try:
    df = pd.read_csv(spreadsheet_url)
    st.success("✅ Data berhasil dimuat dan auto-refresh tiap 10 detik.")
    
    # Tampilkan grafik di bagian atas
    st.header("📈 Visualisasi Grafik Suhu")
    chart = create_temperature_chart(df)
    st_pyecharts(chart, height="500px")
    
    # Tampilkan tabel data
    st.header("📄 Data Tabel")
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
