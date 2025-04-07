import streamlit as st
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Scatter
from streamlit_echarts import st_pyecharts

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Monitoring", layout="wide")
st_autorefresh(interval=10 * 1000, key="auto_refresh")

st.title("📊 Dashboard Monitoring Komprehensif")

# URL spreadsheet (ganti dengan URL Anda)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aFLGmvdviHrPQyKeFcD1jdZU9A3g_RJEMP8X_iMCA7s/export?format=csv"

def load_data():
    try:
        df = pd.read_csv(spreadsheet_url)
        # Konversi kolom timestamp jika ada
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

def create_comprehensive_chart(df):
    if df.empty:
        return None
    
    # Persiapan data
    timestamps = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist() if 'timestamp' in df.columns else df.index.astype(str).tolist()
    
    # Buat tab untuk multi-grafik
    tab = st.tabs(["Grafik Garis", "Grafik Batang", "Scatter Plot"])
    
    with tab[0]:
        # Line Chart untuk semua data numerik
        line_chart = (
            Line()
            .add_xaxis(timestamps)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Trend Semua Parameter (Garis)"),
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
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="right"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            )
        )
        
        # Tambahkan semua kolom numerik
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            line_chart.add_yaxis(
                series_name=col,
                y_axis=df[col].round(2).tolist(),
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(width=2),
            )
        
        st_pyecharts(line_chart, height="600px")

    with tab[1]:
        # Bar Chart untuk perbandingan
        bar_chart = (
            Bar()
            .add_xaxis(timestamps)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Perbandingan Parameter (Batang)"),
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
            )
        )
        
        # Tambahkan 5 parameter pertama untuk menghindari overcrowding
        for col in numeric_cols[:5]:
            bar_chart.add_yaxis(
                series_name=col,
                y_axis=df[col].round(2).tolist(),
                label_opts=opts.LabelOpts(is_show=False),
            )
        
        st_pyecharts(bar_chart, height="600px")

    with tab[2]:
        # Scatter Plot untuk korelasi
        if len(numeric_cols) >= 2:
            scatter = (
                Scatter()
                .add_xaxis(df[numeric_cols[0]].round(2).tolist())
                .add_yaxis(
                    series_name=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                    y_axis=df[numeric_cols[1]].round(2).tolist(),
                    symbol_size=10,
                    label_opts=opts.LabelOpts(is_show=False),
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="Scatter Plot Korelasi Parameter"),
                    xaxis_opts=opts.AxisOpts(name=numeric_cols[0]),
                    yaxis_opts=opts.AxisOpts(name=numeric_cols[1]),
                    toolbox_opts=opts.ToolboxOpts(
                        feature={
                            "saveAsImage": {},
                            "dataView": {},
                            "restore": {},
                        }
                    ),
                )
            )
            st_pyecharts(scatter, height="500px")

def main():
    df = load_data()
    
    if not df.empty:
        # Tampilkan grafik komprehensif
        st.header("Visualisasi Data Lengkap")
        create_comprehensive_chart(df)
        
        # Tampilkan tabel data
        st.header("Data Mentah")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Statistik ringkas
        st.header("Statistik Deskriptif")
        st.dataframe(df.describe(), use_container_width=True)

if __name__ == "__main__":
    main()
