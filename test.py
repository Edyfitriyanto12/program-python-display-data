import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from pyecharts import options as opts
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts
from datetime import datetime

# HARUS PALING ATAS setelah import
st.set_page_config(
    page_title="Monitoring Real-time Pengering Cerdas", 
    layout="wide",
    page_icon="🌡️"
)

# ===========================================
# CSS CUSTOM UNTUK SEMUA KOMPONEN
# ===========================================
st.markdown("""
<style>
    /* [DARK MODE ADAPTIVE STYLES] */
    :root {
        --primary-text: #31333F;
        --secondary-text: #6C757D;
        --bg-color: #FFFFFF;
        --card-bg: #F8F9FA;
        --border-color: #DEE2E6;
    }
    
    [data-theme="dark"] {
        --primary-text: #F0F2F6;
        --secondary-text: #ADB5BD;
        --bg-color: #0E1117;
        --card-bg: #1E1E1E;
        --border-color: #444444;
    }
    
    /* [UMUM] */
    .stApp {
        background-color: var(--bg-color);
    }
    
    /* [HEADER] */
    .header-title {
        color: var(--primary-text);
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 10px;
    }
    
    /* [TABEL] */
    .dataframe {
        border: 1px solid var(--border-color) !important;
    }
    
    /* [FOOTER] */
    .footer {
        background-color: var(--card-bg);
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border-color);
    }
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
    }
    .footer-col-title {
        color: var(--primary-text);
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
    .footer-col-text {
        color: var(--secondary-text);
        line-height: 1.6;
        font-size: 0.9rem;
    }
    .footer-copyright {
        text-align: center;
        margin-top: 2rem;
        color: var(--secondary-text);
        font-size: 0.8rem;
    }
    
    /* [TOOLTIP GRAFIK] */
    .tooltip {
        color: #333333 !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# Auto-refresh tiap 15 detik
st_autorefresh(interval=15 * 1000, key="auto_refresh")

# ===========================================
# FUNGSI UTAMA
# ===========================================
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aFLGmvdviHrPQyKeFcD1jdZU9A3g_RJEMP8X_iMCA7s/export?format=csv"

def highlight_temp(row):
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
    try:
        if isinstance(timestamp_str, str):
            if 'AM' in timestamp_str or 'PM' in timestamp_str:
                return datetime.strptime(timestamp_str, '%m/%d/%Y, %I:%M:%S %p')
            else:
                return datetime.strptime(timestamp_str, '%m/%d/%Y, %H:%M:%S')
        elif isinstance(timestamp_str, datetime):
            return timestamp_str
        elif pd.notnull(timestamp_str):
            return pd.to_datetime(timestamp_str)
    except ValueError as e:
        st.warning(f"Gagal parsing timestamp: {timestamp_str}. Error: {e}")
        return None

def create_chart(df, title, y_axis_name, series_config):
    """Fungsi universal untuk membuat grafik"""
    df['parsed_timestamp'] = df['timestamp'].apply(parse_timestamp)
    df = df.dropna(subset=['parsed_timestamp']).sort_values('parsed_timestamp')
    
    if df.empty:
        st.error("Tidak ada data dengan timestamp valid!")
        return None
    
    timestamps = df['parsed_timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    
    line_chart = (
        Line(init_opts=opts.InitOpts(theme="dark" if st._config.get_option("theme.base") == "dark" else "light"))
        .add_xaxis(timestamps)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                title_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF" if st._config.get_option("theme.base") == "dark" else "#333333")
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                background_color="#FFFFFF",
                border_color="#333333",
                textstyle_opts=opts.TextStyleOpts(color="#333333")
            ),
            xaxis_opts=opts.AxisOpts(
                name="Waktu",
                axislabel_opts=opts.LabelOpts(rotate=45, color="#FFFFFF" if st._config.get_option("theme.base") == "dark" else "#333333"),
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF" if st._config.get_option("theme.base") == "dark" else "#333333"))
            ),
            yaxis_opts=opts.AxisOpts(
                name=y_axis_name,
                axislabel_opts=opts.LabelOpts(color="#FFFFFF" if st._config.get_option("theme.base") == "dark" else "#333333"),
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF" if st._config.get_option("theme.base") == "dark" else "#333333"))
            ),
            datazoom_opts=[opts.DataZoomOpts()]
        )
    )
    
    for config in series_config:
        line_chart.add_yaxis(**config)
    
    return line_chart

# ===========================================
# TAMPILAN UTAMA
# ===========================================
st.title("🌡️ Monitoring Real-time Pengering Cerdas")

try:
    df = pd.read_csv(spreadsheet_url)
    st.success("✅ Data berhasil dimuat. Pembaruan otomatis setiap 15 detik.")
    
    # Grafik Suhu
    with st.container():
        st.header("📊 Grafik Suhu dan Output Fuzzy")
        temp_chart = create_chart(
            df,
            "Trend Suhu dan Output Fuzzy",
            "Nilai (°C)",
            [
                {
                    "series_name": col,
                    "y_axis": df[col].tolist(),
                    "is_smooth": True,
                    "label_opts": opts.LabelOpts(is_show=False),
                    "itemstyle_opts": opts.ItemStyleOpts(color="#FF6347"),
                    "markline_opts": opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")])
                } for col in df.columns if 'suhu' in col.lower() or 'temp' in col.lower()
            ] + [
                {
                    "series_name": col,
                    "y_axis": df[col].tolist(),
                    "is_smooth": True,
                    "linestyle_opts": opts.LineStyleOpts(width=3, type_="dashed"),
                    "label_opts": opts.LabelOpts(is_show=False),
                    "itemstyle_opts": opts.ItemStyleOpts(color="#1E90FF"),
                } for col in df.columns if 'fuzzy' in col.lower() or 'output' in col.lower()
            ]
        )
        if temp_chart:
            st_pyecharts(temp_chart, height=500)

    # Grafik Energi
    with st.container():
        st.header("⚡ Grafik Parameter Energi")
        energy_chart = create_chart(
            df,
            "Trend Parameter Energi",
            "Nilai",
            [
                {
                    "series_name": col,
                    "y_axis": df[col].tolist(),
                    "is_smooth": True,
                    "label_opts": opts.LabelOpts(is_show=False),
                    "itemstyle_opts": opts.ItemStyleOpts(color=color),
                    "markline_opts": opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")])
                } 
                for col, color in zip(
                    [c for c in df.columns if any(x in c.lower() for x in ['volt', 'ampere', 'frekuensi'])],
                    ["#FFA500", "#32CD32", "#9370DB"]
                )
            ]
        )
        if energy_chart:
            st_pyecharts(energy_chart, height=500)

    # Tabel Data
    with st.container():
        st.header("📋 Data Terkini")
        df_display = df.drop(columns=["parsed_timestamp"], errors="ignore")
        st.dataframe(
            df_display.style.apply(highlight_temp, axis=1).format(precision=2),
            use_container_width=True,
            height=400
        )
        st.caption("Baris berwarna biru menunjukkan suhu dalam range 60-70°C")

    # FOOTER
    st.markdown("""
    <div class="footer">
        <div class="footer-grid">
            <div>
                <div class="footer-col-title">Tentang Sistem</div>
                <div class="footer-col-text">
                    Sistem monitoring real-time untuk pengering cerdas berbasis IoT. 
                    Memantau parameter suhu, kelembaban, dan konsumsi energi.
                </div>
            </div>
            <div>
                <div class="footer-col-title">Kontak</div>
                <div class="footer-col-text">
                    Lab. Sistem Cerdas<br>
                    Universitas Contoh<br>
                    Jl. Teknologi No. 123<br>
                    contact@contoh.ac.id
                </div>
            </div>
            <div>
                <div class="footer-col-title">Dikembangkan Oleh</div>
                <div class="footer-col-text">
                    Tim Pengering Cerdas 2023<br>
                    Advisor: Dr. Insinyur Contoh<br>
                    Versi Sistem: 2.1.0
                </div>
            </div>
        </div>
        <div class="footer-copyright">
            © 2023 Sistem Pengering Cerdas | All Rights Reserved
        </div>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Gagal memuat data: {str(e)}")
    st.error("Pastikan koneksi internet stabil dan URL spreadsheet benar.")
