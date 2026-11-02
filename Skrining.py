import streamlit as st

# ==========================================
# 1. BASIS PENGETAHUAN (KNOWLEDGE BASE)
# ==========================================
# Daftar gejala yang sering dialami siswa SMA/SMK
gejala_list = {
    "G01": "Sering merasa sedih, murung, atau kosong",
    "G02": "Kehilangan minat pada hobi atau kegiatan sekolah",
    "G03": "Sering merasa lelah fisik walau tidak banyak aktivitas",
    "G04": "Mengalami kesulitan tidur atau insomnia",
    "G05": "Sering merasa cemas, was-was, atau panik tiba-tiba",
    "G06": "Sulit berkonsentrasi saat belajar di kelas",
    "G07": "Mudah marah, tersinggung, atau sensitif",
    "G08": "Sering menunda tugas sekolah karena merasa kewalahan",
    "G09": "Jantung sering berdebar cepat atau napas pendek",
    "G10": "Merasa tidak berharga atau pesimis dengan masa depan"
}

# Aturan (Rules) menggunakan pendekatan pengumpulan gejala
# Jika persentase kecocokan gejala memenuhi threshold, diagnosis ditegakkan
rules = {
    "Indikasi Depresi Ringan-Sedang": ["G01", "G02", "G03", "G04", "G10"],
    "Indikasi Kecemasan (Anxiety)": ["G04", "G05", "G06", "G09"],
    "Indikasi Stres Akademik (Burnout)": ["G03", "G06", "G07", "G08"]
}

# ==========================================
# 2. MESIN INFERENSI (INFERENCE ENGINE)
# ==========================================
def diagnosa(gejala_terpilih):
    hasil_diagnosa = []
    
    # Mencocokkan gejala terpilih dengan setiap rule (Forward Chaining)
    for penyakit, gejala_penyakit in rules.items():
        # Hitung irisan antara gejala yang dialami dengan rule
        cocok = set(gejala_penyakit).intersection(set(gejala_terpilih))
        
        # Jika gejala yang cocok lebih dari 50% dari rule, masukkan ke hasil
        if len(cocok) / len(gejala_penyakit) >= 0.5:
            persentase = int((len(cocok) / len(gejala_penyakit)) * 100)
            hasil_diagnosa.append((penyakit, persentase))
            
    # Urutkan berdasarkan persentase tertinggi
    return sorted(hasil_diagnosa, key=lambda x: x[1], reverse=True)

# ==========================================
# 3. ANTARMUKA WEB (WEB GUI)
# ==========================================
st.set_page_config(page_title="Skrining Mental Siswa", page_icon="🧠", layout="centered")

st.title("🧠 Sistem Pakar Skrining Kesehatan Mental")
st.markdown("""
Aplikasi ini dirancang untuk melakukan skrining awal kondisi mental siswa SMA/SMK (Stres Akademik, Kecemasan, atau Depresi). 
**Peringatan:** *Hasil dari sistem ini hanyalah deteksi dini untuk keperluan akademis dan tidak menggantikan diagnosis klinis dari psikolog atau psikiater.*
""")
st.divider()

st.subheader("Pilih gejala yang Anda rasakan dalam 2 minggu terakhir:")

# Form input
with st.form("form_diagnosa"):
    gejala_terpilih = []
    
    # Menampilkan checkbox untuk setiap gejala
    for kode, deskripsi in gejala_list.items():
        if st.checkbox(deskripsi, key=kode):
            gejala_terpilih.append(kode)
            
    submit_button = st.form_submit_button(label="Analisis Kondisi Saya")

# Menampilkan hasil setelah tombol ditekan
if submit_button:
    st.divider()
    if not gejala_terpilih:
        st.warning("⚠️ Anda belum memilih gejala apa pun. Silakan centang minimal satu gejala.")
    else:
        st.subheader("📊 Hasil Skrining:")
        hasil = diagnosa(gejala_terpilih)
        
        if hasil:
            for penyakit, probabilitas in hasil:
                st.error(f"**{penyakit}** (Kecocokan Gejala: {probabilitas}%)")
            
            st.info("""
            **Saran Tindakan:**
            - Bicarakan perasaan Anda dengan Guru Bimbingan Konseling (BK) di sekolah.
            - Kurangi tekanan akademik sejenak dan atur ulang jadwal istirahat.
            - Jika kondisi ini mengganggu aktivitas sehari-hari, segera hubungi profesional (Psikolog/Puskesmas terdekat).
            """)
        else:
            st.success("Tingkat stres Anda dalam batas normal. Tetap jaga kesehatan fisik dan mental, serta kelola waktu belajar dengan baik!")