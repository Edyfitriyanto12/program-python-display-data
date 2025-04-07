import streamlit as st
import matplotlib.pyplot as plt
from tabulate import tabulate
import pandas as pd

# Judul Aplikasi
st.title("📊 Dashboard Data Sensor")

# Data sensor contoh (bisa diganti dengan data real)
data_sensor = [
    {"Sensor": "Sensor 1", "Suhu": 25.5, "Kelembaban": 60, "Tekanan": 1013, "Kualitas Udara": "Baik"},
    {"Sensor": "Sensor 2", "Suhu": 26.0, "Kelembaban": 58, "Tekanan": 1012, "Kualitas Udara": "Baik"},
    {"Sensor": "Sensor 3", "Suhu": 24.8, "Kelembaban": 62, "Tekanan": 1014, "Kualitas Udara": "Sedang"},
    {"Sensor": "Sensor 4", "Suhu": 27.2, "Kelembaban": 55, "Tekanan": 1011, "Kualitas Udara": "Baik"}
]

# Konversi ke DataFrame untuk grafik
df = pd.DataFrame(data_sensor)

# ====================== TABEL ======================
st.header("📋 Tabel Data Sensor")

# Tampilkan tabel gabungan dengan tabulate
st.markdown("### Gabungan Data (Tabulate)")
st.markdown(
    tabulate(df, headers="keys", tablefmt="github"),
    unsafe_allow_html=True
)

# Tampilkan tabel interaktif dengan st.dataframe
st.markdown("### Tabel Interaktif (Streamlit)")
st.dataframe(df)

# ====================== GRAFIK ======================
st.header("📈 Visualisasi Grafik")

# Pilih parameter untuk visualisasi
parameter = st.selectbox(
    "Pilih parameter untuk grafik:",
    ["Suhu", "Kelembaban", "Tekanan"]
)

# Buat grafik dengan Matplotlib
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df["Sensor"], df[parameter], color="skyblue")
ax.set_title(f"Perbandingan {parameter} per Sensor")
ax.set_xlabel("Sensor")
ax.set_ylabel(parameter)

# Tambahkan nilai di atas bar
for i, v in enumerate(df[parameter]):
    ax.text(i, v + 0.5, str(v), ha="center")

st.pyplot(fig)

# Grafik garis semua parameter
st.markdown("### Tren Semua Parameter")
fig2, ax2 = plt.subplots(figsize=(10, 5))
for col in ["Suhu", "Kelembaban", "Tekanan"]:
    ax2.plot(df["Sensor"], df[col], marker="o", label=col)
ax2.set_title("Tren Parameter Sensor")
ax2.legend()
st.pyplot(fig2)
