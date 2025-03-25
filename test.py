import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# ========== Konfigurasi Firebase ==========
def init_firebase():
    try:
        if not firebase_admin._apps:
            # Gunakan Streamlit Secrets
            firebase_config = {
                "type": st.secrets["FIREBASE_TYPE"],
                "project_id": st.secrets["FIREBASE_PROJECT_ID"],
                "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
                "private_key": st.secrets["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
                "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
                "client_id": st.secrets["FIREBASE_CLIENT_ID"],
                "auth_uri": st.secrets["FIREBASE_AUTH_URI"],
                "token_uri": st.secrets["FIREBASE_TOKEN_URI"],
                "auth_provider_x509_cert_url": st.secrets["FIREBASE_AUTH_PROVIDER_CERT_URL"],
                "client_x509_cert_url": st.secrets["FIREBASE_CLIENT_CERT_URL"]
            }
            
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred, {
                "databaseURL": st.secrets["FIREBASE_DATABASE_URL"]
            })
    except Exception as e:
        st.error(f"🔥 Error initializing Firebase: {e}")

# ========== Aplikasi Streamlit ==========
def main():
    st.title("📊 Data dari Firebase Realtime Database")
    
    # Inisialisasi Firebase
    init_firebase()
    
    # Contoh: Ambil data dari path 'sensor_data'
    try:
        ref = db.reference("/sensor_data")
        data = ref.get()
        
        if data:
            st.subheader("📈 Data Sensor Terkini")
            st.json(data)
            
            # # Contoh visualisasi sederhana
            # if isinstance(data, dict):
            #     st.metric("Suhu", f"{data.get('temperature', 0)}°C")
            #     st.line_chart({"Suhu": [data.get('temperature', 0)]}s)
        else:
            st.warning("Tidak ada data ditemukan di Firebase.")
            
    except Exception as e:
        st.error(f"🚨 Error fetching data: {e}")

if __name__ == "__main__":
    main()
