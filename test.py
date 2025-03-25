import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Inisialisasi Firebase
def init_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate({
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
                "client_email": st.secrets["firebase"]["client_email"]
            })
            firebase_admin.initialize_app(cred, {
                "databaseURL": st.secrets["firebase"]["database_url"]
            })
    except Exception as e:
        st.error(f"🔥 Error: {e}")
        st.stop()

def main():
    init_firebase()
    
    st.title("Monitoring Blower (Firebase + Streamlit)")
    
    # Ambil data Kontrol Fuzzy
    try:
        st.subheader("🔄 Kontrol Fuzzy")
        fuzzy_ref = db.reference("/Kontrol_Fuzzy")
        fuzzy_data = fuzzy_ref.get()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Out Fuzzy", fuzzy_data.get("Out_Fuzzy"))
        with col2:
            st.metric("Suhu Realtime", fuzzy_data.get("Suhu_realtime"))
        with col3:
            st.metric("Suhu 5 Menit Sebelumnya", fuzzy_data.get("Suhu_5_mentt_sebelumnya"))
        
    except Exception as e:
        st.error(f"Gagal baca data Kontrol Fuzzy: {e}")
    
    # Ambil data Monitoring Tegangan AC
    try:
        st.subheader("⚡ Monitoring Tegangan AC")
        tegangan_ref = db.reference("/Monitoring_Tegangan_AC")
        tegangan_data = tegangan_ref.get()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tegangan", f"{tegangan_data.get('Tegangan')} V")
        with col2:
            st.metric("Ampere", f"{tegangan_data.get('Ampere')} A")
        with col3:
            st.metric("Frequency", f"{tegangan_data.get('Frequency')} Hz")
            
    except Exception as e:
        st.error(f"Gagal baca data Tegangan: {e}")

if __name__ == "__main__":
    main()
