"""
Generate SMK Survey Dataset
Creates synthetic dataset with 1000 records matching actual SMK Makarya 1 Jakarta survey structure
NO nilai_rata/IPK field - SMK doesn't use GPA system
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

# Number of records
n_samples = 1000

print("🚀 Generating SMK Survey Dataset...")
print(f"📊 Creating {n_samples} records with 28+ fields")

# ============================================================================
# SECTION 1: INFORMASI DASAR (5 fields)
# ============================================================================

data = {
    'email': [f'alumni{i}@smkmakarya1.sch.id' for i in range(1, n_samples + 1)],
    'nama': [f'Alumni_{i:04d}' for i in range(1, n_samples + 1)],
    'tempat_tinggal': np.random.choice(
        ['Jakarta', 'Depok', 'Tangerang Selatan', 'Tangerang', 'Bekasi'],
        size=n_samples,
        p=[0.4, 0.2, 0.15, 0.15, 0.1]  # Jakarta dominan
    ),
    'jurusan': np.random.choice(
        ['Akuntansi', 'Perkantoran', 'Pemasaran'],
        size=n_samples,
        p=[0.4, 0.35, 0.25]  # Akuntansi paling banyak
    ),
    'status_bekerja': np.random.choice(
        ['Ya', 'Tidak'],
        size=n_samples,
        p=[0.75, 0.25]  # 75% sudah bekerja
    )
}

# ============================================================================
# SECTION 2 & 3: CONDITIONAL FIELDS
# ============================================================================

# Initialize all fields with defaults
profesi_list = []
tempat_kerja_list = []
cara_mendapat_pekerjaan_list = []
kemudahan_cari_kerja_list = []
bantuan_sekolah_list = []
kesesuaian_minat_list = []
waktu_kerja_pertama_list = []
jenis_perusahaan_list = []
kesesuaian_jurusan_list = []
kepuasan_list = []
rencana_pindah_kerja_list = []
lama_kerja_list = []
kenyamanan_list = []
gaji_list = []

# Fields for unemployed
alasan_belum_kerja_list = []
kemudahan_cari_kerja_belum_list = []
bantuan_sekolah_belum_list = []
rencana_kerja_sesuai_jurusan_list = []
kendala_utama_list = []
ikut_pelatihan_list = []
gunakan_platform_online_list = []
kepercayaan_keterampilan_list = []
bersedia_rekomendasi_sekolah_list = []

# Profession options by major
profesi_mapping = {
    'Akuntansi': ['Akuntan', 'Staff Accounting', 'Tax Consultant', 'Auditor', 'Finance Staff'],
    'Perkantoran': ['Staff Administrasi', 'Sekretaris', 'Customer Service', 'Receptionist', 'Data Entry'],
    'Pemasaran': ['Marketing Staff', 'Sales Executive', 'Digital Marketing', 'Brand Ambassador', 'Account Executive']
}

# Jurusan cocok mapping (13 majors)
jurusan_cocok_options = [
    'Akuntansi', 'Bisnis', 'Komunikasi', 'Teknik', 'Keuangan',
    'Seni', 'Hiburan', 'Teknologi Informasi', 'Pendidikan',
    'Kesehatan', 'Hukum', 'Pertanian', 'Pariwisata'
]

# Perusahaan tepat (2 classes)
perusahaan_tepat_options = ['Tepat', 'Tidak Tepat']

# Generate data based on employment status
for i in range(n_samples):
    status = data['status_bekerja'][i]
    jurusan = data['jurusan'][i]
    
    if status == 'Ya':  # EMPLOYED
        # Profesi based on jurusan
        profesi = np.random.choice(profesi_mapping[jurusan])
        profesi_list.append(profesi)
        
        # Tempat kerja (sama atau beda dari tempat tinggal)
        if np.random.random() < 0.6:  # 60% kerja di kota yang sama
            tempat_kerja_list.append(data['tempat_tinggal'][i])
        else:
            tempat_kerja_list.append(np.random.choice(['Jakarta', 'Depok', 'Tangerang Selatan', 'Tangerang', 'Bekasi']))
        
        # Cara mendapat pekerjaan (bisa multiple)
        cara_options = ['Melalui keluarga/teman', 'Melalui job fair', 'Mencari sendiri']
        n_cara = np.random.choice([1, 2], p=[0.7, 0.3])
        cara = ', '.join(np.random.choice(cara_options, size=n_cara, replace=False))
        cara_mendapat_pekerjaan_list.append(cara)
        
        # Kemudahan cari kerja
        kemudahan_cari_kerja_list.append(np.random.choice(['Mudah', 'Sulit'], p=[0.6, 0.4]))
        
        # Bantuan sekolah
        bantuan_sekolah_list.append(np.random.choice(['Ya', 'Tidak'], p=[0.55, 0.45]))
        
        # Kesesuaian minat
        kesesuaian_minat_list.append(np.random.choice(['Sesuai', 'Tidak sesuai'], p=[0.65, 0.35]))
        
        # Waktu kerja pertama
        waktu_kerja_pertama_list.append(np.random.choice(
            ['< 3 bulan', '3–6 bulan', '6–12 bulan', '1 tahun'],
            p=[0.35, 0.35, 0.2, 0.1]
        ))
        
        # Jenis perusahaan
        jenis_perusahaan_list.append(np.random.choice(
            ['BUMN', 'PNS', 'Perusahaan Swasta', 'Wirausaha'],
            p=[0.15, 0.1, 0.65, 0.1]
        ))
        
        # Kesesuaian jurusan
        kesesuaian_jurusan_list.append(np.random.choice(['Ya', 'Tidak'], p=[0.7, 0.3]))
        
        # Kepuasan
        kepuasan_list.append(np.random.choice(['Tidak puas', 'Puas'], p=[0.3, 0.7]))
        
        # Rencana pindah kerja
        rencana_pindah_kerja_list.append(np.random.choice(['Ya', 'Tidak'], p=[0.4, 0.6]))
        
        # Lama kerja (0.5 - 10 tahun)
        lama_kerja = round(np.random.uniform(0.5, 10), 1)
        lama_kerja_list.append(lama_kerja)
        
        # Kenyamanan
        kenyamanan_list.append(np.random.choice(['Ya', 'Tidak'], p=[0.75, 0.25]))
        
        # Gaji (based on experience and company type)
        if lama_kerja < 2:
            gaji = np.random.choice(['Dibawah UMR', 'UMR', 'Diatas UMR'], p=[0.4, 0.5, 0.1])
        elif lama_kerja < 5:
            gaji = np.random.choice(['Dibawah UMR', 'UMR', 'Diatas UMR'], p=[0.2, 0.5, 0.3])
        else:
            gaji = np.random.choice(['Dibawah UMR', 'UMR', 'Diatas UMR'], p=[0.1, 0.3, 0.6])
        gaji_list.append(gaji)
        
        # Unemployed fields - set to N/A
        alasan_belum_kerja_list.append('N/A')
        kemudahan_cari_kerja_belum_list.append('N/A')
        bantuan_sekolah_belum_list.append('N/A')
        rencana_kerja_sesuai_jurusan_list.append('N/A')
        kendala_utama_list.append('N/A')
        ikut_pelatihan_list.append('N/A')
        gunakan_platform_online_list.append('N/A')
        kepercayaan_keterampilan_list.append('N/A')
        bersedia_rekomendasi_sekolah_list.append('N/A')
        
    else:  # UNEMPLOYED
        # Employed fields - set to N/A or defaults
        profesi_list.append('N/A')
        tempat_kerja_list.append(data['tempat_tinggal'][i])  # Same as residence
        cara_mendapat_pekerjaan_list.append('N/A')
        kesesuaian_minat_list.append('N/A')
        waktu_kerja_pertama_list.append('N/A')
        jenis_perusahaan_list.append('N/A')
        kesesuaian_jurusan_list.append('N/A')
        kepuasan_list.append('N/A')
        rencana_pindah_kerja_list.append('N/A')
        lama_kerja_list.append(0)
        kenyamanan_list.append('N/A')
        gaji_list.append('N/A')
        
        # Unemployed specific fields
        alasan_belum_kerja_list.append(np.random.choice(
            ['Sedang mencari pekerjaan', 'Kuliah'],
            p=[0.7, 0.3]
        ))
        
        kemudahan_cari_kerja_list.append(np.random.choice(['Mudah', 'Sulit'], p=[0.3, 0.7]))
        kemudahan_cari_kerja_belum_list.append(kemudahan_cari_kerja_list[-1])
        
        bantuan_sekolah_list.append(np.random.choice(['Ya', 'Tidak'], p=[0.4, 0.6]))
        bantuan_sekolah_belum_list.append(bantuan_sekolah_list[-1])
        
        rencana_kerja_sesuai_jurusan_list.append(np.random.choice(['Ya', 'Tidak'], p=[0.75, 0.25]))
        
        kendala_utama_list.append(np.random.choice([
            'Kurangnya lowongan yang sesuai',
            'Kurangnya pengalaman kerja',
            'Kurangnya keterampilan yang dibutuhkan'
        ], p=[0.4, 0.4, 0.2]))
        
        ikut_pelatihan_list.append(np.random.choice(['Ya', 'Tidak'], p=[0.35, 0.65]))
        
        gunakan_platform_online_list.append(np.random.choice(['Ya', 'Tidak'], p=[0.6, 0.4]))
        
        kepercayaan_keterampilan_list.append(np.random.choice(['Tidak yakin', 'Yakin'], p=[0.5, 0.5]))
        
        bersedia_rekomendasi_sekolah_list.append(np.random.choice(['Ya', 'Tidak'], p=[0.85, 0.15]))

# ============================================================================
# ADD FIELDS TO DATAFRAME
# ============================================================================

# Section 2: Employed fields
data['profesi_sekarang'] = profesi_list
data['tempat_kerja'] = tempat_kerja_list
data['cara_mendapat_pekerjaan'] = cara_mendapat_pekerjaan_list
data['kemudahan_cari_kerja'] = kemudahan_cari_kerja_list
data['bantuan_sekolah'] = bantuan_sekolah_list
data['kesesuaian_minat'] = kesesuaian_minat_list
data['waktu_kerja_pertama'] = waktu_kerja_pertama_list
data['jenis_perusahaan'] = jenis_perusahaan_list
data['kesesuaian_jurusan'] = kesesuaian_jurusan_list
data['kepuasan'] = kepuasan_list
data['rencana_pindah_kerja'] = rencana_pindah_kerja_list
data['lama_kerja_1'] = lama_kerja_list
data['lama_kerja_2'] = lama_kerja_list  # Same as lama_kerja_1 for simplicity
data['nyaman'] = kenyamanan_list
data['gaji_kategori'] = gaji_list

# Section 3: Unemployed fields
data['alasan_belum_kerja'] = alasan_belum_kerja_list
data['rencana_kerja_sesuai_jurusan'] = rencana_kerja_sesuai_jurusan_list
data['kendala_utama'] = kendala_utama_list
data['ikut_pelatihan'] = ikut_pelatihan_list
data['gunakan_platform_online'] = gunakan_platform_online_list
data['kepercayaan_keterampilan'] = kepercayaan_keterampilan_list
data['bersedia_rekomendasi_sekolah'] = bersedia_rekomendasi_sekolah_list

# ============================================================================
# ADD TARGET VARIABLES (for ML models)
# ============================================================================

# Jurusan cocok (13 classes) - based on jurusan and profesi
jurusan_cocok_list = []
for i in range(n_samples):
    if data['status_bekerja'][i] == 'Ya':
        # Alumni yang bekerja: distribute across all 13 majors
        # Bias toward their SMK jurusan
        if data['jurusan'][i] == 'Akuntansi':
            jurusan_cocok = np.random.choice(jurusan_cocok_options, p=[0.4, 0.15, 0.05, 0.05, 0.15, 0.02, 0.02, 0.05, 0.02, 0.02, 0.02, 0.02, 0.03])
        elif data['jurusan'][i] == 'Perkantoran':
            jurusan_cocok = np.random.choice(jurusan_cocok_options, p=[0.1, 0.3, 0.15, 0.05, 0.1, 0.02, 0.02, 0.15, 0.05, 0.02, 0.02, 0.01, 0.01])
        else:  # Pemasaran
            jurusan_cocok = np.random.choice(jurusan_cocok_options, p=[0.05, 0.3, 0.2, 0.02, 0.1, 0.05, 0.1, 0.08, 0.02, 0.02, 0.02, 0.02, 0.02])
    else:
        # Alumni belum bekerja: distribute evenly
        jurusan_cocok = np.random.choice(jurusan_cocok_options)
    jurusan_cocok_list.append(jurusan_cocok)

data['jurusan_cocok'] = jurusan_cocok_list

# Perusahaan tepat (2 classes) - based on kesesuaian_jurusan and kepuasan
perusahaan_tepat_list = []
for i in range(n_samples):
    if data['status_bekerja'][i] == 'Ya':
        if data['kesesuaian_jurusan'][i] == 'Ya' and data['kepuasan'][i] == 'Puas':
            perusahaan_tepat_list.append('Tepat')
        elif data['kesesuaian_jurusan'][i] == 'Tidak' or data['kepuasan'][i] == 'Tidak puas':
            perusahaan_tepat_list.append(np.random.choice(['Tepat', 'Tidak Tepat'], p=[0.3, 0.7]))
        else:
            perusahaan_tepat_list.append(np.random.choice(['Tepat', 'Tidak Tepat'], p=[0.6, 0.4]))
    else:
        perusahaan_tepat_list.append('Tidak Tepat')  # Belum bekerja

data['perusahaan_tepat'] = perusahaan_tepat_list

# Convert gaji_kategori to numeric gaji for ML
gaji_numeric_list = []
for gaji_kat in data['gaji_kategori']:
    if gaji_kat == 'Dibawah UMR':
        gaji_numeric_list.append(int(np.random.uniform(3000000, 4800000)))
    elif gaji_kat == 'UMR':
        gaji_numeric_list.append(int(np.random.uniform(4800000, 6000000)))
    elif gaji_kat == 'Diatas UMR':
        gaji_numeric_list.append(int(np.random.uniform(6000000, 15000000)))
    else:  # N/A
        gaji_numeric_list.append(0)

data['gaji'] = gaji_numeric_list

# Convert waktu_kerja_pertama to numeric (months)
waktu_numeric_list = []
waktu_map = {
    '< 3 bulan': 2,
    '3–6 bulan': 4,
    '6–12 bulan': 9,
    '1 tahun': 12,
    'N/A': 0
}
for waktu in data['waktu_kerja_pertama']:
    waktu_numeric_list.append(waktu_map.get(waktu, 0))

data['waktu_kerja_pertama_bulan'] = waktu_numeric_list

# ============================================================================
# CREATE DATAFRAME AND SAVE
# ============================================================================

df = pd.DataFrame(data)

# Reorder columns for better organization
columns_order = [
    # Section 1: Basic Info
    'email', 'nama', 'tempat_tinggal', 'jurusan', 'status_bekerja',
    # Section 2: Employed
    'profesi_sekarang', 'tempat_kerja', 'cara_mendapat_pekerjaan',
    'kemudahan_cari_kerja', 'bantuan_sekolah', 'kesesuaian_minat',
    'waktu_kerja_pertama', 'waktu_kerja_pertama_bulan',
    'jenis_perusahaan', 'kesesuaian_jurusan', 'kepuasan',
    'rencana_pindah_kerja', 'lama_kerja_1', 'lama_kerja_2',
    'nyaman', 'gaji_kategori', 'gaji',
    # Section 3: Unemployed
    'alasan_belum_kerja', 'rencana_kerja_sesuai_jurusan', 'kendala_utama',
    'ikut_pelatihan', 'gunakan_platform_online', 'kepercayaan_keterampilan',
    'bersedia_rekomendasi_sekolah',
    # Target variables
    'jurusan_cocok', 'perusahaan_tepat'
]

df = df[columns_order]

# Backup old dataset
import os
old_file = 'job_survey.csv'
if os.path.exists(old_file):
    backup_file = f'job_survey_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    os.rename(old_file, backup_file)
    print(f"✅ Backed up old dataset: {backup_file}")

# Save new dataset
df.to_csv('job_survey.csv', index=False, encoding='utf-8-sig')

print(f"\n✅ Dataset generated successfully!")
print(f"📁 File: job_survey.csv")
print(f"📊 Records: {len(df)}")
print(f"📋 Columns: {len(df.columns)}")
print(f"\n📈 Dataset Summary:")
print(f"   - Employed: {(df['status_bekerja'] == 'Ya').sum()} ({(df['status_bekerja'] == 'Ya').sum()/len(df)*100:.1f}%)")
print(f"   - Unemployed: {(df['status_bekerja'] == 'Tidak').sum()} ({(df['status_bekerja'] == 'Tidak').sum()/len(df)*100:.1f}%)")
print(f"   - Jurusan Akuntansi: {(df['jurusan'] == 'Akuntansi').sum()}")
print(f"   - Jurusan Perkantoran: {(df['jurusan'] == 'Perkantoran').sum()}")
print(f"   - Jurusan Pemasaran: {(df['jurusan'] == 'Pemasaran').sum()}")
print(f"\n🎯 Target Variables:")
print(f"   - Jurusan Cocok: {df['jurusan_cocok'].nunique()} unique classes")
print(f"   - Perusahaan Tepat: {df['perusahaan_tepat'].value_counts().to_dict()}")
print(f"\n🔥 Ready for model training!")
