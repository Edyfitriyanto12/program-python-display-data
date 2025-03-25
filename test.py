import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Fungsi untuk mendapatkan data dari Firebase
def get_firebase_data():
    try:
        # Jika Firebase belum diinisialisasi
        if not firebase_admin._apps:
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://your-project.firebaseio.com'
            })
        
        # Ambil data dari Firebase Realtime Database
        ref = db.reference('path/to/your/data')
        data = ref.get()
        return data
    except Exception as e:
        st.error(f"Error accessing Firebase: {e}")
        return None

# Tampilan Streamlit
st.title("Data dari Firebase")

data = get_firebase_data()

if data:
    st.write("Data dari Firebase:")
    st.json(data)
else:
    st.write("Tidak ada data yang ditemukan atau terjadi error.")
