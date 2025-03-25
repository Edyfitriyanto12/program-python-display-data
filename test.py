import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Inisialisasi Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")  # Sesuaikan dengan file Anda
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://your-project-id.firebaseio.com/'  # Ganti dengan URL Firebase Anda
    })

# Fungsi untuk membaca data dari Firebase
def get_data():
    ref = db.reference('/')  # Baca seluruh data
    data = ref.get()
    return data

# Tampilan di Streamlit
st.title("Monitoring Data dari Firebase")
data = get_data()
st.write(data)
