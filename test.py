import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd

# Data
df1 = pd.DataFrame({"Sensor": ["A1", "A2", "A3", "A4", "A5", "A6"], "Nilai": [23, 29, 25, 48, 30, 50]})
df2 = pd.DataFrame({"Sensor": ["B1", "B2", "B3"], "Nilai": [18, 21, 19]})
df3 = pd.DataFrame({"Sensor": ["C1", "C2", "C3"], "Nilai": [30, 27, 32]})
df4 = pd.DataFrame({"Sensor": ["D1", "D2", "D3"], "Nilai": [15, 13, 17]})

# Styling
st.markdown("<style>div.element-container { padding: 10px; }</style>", unsafe_allow_html=True)

# Title
st.title("📊 Dashboard Sensor Interaktif")

# ============ Grafik Atas ============
st.markdown("### Grafik Atas")
col1, col2 = st.columns(2)

with col1:
    option1 = {
        "title": {"text": "Data 1"},
        "tooltip": {},
        "xAxis": {"data": df1["Sensor"].tolist()},
        "yAxis": {},
        "series": [{
            "type": "bar",
            "data": df1["Nilai"].tolist(),
            "itemStyle": {"color": "#5470C6"}
        }]
    }
    st_echarts(options=option1, height="300px", width="100%")

with col2:
    option2 = {
        "title": {"text": "Data 2"},
        "tooltip": {},
        "xAxis": {"data": df2["Sensor"].tolist()},
        "yAxis": {},
        "series": [{
            "type": "bar",
            "data": df2["Nilai"].tolist(),
            "itemStyle": {"color": "#91CC75"}
        }]
    }
    st_echarts(options=option2, height="300px", width="100%")

# ============ Grafik Bawah ============
st.markdown("### Grafik Bawah")
col3, col4 = st.columns(2)

with col3:
    option3 = {
        "title": {"text": "Data 3"},
        "tooltip": {},
        "xAxis": {"data": df3["Sensor"].tolist()},
        "yAxis": {},
        "series": [{
            "type": "bar",
            "data": df3["Nilai"].tolist(),
            "itemStyle": {"color": "#FAC858"}
        }]
    }
    st_echarts(options=option3, height="300px", width="100%")

with col4:
    option4 = {
        "title": {"text": "Data 4"},
        "tooltip": {},
        "xAxis": {"data": df4["Sensor"].tolist()},
        "yAxis": {},
        "series": [{
            "type": "bar",
            "data": df4["Nilai"].tolist(),
            "itemStyle": {"color": "#EE6666"}
        }]
    }
    st_echarts(options=option4, height="300px", width="100%")
