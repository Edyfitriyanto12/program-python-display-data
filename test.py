import streamlit as st
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
from pyecharts import options as opts
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Monitoring", layout="wide")
st_autorefresh(interval=10 * 1000, key="auto_refresh")

st.title("📊 Dashboard Monitoring dengan Tampilan Waktu Miring")

def load_data():
    try:
        df = pd.read_csv("https://docs.google.com/spreadsheets/d/1aFLGmvdviHrPQyKeFcD1jdZU9A3g_RJEMP8X_iMCA7s/export?format=csv")
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

def create_chart_with_rotated_labels(df):
    if df.empty:
        return None
    
    # Format timestamp
    timestamps = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist()
    
    chart = (
        Line()
        .add_xaxis(timestamps)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Trend Parameter dengan Label Waktu Miring"),
            xaxis_opts=opts.AxisOpts(
                name="Waktu",
                axislabel_opts=opts.LabelOpts(
                    rotate=45,  # Miringkan label 45 derajat
                    font_size=10,
                    margin=20,  # Jarak antara label dan sumbu
                    interval=0,  # Tampilkan semua label
                    formatter="{value}"  # Format tampilan
                ),
                boundary_gap=True,  # Jarak antara label dan garis sumbu
                splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                name="Nilai Parameter",
                splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(
                feature={
                    "saveAsImage": {},
                    "dataView": {},
                    "restore": {},
                    "dataZoom": {},
                    "magicType": {"show": True, "type": ["line", "bar"]},
                }
            ),
            legend_opts=opts.LegendOpts(pos_right="right", pos_top="middle", orient="vertical")
        )
    )
    
    # Tambahkan parameter numerik
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols[:5]:  # Batasi 5 parameter agar tidak terlalu padat
        chart.add_yaxis(
            series_name=col,
            y_axis=df[col].round(2).tolist(),
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
    
    return chart

def main():
    df = load_data()
    
    if not df.empty:
        st.header("Visualisasi Data dengan Label Waktu Miring")
        
        # Tampilkan grafik dengan label miring
        chart = create_chart_with_rotated_labels(df)
        if chart:
            st_pyecharts(chart, height="600px")
        
        # Tampilkan tabel data
        st.header("Data Mentah")
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
