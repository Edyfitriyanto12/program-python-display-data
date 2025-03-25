import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Inisialisasi Firebase
def init_firebase():
    try:
        if not firebase_admin._apps:
            # Konfigurasi credentials dari Streamlit secrets
            firebase_config = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
                "client_email": st.secrets["firebase"]["client_email"],
                "token_uri": st.secrets["firebase"]["token_uri"]
            }
            
            # Inisialisasi Firebase Admin SDK
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred, {
                "databaseURL": st.secrets["firebase"]["database_url"]
            })
    except Exception as e:
        st.error(f"🔥 Gagal inisialisasi Firebase: {str(e)}")
        st.stop()  # Hentikan aplikasi jika inisialisasi gagal

def main():
    # Judul Aplikasi
    st.title("🔥 Monitoring Blower - Firebase Realtime")
    
    # Inisialisasi Firebase
    init_firebase()
    
    # =============================================
    # Bagian 1: Kontrol Fuzzy
    # =============================================
    st.subheader("🔄 Kontrol Fuzzy")
    try:
        # Ambil data dari path /Kontrol_Fuzzy
        fuzzy_ref = db.reference("/Kontrol_Fuzzy")
        fuzzy_data = fuzzy_ref.get()
        
        if fuzzy_data is None:
            st.warning("Data Kontrol Fuzzy tidak ditemukan. Pastikan:")
            st.markdown("- Path `/Kontrol_Fuzzy` ada di Firebase")
            st.markdown("- Rules database mengizinkan operasi baca")
        else:
            # Tampilkan data dalam 3 kolom
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Out Fuzzy", fuzzy_data.get("Out_Fuzzy", "N/A"))
            with col2:
                st.metric("Suhu Realtime", fuzzy_data.get("Suhu_realtime", "N/A"))
            with col3:
                st.metric("Suhu 5 Menit Sebelumnya", fuzzy_data.get("Suhu_5_mentt_sebelumnya", "N/A"))
            
            # Debug: Tampilkan raw data
            with st.expander("🔍 Lihat Data Mentah"):
                st.json(fuzzy_data)
                
    except Exception as e:
        st.error(f"🚨 Gagal membaca data Kontrol Fuzzy: {str(e)}")
    
    # =============================================
    # Bagian 2: Monitoring Tegangan AC
    # =============================================
    st.subheader("⚡ Monitoring Tegangan AC")
    try:
        # Ambil data dari path /Monitoring_Tegangan_AC
        tegangan_ref = db.reference("/Monitoring_Tegangan_AC")
        tegangan_data = tegangan_ref.get()
        
        if tegangan_data is None:
            st.warning("Data Tegangan AC tidak ditemukan. Pastikan:")
            st.markdown("- Path `/Monitoring_Tegangan_AC` ada di Firebase")
            st.markdown("- Rules database mengizinkan operasi baca")
        else:
            # Tampilkan data dalam 3 kolom
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tegangan", f"{tegangan_data.get('Tegangan', 'N/A')} V")
            with col2:
                st.metric("Ampere", f"{tegangan_data.get('Ampere', 'N/A')} A")
            with col3:
                st.metric("Frequency", f"{tegangan_data.get('Frequency', 'N/A')} Hz")
            
            # Debug: Tampilkan raw data
            with st.expander("🔍 Lihat Data Mentah"):
                st.json(tegangan_data)
                
    except Exception as e:
        st.error(f"🚨 Gagal membaca data Tegangan AC: {str(e)}")
    
    # =============================================
    # Bagian 3: Debugging - Tampilkan Semua Data
    # =============================================
    with st.expander("🛠️ Debug Database"):
        try:
            all_data_ref = db.reference("/")
            all_data = all_data_ref.get()
            st.write("Struktur Database Lengkap:")
            st.json(all_data)
        except Exception as e:
            st.error(f"Gagal memuat semua data: {str(e)}")

if __name__ == "__main__":
    main()
