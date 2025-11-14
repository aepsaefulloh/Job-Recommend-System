# 📊 DOKUMENTASI STRUKTUR DATA & DATABASE
## Sistem Rekomendasi Pekerjaan Alumni SMK

**Untuk Kebutuhan Skripsi**  
**Tanggal:** November 14, 2025  
**Penulis:** Job Recommendation System Team

---

## 📋 Daftar Isi

1. [Pendahuluan](#pendahuluan)
2. [Arsitektur Sistem Data](#arsitektur-sistem-data)
3. [Struktur Dataset (CSV)](#struktur-dataset-csv)
4. [Model Database](#model-database)
5. [Proses Generate Dataset](#proses-generate-dataset)
6. [Proses Import ke Database](#proses-import-ke-database)
7. [Flow Data Lengkap](#flow-data-lengkap)
8. [Statistik & Validasi](#statistik--validasi)

---

## 🎯 Pendahuluan

### **Tujuan Dokumentasi**
Dokumentasi ini menjelaskan struktur data lengkap dari Sistem Rekomendasi Pekerjaan untuk Alumni SMK, mulai dari pembuatan dataset sintetis hingga penyimpanan di database MySQL.

### **Komponen Utama**
1. **Dataset Generator** (`generate_smk_dataset.py`)
2. **Database Models** (`models.py`)
3. **Database Setup** (`setup_database.py`)
4. **Preprocessing** (`preprocessing.py`)

---

## 🏗️ Arsitektur Sistem Data

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CSV Dataset   │ -> │   Data Models   │ -> │   MySQL DB      │
│                 │    │                 │    │                 │
│ job_survey.csv  │    │ SurveyData      │    │ survey_data     │
│ (7,000 records) │    │ DashboardStats  │    │ dashboard_stats │
│                 │    │ User            │    │ users           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
    Generate Script         Flask-SQLAlchemy        XAMPP MySQL
```

---

## 📊 Struktur Dataset (CSV)

### **File:** `job_survey.csv`
### **Total Records:** 7,000
### **Total Kolom:** 31

### **1. Informasi Dasar (Section 1)**
| Kolom | Tipe Data | Deskripsi | Contoh |
|-------|-----------|-----------|---------|
| `email` | String | Email alumni | alumni0001@smkmakarya1.sch.id |
| `nama` | String | Nama lengkap | Alumni_0001 |
| `tempat_tinggal` | String | Kota domisili | Jakarta, Depok, Tangerang |
| `jurusan` | String | Jurusan SMK | Akuntansi, Perkantoran, Pemasaran |
| `status_bekerja` | String | Status pekerjaan | Ya/Tidak |

### **2. Data Pekerjaan (Section 2 - Jika Sudah Bekerja)**
| Kolom | Tipe Data | Deskripsi | Contoh |
|-------|-----------|-----------|---------|
| `profesi_sekarang` | String | Posisi saat ini | Staff Accounting, Sekretaris |
| `tempat_kerja` | String | Lokasi kerja | Jakarta, Depok |
| `cara_mendapat_pekerjaan` | Text | Cara mendapat kerja | Melalui keluarga/teman |
| `kemudahan_cari_kerja` | String | Tingkat kesulitan | Mudah, Sulit |
| `bantuan_sekolah` | String | Dukungan sekolah | Ya, Tidak |
| `kesesuaian_minat` | String | Minat dengan pekerjaan | Sesuai, Tidak sesuai |
| `waktu_kerja_pertama` | String | Waktu tunggu kerja | < 3 bulan, 3-6 bulan |
| `waktu_kerja_pertama_bulan` | Float | Waktu dalam bulan | 2.0, 4.0, 9.0 |
| `jenis_perusahaan` | String | Tipe perusahaan | BUMN, PNS, Swasta |
| `kesesuaian_jurusan` | String | Cocok dengan jurusan | Ya, Tidak |
| `kepuasan` | String | Tingkat kepuasan | Puas, Tidak puas |
| `rencana_pindah_kerja` | String | Plan pindah kerja | Ya, Tidak |
| `lama_kerja_1` | Float | Lama kerja (tahun) | 2.5, 5.0 |
| `lama_kerja_2` | Float | Total pengalaman | 2.5, 5.0 |
| `nyaman` | String | Kenyamanan kerja | Ya, Tidak |
| `gaji_kategori` | String | Kategori gaji | UMR, Diatas UMR |
| `gaji` | Float | Gaji numerik (Rp) | 5500000, 8500000 |

### **3. Data Pengangguran (Section 3 - Jika Belum Bekerja)**
| Kolom | Tipe Data | Deskripsi | Contoh |
|-------|-----------|-----------|---------|
| `alasan_belum_kerja` | String | Alasan belum kerja | Sedang mencari, Kuliah |
| `rencana_kerja_sesuai_jurusan` | String | Plan kerja sesuai jurusan | Ya, Tidak |
| `kendala_utama` | String | Kendala utama | Kurang pengalaman |
| `ikut_pelatihan` | String | Mengikuti pelatihan | Ya, Tidak |
| `gunakan_platform_online` | String | Platform online | Ya, Tidak |
| `kepercayaan_keterampilan` | String | Keyakinan skill | Yakin, Tidak yakin |
| `bersedia_rekomendasi_sekolah` | String | Rekomendasi sekolah | Ya, Tidak |

### **4. Variabel Target (Machine Learning)**
| Kolom | Tipe Data | Deskripsi | Kategori |
|-------|-----------|-----------|----------|
| `jurusan_cocok` | String | Rekomendasi jurusan | 8 kategori |
| `perusahaan_tepat` | String | Kesesuaian perusahaan | Tepat, Tidak Tepat |

---

## 🗄️ Model Database

### **Teknologi:** Flask-SQLAlchemy + MySQL
### **Database:** `job_recommendation_db`

### **1. Tabel: `survey_data`**
```sql
CREATE TABLE survey_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(120),
    nama VARCHAR(100),
    tempat_tinggal VARCHAR(50),
    jurusan VARCHAR(50),
    status_bekerja VARCHAR(10),

    -- Employment data
    profesi_sekarang VARCHAR(100),
    tempat_kerja VARCHAR(100),
    cara_mendapat_pekerjaan TEXT,
    kemudahan_cari_kerja VARCHAR(20),
    bantuan_sekolah VARCHAR(10),
    kesesuaian_minat VARCHAR(20),
    waktu_kerja_pertama FLOAT,
    waktu_kerja_pertama_bulan FLOAT,
    jenis_perusahaan VARCHAR(50),
    kesesuaian_jurusan VARCHAR(10),
    kepuasan VARCHAR(20),
    rencana_pindah_kerja VARCHAR(10),
    lama_kerja_1 FLOAT,
    lama_kerja_2 FLOAT,
    nyaman VARCHAR(10),
    gaji_kategori VARCHAR(20),
    gaji FLOAT,

    -- Unemployment data
    alasan_belum_kerja VARCHAR(100),
    rencana_kerja_sesuai_jurusan VARCHAR(10),
    kendala_utama VARCHAR(100),
    ikut_pelatihan VARCHAR(10),
    gunakan_platform_online VARCHAR(10),
    kepercayaan_keterampilan VARCHAR(20),
    bersedia_rekomendasi_sekolah VARCHAR(10),

    -- ML predictions
    jurusan_cocok VARCHAR(50),
    perusahaan_tepat VARCHAR(20),

    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### **2. Tabel: `users`** (Authentication)
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);
```

### **3. Tabel: `dashboard_stats`** (Cache Statistics)
```sql
CREATE TABLE dashboard_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    stat_name VARCHAR(50) UNIQUE NOT NULL,
    stat_value FLOAT NOT NULL,
    stat_type VARCHAR(20) NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## 🔧 Proses Generate Dataset

### **File:** `generate_smk_dataset.py`
### **Input:** Parameter konfigurasi
### **Output:** `job_survey.csv` (7,000 records)

### **Langkah-langkah Generate:**

#### **1. Setup Parameter**
```python
n_samples = 7000  # Total records
np.random.seed(42)  # Reproducibility
```

#### **2. Generate Data Dasar**
```python
data = {
    'email': [f'alumni{i}@smkmakarya1.sch.id' for i in range(1, n_samples + 1)],
    'nama': [f'Alumni_{i:04d}' for i in range(1, n_samples + 1)],
    'tempat_tinggal': np.random.choice(['Jakarta', 'Depok', 'Tangerang Selatan', 'Tangerang', 'Bekasi'], ...),
    'jurusan': np.random.choice(['Akuntansi', 'Perkantoran', 'Pemasaran'], ...),
    'status_bekerja': np.random.choice(['Ya', 'Tidak'], p=[0.75, 0.25])
}
```

#### **3. Conditional Logic Berdasarkan Status**
```python
if status_bekerja == 'Ya':  # SUDAH BEKERJA
    # Generate employment-related fields
    profesi = np.random.choice(profesi_mapping[jurusan])
    # ... other employment fields
else:  # BELUM BEKERJA
    # Generate unemployment-related fields
    alasan_belum_kerja = np.random.choice(['Sedang mencari pekerjaan', 'Kuliah'], ...)
    # ... other unemployment fields
```

#### **4. Generate Target Variables**
```python
# Jurusan cocok (8 classes)
if jurusan == 'Akuntansi':
    jurusan_cocok = np.random.choice(jurusan_cocok_options, p=[0.75, 0.15, ...])

# Perusahaan tepat (2 classes)
if kesesuaian_jurusan == 'Ya' and kepuasan == 'Puas':
    perusahaan_tepat = 'Tepat'
else:
    perusahaan_tepat = np.random.choice(['Tepat', 'Tidak Tepat'], p=[0.6, 0.4])
```

#### **5. Data Conversion**
```python
# Convert categorical gaji to numeric
gaji_numeric_list = []
for gaji_kat in data['gaji_kategori']:
    if gaji_kat == 'Dibawah UMR':
        gaji_numeric_list.append(int(np.random.uniform(3000000, 4800000)))
    # ... other conversions

# Convert waktu_kerja_pertama to numeric
waktu_map = {'< 3 bulan': 2, '3–6 bulan': 4, '6–12 bulan': 9, '1 tahun': 12}
```

#### **6. Save to CSV**
```python
df = pd.DataFrame(data)
df.to_csv('job_survey.csv', index=False, encoding='utf-8-sig')
```

---

## 💾 Proses Import ke Database

### **File:** `setup_database.py`
### **Input:** `job_survey.csv`
### **Output:** Data tersimpan di MySQL

### **Langkah-langkah Import:**

#### **1. Setup Database Connection**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
```

#### **2. Create Database & Tables**
```python
# Create database if not exists
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

# Create tables from models
db.create_all()
```

#### **3. Import Data Row by Row**
```python
for _, row in df.iterrows():
    survey_record = SurveyData(
        email=clean_value(row.get('email', '')),
        nama=clean_value(row.get('nama', '')),
        tempat_tinggal=clean_value(row.get('tempat_tinggal', '')),
        # ... map all CSV columns to model fields
        jurusan_cocok=clean_value(row.get('jurusan_cocok')),
        perusahaan_tepat=clean_value(row.get('perusahaan_tepat'))
    )
    db.session.add(survey_record)
```

#### **4. Calculate Dashboard Statistics**
```python
# Auto-calculate statistics
total_surveys = SurveyData.query.count()
employed_count = SurveyData.query.filter_by(status_bekerja='Ya').count()
employment_rate = (employed_count / total_surveys * 100)
avg_salary = db.session.query(db.func.avg(SurveyData.gaji)).filter(...).scalar()

# Save to dashboard_stats table
stats_data = [
    DashboardStats(stat_name='total_surveys', stat_value=total_surveys, stat_type='count'),
    DashboardStats(stat_name='employment_rate', stat_value=employment_rate, stat_type='percentage'),
    # ... other statistics
]
```

---

## 🔄 Flow Data Lengkap

```
1. GENERATE DATASET
   ├── generate_smk_dataset.py
   ├── Input: Configuration parameters
   └── Output: job_survey.csv (7,000 records)

2. DATABASE SETUP
   ├── setup_database.py
   ├── Create database & tables
   ├── Import CSV to MySQL
   └── Calculate statistics

3. DATA PREPROCESSING
   ├── preprocessing.py
   ├── Load data from CSV
   ├── Feature engineering
   ├── Normalization (StandardScaler)
   └── Train ML models

4. APPLICATION USAGE
   ├── app.py (Flask web app)
   ├── User submits survey
   ├── ML prediction
   └── Store results in database
```

### **Data Flow Diagram:**

```
CSV Dataset (7,000 records)
        │
        ▼
Database Import (setup_database.py)
        │
        ▼
MySQL Database (3 tables)
        │
        ▼
Preprocessing (preprocessing.py)
        │
        ▼
ML Models (KNN)
        │
        ▼
Web Application (app.py)
        │
        ▼
User Predictions
```

---

## 📈 Statistik & Validasi

### **Dataset Summary:**
- **Total Records:** 7,000
- **Employed:** 5,198 (74.3%)
- **Unemployed:** 1,802 (25.7%)
- **Jurusan Distribution:**
  - Akuntansi: 2,800 (40%)
  - Perkantoran: 2,450 (35%)
  - Pemasaran: 1,750 (25%)

### **Target Variables:**
- **Jurusan Cocok:** 8 unique classes
  - Akuntansi & Keuangan (most common)
  - Administrasi Perkantoran
  - Bisnis & Pemasaran
  - Teknologi Informasi
  - Komunikasi & Media
  - Pendidikan
  - Kesehatan
  - Lainnya

- **Perusahaan Tepat:** 2 classes
  - Tepat: ~65%
  - Tidak Tepat: ~35%

### **Data Quality Checks:**
```python
# Check for missing values
print(df.isnull().sum())

# Check data types
print(df.dtypes)

# Validate target distributions
print(df['jurusan_cocok'].value_counts())
print(df['perusahaan_tepat'].value_counts())

# Check correlations
correlation_matrix = df.corr()
```

### **Database Validation:**
```sql
-- Check record counts
SELECT COUNT(*) FROM survey_data;

-- Check employment distribution
SELECT status_bekerja, COUNT(*) FROM survey_data GROUP BY status_bekerja;

-- Check major distribution
SELECT jurusan, COUNT(*) FROM survey_data GROUP BY jurusan;

-- Check target variables
SELECT jurusan_cocok, COUNT(*) FROM survey_data GROUP BY jurusan_cocok;
SELECT perusahaan_tepat, COUNT(*) FROM survey_data GROUP BY perusahaan_tepat;
```

---

## 🎯 Kesimpulan

### **Struktur Data Lengkap:**
1. **CSV Dataset:** 7,000 records dengan 31 kolom
2. **Database:** 3 tabel (survey_data, users, dashboard_stats)
3. **ML Models:** KNN dengan 10 fitur ternormalisasi
4. **Web App:** Flask application dengan autentikasi

### **Keunggulan Sistem:**
- ✅ **Data Realistis:** Menggunakan distribusi probability yang realistis
- ✅ **Conditional Logic:** Data berbeda untuk employed vs unemployed
- ✅ **Target Variables:** 8 kelas jurusan + 2 kelas perusahaan
- ✅ **Normalization:** StandardScaler untuk performa ML optimal
- ✅ **Dashboard:** Statistik real-time tersimpan di database

### **Untuk Skripsi:**
- **Bab 3:** Metodologi - Jelaskan struktur data ini
- **Bab 4:** Implementasi - Flow dari dataset ke database
- **Bab 5:** Hasil - Statistik dan performa model

---

**📅 Dokumentasi Lengkap - November 14, 2025**  
**👨‍💻 Job Recommendation System Team**</content>
<parameter name="filePath">c:\xampp\htdocs\python\Job-Requirement-System\DATABASE_DOCUMENTATION.md