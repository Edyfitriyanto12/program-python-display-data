import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

def init_firebase():
    try:
        if not firebase_admin._apps:
            # Gunakan struktur dictionary langsung
            firebase_config = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
                "client_email": st.secrets["firebase"]["client_email"],
                "token_uri": st.secrets["firebase"]["token_uri"]
            }
            
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred, {
                "databaseURL": st.secrets["firebase"]["database_url"]
            })
            st.success("✅ Firebase initialized!")
    except Exception as e:
        st.error(f"🔥 Error: {e}")
        st.stop()  # Hentikan aplikasi jika gagal

def main():
    init_firebase()  # Pastikan ini dipanggil pertama!
    
    try:
        ref = db.reference("/")  # Ganti dengan path data Anda
        data = ref.get()
        st.json(data)
    except Exception as e:
        st.error(f"🚨 Failed to fetch data: {e}")

if __name__ == "__main__":
    main()
