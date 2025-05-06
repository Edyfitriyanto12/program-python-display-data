import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from pyecharts import options as opts
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts
from datetime import datetime

# Konfigurasi halaman untuk mobile friendly
st.set_page_config(
    page_title="Data dari Google Sheet",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Deteksi perangkat mobile (pendekatan sederhana)
user_agent = st.experimental_get_query_params().get("user_agent", [""])[0]
is_mobile = "mobi" in user_agent.lower()

# CSS Custom dengan fitur responsif
st.markdown(f"""
<style>
    /* Gaya dasar untuk semua perangkat */
    .chart-title {{
        color: #ffffff !important;
        font-weight: bold !important;
    }}
    
    .x-axis-label, .y-axis-label {{
        fill: #ffffff !important;
    }}
    
    .legend-text {{
        fill: #ffffff !important;
    }}
    
    .tooltip {{
        color: #333333 !important;
        background-color: #ffffff !important;
    }}
    
    .highlight-example {{
        background-color: rgba(100, 149, 237, 0.6);
        padding: 5px;
        border-radius: 3px;
        font-weight: bold;
    }}
    
    /* Responsive design untuk mobile */
    @media screen and (max-width: 768px) {{
        /* Penyesuaian ukuran grafik */
        .st-echarts {{
            width: 100% !important;
            height: {300 if is_mobile else 500}px !important;
        }}
        
        /* Tabel scroll horizontal */
        .stDataFrame {{
            overflow-x: auto;
            display: block;
            width: 100%;
            font-size: 12px;
        }}
        
        /* Padding lebih kecil */
        .main .block-container {{
            padding: 1rem;
        }}
        
        /* Ukuran teks lebih kecil */
        h1 {{
            font-size: 1.5rem !important;
        }}
        
        h2 {{
            font-size: 1.2rem !important;
        }}
        
        /* Layout footer vertikal */
        .footer-container {{
            flex-direction: column;
            padding: 20px 10px;
        }}
        
        .footer-column {{
            flex: 1 1 100%;
            margin-bottom: 20px;
            padding: 10px 0;
        }}
        
        .social-icons {{
            justify-content: center;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Auto-refresh tiap 15 detik
st_autorefresh(interval=15 * 1000, key="auto_refresh")

st.title("📊 Monitoring Real-time Pengering Cerdas")

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

def to_float_safe(val):
    """Mengonversi string dengan koma ke float. Contoh: '66,55' → 66.55"""
    try:
        if isinstance(val, str):
            val = val.replace(',', '.')
        return float(val)
    except (ValueError, TypeError):
        return None

def create_temperature_chart(df):
    """Membuat grafik line chart untuk suhu dan output fuzzy"""
    
    # Cari kolom timestamp (case insensitive)
    timestamp_cols = [col for col in df.columns if 'timestamp' in col.lower()]
    if not timestamp_cols:
        st.error("Kolom timestamp tidak ditemukan!")
        return None
        
    timestamp_col = timestamp_cols[0]
    
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
    
    # Buat line chart dengan tema dark
    line_chart = (
        Line(init_opts=opts.InitOpts(theme="dark"))
        .add_xaxis(timestamps)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Nilai Parameter Suhu",
                title_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF", font_weight="bold")
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                background_color="#FFFFFF",
                border_color="#333333",
                textstyle_opts=opts.TextStyleOpts(color="#333333")
            ),
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")
            ),
            xaxis_opts=opts.AxisOpts(
                name="Timestamp",
                axislabel_opts=opts.LabelOpts(
                    rotate=45,
                    color="#FFFFFF"
                ),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#FFFFFF")
                )
            ),
            yaxis_opts=opts.AxisOpts(
                name="Suhu (°C) dan Output Fuzzy",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(color="#FFFFFF"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#FFFFFF")
                )
            ),
            toolbox_opts=opts.ToolboxOpts(
                feature={
                    "saveAsImage": {},
                    "dataView": {},
                    "restore": {},
                    "dataZoom": {},
                    "magicType": {"show": True, "type": ["line", "bar"]},
                }
            ),
            datazoom_opts=[opts.DataZoomOpts()]
        )
    )
    
    # Tambahkan series untuk suhu
    for col in temp_columns:
        if col != timestamp_col:
            df[col] = df[col].apply(to_float_safe)
            
            line_chart.add_yaxis(
                series_name=col,
                y_axis=df[col].round(1).tolist(),
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
        df[col] = df[col].apply(to_float_safe)
        
        line_chart.add_yaxis(
            series_name=col,
            y_axis=df[col].round(1).tolist(),
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

def create_energy_chart(df):
    """Membuat grafik line chart untuk parameter energi (tegangan, ampere, frekuensi)"""
    if 'parsed_timestamp' not in df.columns:
        timestamp_cols = [col for col in df.columns if 'timestamp' in col.lower()]
        if not timestamp_cols:
            st.error("Kolom timestamp tidak ditemukan dalam data!")
            return None
        
        df['parsed_timestamp'] = df[timestamp_cols[0]].apply(parse_timestamp)
        df = df.dropna(subset=['parsed_timestamp'])
    
    if df.empty:
        st.error("Tidak ada data dengan timestamp valid!")
        return None
    
    df = df.sort_values('parsed_timestamp')
    timestamps = df['parsed_timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    
    for col in df.columns:
        df[col] = df[col].apply(to_float_safe)
    
    voltage_columns = [col for col in df.columns if 'volt' in col.lower() or 'tegangan' in col.lower()]
    current_columns = [col for col in df.columns if 'ampere' in col.lower() or 'current' in col.lower()]
    freq_columns = [col for col in df.columns if 'frekuensi' in col.lower() or 'freq' in col.lower()]
    
    line_chart = (
        Line(init_opts=opts.InitOpts(theme="dark"))
        .add_xaxis(timestamps)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Data Parameter Energi",
                title_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF", font_weight="bold")
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                background_color="#FFFFFF",
                border_color="#333333",
                textstyle_opts=opts.TextStyleOpts(color="#333333")
            ),
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")
            ),
            xaxis_opts=opts.AxisOpts(
                name="Timestamp",
                axislabel_opts=opts.LabelOpts(
                    rotate=45,
                    color="#FFFFFF"
                ),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#FFFFFF")
                )
            ),
            yaxis_opts=opts.AxisOpts(
                name="Nilai Parameter",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(color="#FFFFFF"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#FFFFFF")
                )
            ),
            toolbox_opts=opts.ToolboxOpts(
                feature={
                    "saveAsImage": {},
                    "dataView": {},
                    "restore": {},
                    "dataZoom": {},
                    "magicType": {"show": True, "type": ["line", "bar"]},
                }
            ),
            datazoom_opts=[opts.DataZoomOpts()]
        )
    )
    
    for col in voltage_columns:
        line_chart.add_yaxis(
            series_name=col,
            y_axis=df[col].tolist(),
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color="#1E90FF"),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Max"),
                    opts.MarkPointItem(type_="min", name="Min"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="Rata-rata")]
            ),
        )
    
    for col in current_columns:
        line_chart.add_yaxis(
            series_name=col,
            y_axis=df[col].tolist(),
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color="#32CD32"),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Max"),
                    opts.MarkPointItem(type_="min", name="Min"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="Rata-rata")]
            ),
        )
    
    for col in freq_columns:
        line_chart.add_yaxis(
            series_name=col,
            y_axis=df[col].tolist(),
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color="#FF6347"),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Max"),
                    opts.MarkPointItem(type_="min", name="Min"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="Rata-rata")]
            ),
        )
    
    return line_chart

try:
    df = pd.read_csv(spreadsheet_url)
    st.success("✅ Data berhasil dimuat dan auto-refresh tiap 15 detik.")
    
    # Tampilkan grafik suhu
    with st.container():
        st.header("📈 Visualisasi Grafik Suhu dan Output Fuzzy")
        temp_chart = create_temperature_chart(df)
        if temp_chart:
            st_pyecharts(temp_chart, height=300 if is_mobile else 500, theme="dark")
    
    # Tampilkan grafik energi
    with st.container():
        st.header("⚡ Visualisasi Grafik Parameter Energi")
        energy_chart = create_energy_chart(df)
        if energy_chart:
            st_pyecharts(energy_chart, height=300 if is_mobile else 500, theme="dark")
    
    # Tampilkan tabel data
    df_display = df.drop(columns=["parsed_timestamp"], errors="ignore")

    st.header("📄 Data Tabel")
    styled_df = df_display.style \
        .apply(highlight_temp, axis=1) \
        .format(precision=1)
    st.dataframe(
        styled_df, 
        use_container_width=True,
        height=300 if is_mobile else None
    )

    st.markdown("""
    <p>Baris dengan <span class="highlight-example">warna biru transparan</span> menunjukkan terdapat suhu antara 60-70°C pada salah satu sensor</p>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat mengambil data: {e}")

# Footer responsif
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    .footer-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        background-color: #2C3E50;
        color: #ffffff;
        font-family: Arial, sans-serif;
        padding: 40px 20px 20px 20px;
    }

    .footer-column {
        flex: 1 1 30%;
        min-width: 200px;
        padding: 10px 20px;
        box-sizing: border-box;
    }

    .footer-title {
        color: #ffffff;
        margin-bottom: 20px;
        font-size: 16px;
        font-weight: bold;
    }

    .footer-text {
        color: #bdc3c7;
        font-size: 14px;
        line-height: 1.5;
    }

    .social-icons {
        display: flex;
        gap: 15px;
        align-items: center;
    }

    .social-icons a {
        color: #ffffff;
        background-color: #1abc9c;
        border-radius: 50%;
        padding: 10px;
        font-size: 16px;
        text-align: center;
        text-decoration: none;
        transition: background-color 0.3s;
    }

    .social-icons a:hover {
        background-color: #16a085;
    }

    .copyright {
        background-color: #233140;
        text-align: center;
        color: #bdc3c7;
        padding: 15px 0;
        font-size: 13px;
    }
    
    /* Responsive footer */
    @media screen and (max-width: 768px) {
        .footer-container {
            flex-direction: column;
            padding: 20px 10px;
        }
        
        .footer-column {
            flex: 1 1 100%;
            margin-bottom: 20px;
            padding: 10px 0;
        }
        
        .social-icons {
            justify-content: center;
        }
    }
</style>

<div class="footer-container">
    <div class="footer-column">
        <h3 class="footer-title">LOCATION</h3>
        <p class="footer-text">Bruno, Purworejo, Central Java (54261)</p>
    </div>
    <div class="footer-column">
        <h3 class="footer-title">AROUND THE WEB</h3>
        <div class="social-icons">
            <a href="https://www.instagram.com/edy_ftrynto/" target="_blank"><i class="fab fa-instagram"></i></a>
            <a href="https://wa.me/082324403671"><i class="fas fa-phone"></i></a> 
            <a href="https://www.linkedin.com/in/edy-fitriyanto-12163622a/" target="_blank"><i class="fab fa-linkedin-in"></i></a>
        </div>
    </div>
    <div class="footer-column">
        <h3 class="footer-title">ABOUT DELTAUSER</h3>
        <p class="footer-text">DeltaUser is a content creator focused on delivering educational resources in programming, IoT, and modern web technologies.</p>
    </div>
</div>

<div class="copyright">
    © 2023 DeltaUser. All rights reserved.
</div>
""", unsafe_allow_html=True)
