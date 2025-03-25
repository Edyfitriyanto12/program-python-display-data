import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import os
import json
import time

# ==============================
# 🔹 Setup Firebase
# ==============================
st.set_page_config(page_title="Monitoring Firebase", layout="wide")

st.title("📡 Monitoring Data Realtime dari Firebase")

# Ambil JSON kredensial dari GitHub Secrets
firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if firebase_json:
    cred_dict = json.loads(firebase_json)
    if not firebase_admin._apps:  # Hindari inisialisasi ganda
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://your-project-id.firebaseio.com/'  # Ganti dengan URL Firebase Anda
        })
else:
    st.error("⚠️ Kredensial Firebase tidak ditemukan! Pastikan Anda telah menambahkan FIREBASE_CREDENTIALS di GitHub Secrets.")

# ==============================
# 🔹 Fungsi Ambil Data dari Firebase
# ==============================
def get_data():
    try:
        ref = db.reference('/')  # Baca seluruh data
        data = ref.get()
        return data if data else {}
    except Exception as e:
        st.error(f"⚠️ Gagal mengambil data dari Firebase: {e}")
        return {}

# ==============================
# 🔹 Tampilan di Streamlit
# ==============================
st.subheader("📊 Data dari Firebase")

# Loop untuk membaca data secara otomatis setiap 5 detik
placeholder = st.empty()  # Placeholder untuk update data secara live

while True:
    data = get_data()
    placeholder.json(data)  # Update tampilan JSON di Streamlit
    time.sleep(5)  # Tunggu 5 detik sebelum refresh lagi
