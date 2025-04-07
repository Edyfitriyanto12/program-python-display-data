import streamlit as st
from tabulate import tabulate

# Judul Aplikasi
st.title("📊 Visualisasi Data Sensor")

# Data sensor contoh (bisa diganti dengan data real)
data_sensor = [
    {"Sensor": "Sensor 1", "Suhu": 25.5, "Kelembaban": 60, "Tekanan": 1013, "Kualitas Udara": "Baik"},
    {"Sensor": "Sensor 2", "Suhu": 26.0, "Kelembaban": 58, "Tekanan": 1012, "Kualitas Udara": "Baik"},
    {"Sensor": "Sensor 3", "Suhu": 24.8, "Kelembaban": 62, "Tekanan": 1014, "Kualitas Udara": "Sedang"},
    {"Sensor": "Sensor 4", "Suhu": 27.2, "Kelembaban": 55, "Tekanan": 1011, "Kualitas Udara": "Baik"}
]

# Tampilkan data per sensor
st.header("📌 Data Sensor Individual")
for data in data_sensor:
    st.subheader(f"{data['Sensor']}")
    
    # Format tabel untuk setiap sensor
    table_data = [
        ["Parameter", "Nilai"],
        ["Suhu (°C)", data["Suhu"]],
        ["Kelembaban (%)", data["Kelembaban"]],
        ["Tekanan (hPa)", data["Tekanan"]],
        ["Kualitas Udara", data["Kualitas Udara"]]
    ]
    
    st.markdown(
        tabulate(table_data, headers="firstrow", tablefmt="github"),
        unsafe_allow_html=True
    )
    st.divider()

# Tampilkan gabungan semua data
st.header("📊 Gabungan Data Semua Sensor")
# Format data untuk tabel gabungan
headers = ["Sensor", "Suhu (°C)", "Kelembaban (%)", "Tekanan (hPa)", "Kualitas Udara"]
rows = []
for data in data_sensor:
    rows.append([
        data["Sensor"],
        data["Suhu"],
        data["Kelembaban"],
        data["Tekanan"],
        data["Kualitas Udara"]
    ])

# Tampilkan tabel gabungan
st.markdown(
    tabulate(rows, headers=headers, tablefmt="github"),
    unsafe_allow_html=True
)
