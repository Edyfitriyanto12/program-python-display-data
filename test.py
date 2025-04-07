import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd

# Dummy data
data1 = {"Sensor": ["A1", "A2", "A3"], "Nilai": [23, 29, 25]}
data2 = {"Sensor": ["B1", "B2", "B3"], "Nilai": [18, 21, 19]}
data3 = {"Sensor": ["C1", "C2", "C3"], "Nilai": [30, 27, 32]}
data4 = {"Sensor": ["D1", "D2", "D3"], "Nilai": [15, 13, 17]}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)

# Judul Dashboard
st.title("📊 Dashboard Sensor dengan ECharts")

# Baris 1: Dua grafik
st.subheader("Grafik Atas")
col1, col2 = st.columns(2)

with col1:
    option1 = {
        "title": {"text": "Data 1"},
        "tooltip": {},
        "xAxis": {"data": df1["Sensor"].tolist()},
        "yAxis": {},
        "series": [{
            "name": "Nilai",
            "type": "bar",
            "data": df1["Nilai"].tolist(),
            "itemStyle": {"color": "#3BA272"}
        }]
    }
    st_echarts(options=option1, height="300px")

with col2:
    option2 = {
        "title": {"text": "Data 2"},
        "tooltip": {},
        "xAxis": {"data": df2["Sensor"].tolist()},
        "yAxis": {},
        "series": [{
            "name": "Nilai",
            "type": "bar",
            "data": df2["Nilai"].tolist(),
            "itemStyle": {"color": "#FC8452"}
        }]
    }
    st_echarts(options=option2, height="300px")

# Baris 2: Dua grafik
st.subheader("Grafik Bawah")
col3, col4 = st.columns(2)

with col3:
    option3 = {
        "title": {"text": "Data 3"},
        "tooltip": {},
        "xAxis": {"data": df3["Sensor"].tolist()},
        "yAxis": {},
        "series": [{
            "name": "Nilai",
            "type": "bar",
            "data": df3["Nilai"].tolist(),
            "itemStyle": {"color": "#9A60B4"}
        }]
    }
    st_echarts(options=option3, height="300px")

with col4:
    option4 = {
        "title": {"text": "Data 4"},
        "tooltip": {},
        "xAxis": {"data": df4["Sensor"].tolist()},
        "yAxis": {},
        "series": [{
            "name": "Nilai",
            "type": "bar",
            "data": df4["Nilai"].tolist(),
            "itemStyle": {"color": "#73C0DE"}
        }]
    }
    st_echarts(options=option4, height="300px")

# Gabungkan data semua
st.subheader("📋 Tabel Gabungan")
df_all = pd.concat([
    df1.assign(Grafik="Data 1"),
    df2.assign(Grafik="Data 2"),
    df3.assign(Grafik="Data 3"),
    df4.assign(Grafik="Data 4"),
], ignore_index=True)

st.dataframe(df_all)

# Grafik gabungan semua data
st.subheader("📈 Grafik Gabungan Semua Data")
grouped = df_all.groupby("Grafik")
option_all = {
    "title": {"text": "Gabungan Semua Data"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": list(grouped.groups.keys())},
    "xAxis": {"type": "category", "data": df_all["Sensor"].tolist()},
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": name,
            "type": "line",
            "data": group["Nilai"].tolist()
        }
        for name, group in grouped
    ]
}
st_echarts(options=option_all, height="400px")

