import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Dark mode style
plt.style.use("dark_background")
sns.set_palette("bright")

# ========== Judul Aplikasi ==========
st.title("📊 Dashboard Data Sensor - Versi Layout Baru")

# Data sensor contoh (data berbeda untuk masing-masing grafik)
data1 = [
    {"Sensor": "Sensor A1", "Nilai": 23},
    {"Sensor": "Sensor A2", "Nilai": 29},
    {"Sensor": "Sensor A3", "Nilai": 25}
]

data2 = [
    {"Sensor": "Sensor B1", "Nilai": 18},
    {"Sensor": "Sensor B2", "Nilai": 21},
    {"Sensor": "Sensor B3", "Nilai": 19}
]

data3 = [
    {"Sensor": "Sensor C1", "Nilai": 30},
    {"Sensor": "Sensor C2", "Nilai": 27},
    {"Sensor": "Sensor C3", "Nilai": 32}
]

data4 = [
    {"Sensor": "Sensor D1", "Nilai": 15},
    {"Sensor": "Sensor D2", "Nilai": 13},
    {"Sensor": "Sensor D3", "Nilai": 17}
]

# Konversi ke DataFrame
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)

# ========== Baris 1: Dua grafik bar berdempetan ==========
st.markdown("## 📈 Grafik Baris 1")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    ax.bar(df1["Sensor"], df1["Nilai"], color="cyan")
    ax.set_title("Grafik Data 1")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    ax.bar(df2["Sensor"], df2["Nilai"], color="orange")
    ax.set_title("Grafik Data 2")
    st.pyplot(fig)

# ========== Baris 2: Dua grafik bar berdempetan ==========
st.markdown("## 📈 Grafik Baris 2")
col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots()
    ax.bar(df3["Sensor"], df3["Nilai"], color="magenta")
    ax.set_title("Grafik Data 3")
    st.pyplot(fig)

with col4:
    fig, ax = plt.subplots()
    ax.bar(df4["Sensor"], df4["Nilai"], color="lime")
    ax.set_title("Grafik Data 4")
    st.pyplot(fig)

# ========== Baris 3: Tabel Gabungan Semua Data ==========
st.markdown("## 📋 Tabel Gabungan Semua Data")

# Gabungkan semua DataFrame
df_all = pd.concat([
    df1.assign(Grafik="Data 1"),
    df2.assign(Grafik="Data 2"),
    df3.assign(Grafik="Data 3"),
    df4.assign(Grafik="Data 4"),
], ignore_index=True)

st.dataframe(df_all)

# ========== Baris 4: Grafik Gabungan Semua Data ==========
st.markdown("## 📉 Grafik Gabungan Semua Data")

fig, ax = plt.subplots(figsize=(12, 6))

for name, group in df_all.groupby("Grafik"):
    ax.plot(group["Sensor"], group["Nilai"], marker="o", label=name)

ax.set_title("Gabungan Semua Grafik")
ax.set_xlabel("Sensor")
ax.set_ylabel("Nilai")
ax.legend()
st.pyplot(fig)
