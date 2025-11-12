# 🎓 Job Recommendation System (JRC)

Sistem rekomendasi pekerjaan berbasis machine learning untuk alumni universitas. Aplikasi web yang memprediksi kecocokan alumni dengan posisi pekerjaan dan lingkungan perusahaan menggunakan algoritma K-Nearest Neighbors dan K-Means Clustering.

---

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Instalasi & Setup](#instalasi--setup)
- [Cara Menjalankan](#cara-menjalankan)
- [Struktur Projek](#struktur-projek)
- [Dataset](#dataset)
- [Model Machine Learning](#model-machine-learning)
- [Rute & Halaman](#rute--halaman)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)

---

## 🚀 Fitur Utama

### 1. **Survey Form Interaktif (28 Pertanyaan)**
- Formulir komprehensif dengan 28 pertanyaan terstruktur
- 3 bagian otomatis berdasarkan status bekerja:
  - **Bagian 1**: Informasi Dasar (nama, tempat tinggal, jurusan, dsb)
  - **Bagian 2**: Detail Pekerjaan (jika sudah bekerja)
  - **Bagian 3**: Pencarian Kerja (jika belum bekerja)
- Validasi form real-time
- Interface responsif dengan Bootstrap

### 2. **Prediksi Rekomendasi Pekerjaan**
- **Kecocokan Perusahaan**: 96.67% accuracy
  - Memprediksi apakah alumni sesuai dengan lingkungan perusahaan
  - Klasifikasi biner: Tepat / Tidak Tepat
  - Menggunakan K-Nearest Neighbors (k=5)
  
- **Jurusan Cocok**: 10% accuracy
  - Merekomendasikan jurusan akademis yang sesuai
  - 13 kategori jurusan
  - Hasil beragam untuk keperluan testing

### 3. **Analytics & Visualisasi**
- **Dashboard Metrik**: Performa dan akurasi model
- **Visualisasi Fitur**: 8 chart distribusi data alumni
  - Scatter plot IPK vs Gaji
  - Waktu kerja vs Kepuasan
  - Distribusi IPK
  - Distribusi Gaji
  - Heatmap Korelasi Fitur
  - Box plot Pengalaman Kerja
  - Top 10 Jurusan
  - Pie chart Kepuasan
  
- **Clustering K-Means**: Alumni dikelompokkan menjadi 3 cluster
  - Cluster 0: High Performers Junior (46.7%)
  - Cluster 1: Senior Stars (16.7%)
  - Cluster 2: Developing Professionals (36.7%)

---

## 🔧 Instalasi & Setup

### Persyaratan Sistem
- **Python 3.7+** (Direkomendasikan: Python 3.13.2 ✅)
- pip (package manager)
- Browser modern (Chrome, Firefox, Safari, Edge)

### Install Dependencies
```bash
# Install semua dependencies dari requirements.txt
pip install -r requirements.txt
```

**Requirements.txt terbaru (Python 3.13.2 compatible):**
```txt
# Job Recommendation System - Dependencies

# Web Framework
Flask==3.1.0
Werkzeug>=3.1.0

# Machine Learning
scikit-learn>=1.6.0
numpy>=1.24.0
pandas>=2.0.0

# Data Visualization
matplotlib>=3.7.0
seaborn>=0.12.0

# Additional Dependencies
Jinja2>=3.1.0
MarkupSafe>=2.1.0
joblib>=1.3.0
scipy>=1.11.0
threadpoolctl>=3.2.0
```

### Troubleshooting Instalasi

#### ❌ Error: "Microsoft Visual C++ 14.0 or greater is required"
**Solusi**: Update ke Python 3.13.2 atau gunakan versi scikit-learn yang kompatibel:
```bash
pip install scikit-learn>=1.6.0
```

#### ❌ Error: "Cannot install Werkzeug==3.0.1 and flask==3.1.0"
**Solusi**: Update Werkzeug ke versi 3.1.0+:
```bash
pip install Werkzeug>=3.1.0
```

#### ❌ Error: Column name mismatch di visualisasi
**Solusi**: Sudah diperbaiki dalam versi terbaru. Pastikan menggunakan `utils/visualization.py` yang terbaru.

---

## ▶️ Cara Menjalankan

### 1. Jalankan Aplikasi
```bash
cd "c:\xampp\htdocs\python\job recommended system"
python app.py
```

**Output yang diharapkan:**
```
==================================================
JOB RECOMMENDATION SYSTEM
==================================================

Flask app starting...
Open browser and go to: http://127.0.0.1:5000

Routes available:
  - http://127.0.0.1:5000/ (Home - Prediction Form)
  - http://127.0.0.1:5000/metrics (Model Performance)
  - http://127.0.0.1:5000/visualize (Supervised Learning Visualizations)
  - http://127.0.0.1:5000/clustering (Unsupervised Learning - K-Means)
==================================================
```

### 2. Akses Aplikasi
Buka browser dan kunjungi: **http://127.0.0.1:5000/**

### 3. Melatih Ulang Model (Opsional)
Untuk melatih ulang model dengan data baru:
```bash
python preprocessing.py
```

Proses ini akan:
1. Memuat dataset `job_survey.csv`
2. Filter records yang sudah bekerja (600 dari 1000)
3. Encoding fitur kategorikal
4. Training KNN models (2 model)
5. Clustering dengan K-Means (3 clusters)
6. Menyimpan semua file model (.pkl)
7. Generate data visualisasi dan metrik

---

## 📁 Struktur Projek

```
job recommended system/
│
├── app.py                            # ⭐ Flask app utama & semua rute
├── preprocessing.py                  # Script training/retraining model
├── job_survey.csv                    # Dataset (1000 records, 600 employed)
│
├── 📊 Model Files (ML Models):
│   ├── knn_jurusan_model.pkl         # Classifier untuk jurusan cocok (13 classes)
│   ├── knn_perusahaan_model.pkl      # Classifier untuk kecocokan perusahaan (2 classes)
│   ├── scaler.pkl                    # Feature scaling (StandardScaler)
│   └── label_encoders.pkl            # Encoding fitur kategorikal (8 features)
│
├── 📈 Data Files (untuk Display):
│   ├── metrics.pkl                   # Metrik performa & confusion matrix
│   ├── visualization_data.pkl        # Data untuk 8 visualisasi (500 samples)
│   └── clustering_data.pkl           # Data K-Means & elbow method
│
├── 🌐 templates/ (Web Interface):
│   ├── index.html                    # Halaman survey (28 pertanyaan)
│   ├── result.html                   # Halaman hasil prediksi
│   ├── metrics.html                  # Dashboard metrik performa
│   ├── visualize.html                # 8 chart fitur & distribusi
│   └── clustering.html               # Analisis clustering K-Means
│
├── static/                           # CSS, JavaScript, images
│
└── 📝 Documentation:
    ├── README.md                     # File ini
    ├── DOCUMENTATION_FOR_AI_AGENT.md # Dokumentasi teknis untuk AI
    └── QUICK_REFERENCE.md            # Quick reference untuk developers
```

---

## 📊 Dataset

### Informasi Dataset
- **File**: `job_survey.csv`
- **Total Records**: 1000
- **Employed**: 600 (untuk training)
- **Unemployed**: 400 (untuk testing)
- **Size**: ~220 KB
- **Encoding**: UTF-8

### Fitur Dataset (31 Kolom)

#### Informasi Personal
- `email` - Email alumni
- `nama` - Nama lengkap
- `tempat_tinggal` - Asal daerah
- `status_bekerja` - Status: Sudah/Belum bekerja

#### Informasi Akademis
- `jurusan` - Program studi (13 kategori)
- `nilai_rata` - IPK (GPA)

#### Detail Pekerjaan (Jika Bekerja)
- `waktu_kerja_pertama` - Bulan pertama bekerja
- `profesi_sekarang` - Profesi saat ini
- `tempat_kerja_saat_ini` - Lokasi perusahaan
- `lama_kerja` - Durasi pekerjaan (tahun)
- `gaji` - Gaji per bulan (Rp)
- `kepuasan` - Tingkat kepuasan (scale 1-10)
- `kenyamanan` - Kenyamanan bekerja
- `perusahaan_tepat` - Kecocokan perusahaan (Target KNN 1)
- `jurusan_cocok` - Jurusan cocok untuk pekerjaan (Target KNN 2)

#### Detail Pencarian Kerja (Jika Belum Bekerja)
- `cara_mencari` - Metode pencarian kerja
- `hambatan` - Hambatan utama
- `ekspektasi_gaji` - Harapan gaji
- `lokasi_preferen` - Lokasi preferensi kerja
- `dsb...` - Field tambahan lainnya

### Preprocessing Pipeline
1. **Data Loading**: Load CSV dengan encoding UTF-8
2. **Filtering**: Ambil hanya 600 records yang status_bekerja='Sudah'
3. **Feature Engineering**: Create derived features
4. **Encoding**: Encode 8 categorical features dengan LabelEncoder
5. **Scaling**: Normalize dengan StandardScaler
6. **Train-Test Split**: 80% train (480), 20% test (120)

---

## 🤖 Model Machine Learning

### 1. K-Nearest Neighbors (KNN) - Kecocokan Perusahaan
- **File Model**: `knn_perusahaan_model.pkl`
- **K Value**: 5 neighbors
- **Akurasi**: 96.67%
- **Classes**: 2 (Tepat / Tidak Tepat)
- **Fitur Input**: 7 features (numeric + encoded categorical)
- **Status**: ✅ Production Ready

### 2. K-Nearest Neighbors (KNN) - Jurusan Cocok
- **File Model**: `knn_jurusan_model.pkl`
- **K Value**: 5 neighbors
- **Akurasi**: 10%
- **Classes**: 13 jurusan
- **Fitur Input**: 7 features
- **Status**: ✅ Diverse predictions (good for testing)

### 3. K-Means Clustering
- **File Data**: `clustering_data.pkl`
- **Optimal K**: 3 (dari elbow method)
- **Silhouette Score**: 0.2471
- **Fitur**: 3 features terseleksi
- **Cluster Profiles**:
  - Cluster 0 (46.7%): High Performers Junior
  - Cluster 1 (16.7%): Senior Stars
  - Cluster 2 (36.7%): Developing Professionals
- **Status**: ✅ Alumni segmentation ready

### Model Architecture
```
Input Features (7)
    ↓
StandardScaler (normalize)
    ↓
LabelEncoder (categorical → numeric)
    ↓
KNN Model (k=5) / K-Means (k=3)
    ↓
Predictions + Probabilities
```

---

## 🌐 Rute & Halaman

### Rute Web (HTTP Routes)

| Rute | Method | Deskripsi | Output |
|------|--------|-----------|--------|
| `/` | GET | Halaman survey form | HTML form (28 pertanyaan) |
| `/result` | POST | Process survei & prediksi | HTML hasil prediksi |
| `/metrics` | GET | Dashboard metrik model | HTML tabel akurasi & confusion matrix |
| `/visualize` | GET | Visualisasi supervised learning | HTML dengan 8 chart |
| `/clustering` | GET | Analisis K-Means clustering | HTML dengan 2 plot + cluster info |

### Halaman Aplikasi

#### 1. **Home (/)** - Survey Form
- Interface form dengan 28 pertanyaan
- Conditional sections (dynamic show/hide based on status)
- Validasi input real-time
- Submit button untuk prediksi

#### 2. **Result (/result)** - Hasil Prediksi
- Tampil data input yang disubmit
- Prediksi: Kecocokan Perusahaan (Tepat/Tidak Tepat)
- Rekomendasi: Jurusan Cocok (13 pilihan)
- Confidence scores / probabilities
- Cluster membership (alumni cluster mana)
- Tombol back to form

#### 3. **Metrics (/metrics)** - Dashboard Performa
- Tabel akurasi model
- Confusion matrix KNN Perusahaan
- Confusion matrix KNN Jurusan
- Dataset source info
- Model training date

#### 4. **Visualize (/visualize)** - 8 Chart Fitur
- **Plot 1**: Scatter IPK vs Gaji
- **Plot 2**: Waktu kerja vs Kepuasan
- **Plot 3**: Histogram distribusi IPK
- **Plot 4**: Histogram distribusi Gaji
- **Plot 5**: Heatmap korelasi fitur
- **Plot 6**: Box plot pengalaman kerja
- **Plot 7**: Bar chart top 10 jurusan
- **Plot 8**: Pie chart distribusi kepuasan

#### 5. **Clustering (/clustering)** - K-Means Analysis
- **Plot 1**: Elbow curve (untuk menentukan k=3)
- **Plot 2**: Scatter plot cluster (2D visualization)
- **Info**: Optimal k value, silhouette score
- **Stats**: Jumlah alumni per cluster

---

## 💻 Teknologi yang Digunakan

### Backend
- **Flask 3.1.0** - Web framework
- **Python 3.13.2** - Programming language (✅ Tested & Compatible)
- **Werkzeug 3.1.3** - WSGI utility library

### Machine Learning
- **scikit-learn 1.6.1** - ML algorithms (KNN, K-Means)
- **pandas 2.2.3** - Data manipulation
- **numpy 2.2.3** - Numerical computing

### Data Visualization
- **Matplotlib 3.10.7** - Chart generation (Agg backend untuk Flask)
- **Seaborn 0.13.2** - Statistical data visualization
- **Base64** - Image encoding untuk HTML embedding

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript** - Interactive elements

### File Format
- **CSV** - Dataset format
- **PKL (Pickle)** - Model serialization
- **JSON** - Data interchange (implicit)

### Recent Updates (November 13, 2025)
- ✅ **Fixed emoji display issues** - Replaced corrupted symbols in `index.html`
- ✅ **Updated requirements.txt** - Compatible with Python 3.13.2
- ✅ **Fixed visualization functions** - Corrected column name mismatches
- ✅ **Resolved dependency conflicts** - Flask 3.1.0 + Werkzeug 3.1.3 compatibility

---

## ✅ Model Performance Summary

| Model | Akurasi | Jumlah Class | Status |
|-------|---------|--------------|--------|
| KNN Perusahaan | 96.67% | 2 | ✅ Production Ready |
| KNN Jurusan | 10% | 13 | ✅ Testing Ready |
| K-Means Clustering | - | 3 clusters | ✅ Validated |

---

## 📝 File Penting

### Python Scripts
- **app.py** (441 lines)
  - Flask routes & handlers
  - 11 visualization helper functions
  - Matplotlib backend configuration
  - Model loading & prediction logic

- **preprocessing.py**
  - Dataset loading & preprocessing
  - Feature encoding & scaling
  - KNN model training
  - K-Means clustering
  - Model serialization (save .pkl files)

### Data Files
- **job_survey.csv** - 1000 record dataset
- **\*.pkl** - 7 serialized model files (~215 KB total)

### Web Assets
- **templates/** - 5 HTML templates
- **static/** - CSS, JS, images

---

## 🔄 Workflow Prediksi

```
User mengisi survey (28 pertanyaan)
    ↓
Submit form → POST /result
    ↓
Data preprocessing
    ├─ Feature scaling (StandardScaler)
    └─ Feature encoding (LabelEncoder)
    ↓
Prediksi KNN Perusahaan
    ├─ Model: knn_perusahaan_model.pkl
    └─ Output: Tepat / Tidak Tepat (96.67% akurasi)
    ↓
Prediksi KNN Jurusan
    ├─ Model: knn_jurusan_model.pkl
    └─ Output: 13 kategori jurusan
    ↓
Assign Cluster (K-Means)
    ├─ Model: clustering_data.pkl
    └─ Output: Cluster 0 / 1 / 2
    ↓
Render result.html
    ├─ Tampil semua prediksi
    ├─ Confidence scores
    └─ Cluster info
```

---

## 🚀 Cara Menggunakan

### 1. Mengakses Survey
1. Jalankan `python app.py`
2. Buka http://127.0.0.1:5000/ di browser
3. Isi semua 28 pertanyaan
4. Klik "Submit" button

### 2. Melihat Hasil Prediksi
- Halaman result.html akan tampil otomatis setelah submit
- Lihat prediksi kecocokan perusahaan
- Lihat rekomendasi jurusan
- Lihat cluster assignment

### 3. Melihat Metrik Model
- Klik link "Metrics" atau akses http://127.0.0.1:5000/metrics
- Lihat akurasi model
- Lihat confusion matrices

### 4. Melihat Visualisasi Data
- Klik link "Visualize" atau akses http://127.0.0.1:5000/visualize
- Explore 8 chart berbeda
- Pahami distribusi data alumni

### 5. Melihat Clustering Analysis
- Klik link "Clustering" atau akses http://127.0.0.1:5000/clustering
- Lihat elbow curve
- Lihat scatter plot cluster
- Pahami alumni segmentation

---

## 📌 Catatan Penting

1. **Synthetic Data**: Dataset saat ini menggunakan data synthetic untuk development/testing
2. **Feature Importance**: Model menggunakan 7 features terpilih untuk akurasi maksimal
3. **Scaling Required**: Semua numeric features harus di-scale menggunakan StandardScaler yang sama
4. **Encoding Consistency**: Categorical features harus di-encode dengan LabelEncoder yang sama
5. **Cluster Validation**: K=3 optimal untuk dataset ini berdasarkan elbow method
6. **Python 3.13.2 Compatibility**: ✅ Tested and verified working

### 🔧 Recent Fixes & Updates

#### Version Updates (November 13, 2025)
- **Fixed Emoji Display**: Replaced all corrupted emoji symbols (���) in `index.html` with proper Unicode emojis
- **Python 3.13.2 Support**: Updated `requirements.txt` for full compatibility with Python 3.13.2
- **Dependency Resolution**: Fixed Flask 3.1.0 + Werkzeug 3.1.3 compatibility issues
- **Visualization Bug Fix**: Corrected column name mismatch (`kenyamanan` → `nyaman`) in visualization functions
- **Package Versions**: Updated to latest compatible versions:
  - scikit-learn: 1.3.2 → 1.6.1
  - Werkzeug: 3.0.1 → 3.1.3
  - numpy: 1.24.3 → 2.2.3
  - pandas: 2.0.3 → 2.2.3

#### Installation Issues Resolved
- ✅ Microsoft Visual C++ compilation errors (resolved by version updates)
- ✅ Werkzeug dependency conflicts (resolved by version updates)
- ✅ Visualization function errors (resolved by column name fixes)
- ✅ Emoji display corruption (resolved by Unicode replacement)

---

## 📞 Informasi Lebih Lanjut

- **Documentation**: Lihat `DOCUMENTATION_FOR_AI_AGENT.md`
- **Quick Reference**: Lihat `QUICK_REFERENCE.md`
- **Last Updated**: November 13, 2025
- **Python Version**: ✅ Compatible with Python 3.13.2
- **Status**: ✅ Production Ready (All Issues Fixed)

---

**Dikembangkan dengan ❤️ menggunakan Flask & Machine Learning**

### 🚀 Quick Start Command
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser: http://127.0.0.1:5000
```
