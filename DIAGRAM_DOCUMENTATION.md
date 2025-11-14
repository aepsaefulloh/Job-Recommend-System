# 📋 DOKUMENTASI SISTEM UNTUK PEMBUATAN DIAGRAM UML & ERD

## Sistem Rekomendasi Pekerjaan Alumni SMK

**Dibuat untuk membantu AI dalam membuat:**
- ERD (Entity Relationship Diagram)
- LRS (Logical Relational Schema)
- Activity Diagram
- Sequence Diagram
- UML Class Diagram
- Use Case Diagram

---

## 🎯 **OVERVIEW SISTEM**

### **Nama Sistem:** Job Recommendation System
### **Domain:** Rekomendasi pekerjaan untuk alumni SMK
### **Teknologi:** Flask Web App + MySQL + Machine Learning (KNN)

### **Aktor Utama:**
1. **Alumni SMK** (User) - Mengisi survey dan mendapat rekomendasi
2. **Administrator** - Mengelola dashboard dan melihat analytics
3. **System** - ML models dan database

---

## 🗄️ **ENTITAS & ATRIBUT (UNTUK ERD & LRS)**

### **1. Entitas: SURVEY_DATA**
**Deskripsi:** Data survey alumni SMK
**Primary Key:** id (AUTO_INCREMENT)

#### **Atribut:**
| Atribut | Tipe Data | Constraint | Deskripsi |
|---------|-----------|------------|-----------|
| id | INT | PK, AUTO_INCREMENT | ID unik survey |
| email | VARCHAR(120) | UNIQUE, NOT NULL | Email alumni |
| nama | VARCHAR(100) | NOT NULL | Nama lengkap |
| tempat_tinggal | VARCHAR(50) | NOT NULL | Kota domisili |
| jurusan | VARCHAR(50) | NOT NULL | Jurusan SMK |
| status_bekerja | VARCHAR(10) | NOT NULL | 'Ya'/'Tidak' |

#### **Employment Data (Conditional):**
| Atribut | Tipe Data | Constraint | Deskripsi |
|---------|-----------|------------|-----------|
| profesi_sekarang | VARCHAR(100) | NULL | Posisi saat ini |
| tempat_kerja | VARCHAR(100) | NULL | Lokasi kerja |
| cara_mendapat_pekerjaan | TEXT | NULL | Cara mendapat kerja |
| kemudahan_cari_kerja | VARCHAR(20) | NULL | 'Mudah'/'Sulit' |
| bantuan_sekolah | VARCHAR(10) | NULL | 'Ya'/'Tidak' |
| kesesuaian_minat | VARCHAR(20) | NULL | 'Sesuai'/'Tidak sesuai' |
| waktu_kerja_pertama | FLOAT | NULL | Waktu tunggu (bulan) |
| jenis_perusahaan | VARCHAR(50) | NULL | 'BUMN'/'PNS'/'Swasta' |
| kesesuaian_jurusan | VARCHAR(10) | NULL | 'Ya'/'Tidak' |
| kepuasan | VARCHAR(20) | NULL | 'Puas'/'Tidak puas' |
| lama_kerja_1 | FLOAT | NULL | Lama kerja (tahun) |
| lama_kerja_2 | FLOAT | NULL | Total pengalaman |
| nyaman | VARCHAR(10) | NULL | 'Ya'/'Tidak' |
| gaji | FLOAT | NULL | Gaji dalam Rupiah |

#### **Unemployment Data (Conditional):**
| Atribut | Tipe Data | Constraint | Deskripsi |
|---------|-----------|------------|-----------|
| alasan_belum_kerja | VARCHAR(100) | NULL | Alasan belum kerja |
| kendala_utama | VARCHAR(100) | NULL | Kendala utama |
| ikut_pelatihan | VARCHAR(10) | NULL | 'Ya'/'Tidak' |

#### **Prediction Results:**
| Atribut | Tipe Data | Constraint | Deskripsi |
|---------|-----------|------------|-----------|
| jurusan_cocok | VARCHAR(50) | NULL | Rekomendasi jurusan (8 kategori) |
| perusahaan_tepat | VARCHAR(20) | NULL | 'Tepat'/'Tidak Tepat' |

#### **Metadata:**
| Atribut | Tipe Data | Constraint | Default |
|---------|-----------|------------|---------|
| created_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP |

### **2. Entitas: USERS**
**Deskripsi:** Data pengguna untuk autentikasi
**Primary Key:** id (AUTO_INCREMENT)

| Atribut | Tipe Data | Constraint | Deskripsi |
|---------|-----------|------------|-----------|
| id | INT | PK, AUTO_INCREMENT | ID unik user |
| username | VARCHAR(80) | UNIQUE, NOT NULL | Username login |
| email | VARCHAR(120) | UNIQUE, NOT NULL | Email user |
| password | VARCHAR(128) | NOT NULL | Password hash |
| full_name | VARCHAR(100) | NOT NULL | Nama lengkap |
| role | VARCHAR(20) | NOT NULL | 'admin'/'user' |
| is_active | BOOLEAN | NOT NULL | Status aktif |
| created_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP |
| last_login | DATETIME | NULL | Waktu login terakhir |

### **3. Entitas: DASHBOARD_STATS**
**Deskripsi:** Cache statistik untuk dashboard
**Primary Key:** id (AUTO_INCREMENT)

| Atribut | Tipe Data | Constraint | Deskripsi |
|---------|-----------|------------|-----------|
| id | INT | PK, AUTO_INCREMENT | ID unik stat |
| stat_name | VARCHAR(50) | UNIQUE, NOT NULL | Nama statistik |
| stat_value | FLOAT | NOT NULL | Nilai statistik |
| stat_type | VARCHAR(20) | NOT NULL | 'count'/'percentage'/'average' |
| updated_at | DATETIME | NOT NULL | CURRENT_TIMESTAMP |

---

## 🔗 **HUBUNGAN ANTAR ENTITAS (UNTUK ERD)**

### **Relasi Utama:**

1. **USERS → SURVEY_DATA**
   - **Type:** One-to-Many (1:N)
   - **Cardinality:** Satu user bisa memiliki banyak survey
   - **Foreign Key:** Tidak ada (email sebagai identifier)
   - **Business Rule:** User bisa mengisi multiple survey

2. **SURVEY_DATA → DASHBOARD_STATS**
   - **Type:** Many-to-One (N:1)
   - **Cardinality:** Banyak survey menghasilkan satu statistik
   - **Foreign Key:** Tidak ada (computed relationship)
   - **Business Rule:** Stats dihitung dari semua survey data

### **Relasi Sekunder:**

3. **USERS (role) → DASHBOARD_STATS**
   - **Type:** Conditional Access
   - **Condition:** Hanya admin yang bisa akses stats
   - **Business Rule:** Role-based access control

---

## 📊 **LOGICAL RELATIONAL SCHEMA (LRS)**

### **Tabel Normalisasi:**

#### **1. SURVEY_DATA (1NF, 2NF, 3NF)**
```
SURVEY_DATA (
    id (PK),
    email (UK),
    nama,
    tempat_tinggal,
    jurusan,
    status_bekerja,
    profesi_sekarang,
    tempat_kerja,
    cara_mendapat_pekerjaan,
    kemudahan_cari_kerja,
    bantuan_sekolah,
    kesesuaian_minat,
    waktu_kerja_pertama,
    jenis_perusahaan,
    kesesuaian_jurusan,
    kepuasan,
    lama_kerja_1,
    lama_kerja_2,
    nyaman,
    gaji,
    alasan_belum_kerja,
    kendala_utama,
    ikut_pelatihan,
    jurusan_cocok,
    perusahaan_tepat,
    created_at,
    updated_at
)
```

#### **2. USERS (1NF, 2NF, 3NF)**
```
USERS (
    id (PK),
    username (UK),
    email (UK),
    password,
    full_name,
    role,
    is_active,
    created_at,
    last_login
)
```

#### **3. DASHBOARD_STATS (1NF, 2NF, 3NF)**
```
DASHBOARD_STATS (
    id (PK),
    stat_name (UK),
    stat_value,
    stat_type,
    updated_at
)
```

### **Functional Dependencies:**
- `id → all attributes` (SURVEY_DATA)
- `username → id, email, password, full_name, role, is_active, created_at, last_login` (USERS)
- `stat_name → id, stat_value, stat_type, updated_at` (DASHBOARD_STATS)

---

## 🔄 **USE CASE & AKTIVITAS (UNTUK ACTIVITY DIAGRAM)**

### **Use Case Diagram:**

#### **Aktor: Alumni SMK**
1. **UC-001:** Mengisi Survey Pekerjaan
   - Precondition: User belum login
   - Postcondition: Mendapat rekomendasi pekerjaan

2. **UC-002:** Melihat Hasil Rekomendasi
   - Precondition: Survey sudah diisi
   - Postcondition: Menampilkan rekomendasi jurusan & perusahaan

#### **Aktor: Administrator**
3. **UC-003:** Login ke Dashboard
   - Precondition: Valid credentials
   - Postcondition: Akses dashboard admin

4. **UC-004:** Melihat Dashboard Analytics
   - Precondition: Admin logged in
   - Postcondition: Menampilkan statistik & charts

5. **UC-005:** Filter Data Survey
   - Precondition: Admin logged in
   - Postcondition: Data terfilter berdasarkan kriteria

### **Activity Diagram - Main Flow:**

```
1. User mengakses homepage
   ├── Input: URL (/)
   └── Output: Form survey

2. User mengisi form survey
   ├── Section 1: Info dasar
   ├── Section 2: Jika sudah bekerja
   └── Section 3: Jika belum bekerja

3. System memproses form
   ├── Validate input
   ├── Preprocess data
   └── Generate features

4. ML Prediction
   ├── Load KNN models
   ├── Scale features
   ├── Predict jurusan_cocok
   └── Predict perusahaan_tepat

5. Generate recommendations
   ├── Job recommendations
   ├── Career advice
   └── Display results

6. Save to database (optional)
   └── Store survey + predictions
```

---

## 📡 **SEQUENCE DIAGRAM - INTERAKSI KOMPONEN**

### **Sequence Diagram 1: User Survey & Prediction**

```
User Browser → Flask App (app.py)
    ├── GET / (homepage)
    └── POST /result (submit survey)

Flask App → predictor.py
    ├── preprocess_form_data()
    └── make_predictions()

predictor.py → ML Models
    ├── Load scaler.pkl
    ├── Load knn_jurusan_model.pkl
    ├── Load knn_perusahaan_model.pkl
    └── Generate predictions

ML Models → predictor.py
    └── Return predictions

predictor.py → Flask App
    └── Return results

Flask App → Database (Optional)
    └── Save survey data

Flask App → User Browser
    └── Render result.html
```

### **Sequence Diagram 2: Admin Dashboard**

```
Admin Browser → Flask App (app.py)
    ├── GET /login
    └── POST /login (authenticate)

Flask App → Database (users table)
    └── Validate credentials

Flask App → Admin Browser
    ├── Redirect to /dashboard
    └── GET /dashboard

Flask App → Database (survey_data, dashboard_stats)
    ├── Query survey data
    └── Query statistics

Flask App → Admin Browser
    └── Render dashboard.html with data
```

### **Sequence Diagram 3: Data Import Process**

```
setup_database.py → MySQL Server
    ├── CREATE DATABASE
    └── CREATE TABLES

setup_database.py → job_survey.csv
    └── Read CSV data

setup_database.py → MySQL Server
    ├── INSERT survey_data
    ├── INSERT dashboard_stats
    └── COMMIT transaction

setup_database.py → Console
    └── Print success message
```

---

## 🏗️ **UML CLASS DIAGRAM**

### **Class: SurveyData**
```
+---------------------+
|    SurveyData       |
+---------------------+
| - id: int           |
| - email: string     |
| - nama: string      |
| - tempat_tinggal: string |
| - jurusan: string   |
| - status_bekerja: string |
+---------------------+
| + save(): void      |
| + update(): void    |
| + delete(): void    |
+---------------------+
```

### **Class: User**
```
+---------------------+
|       User          |
+---------------------+
| - id: int           |
| - username: string  |
| - email: string     |
| - password: string  |
| - role: string      |
| - is_active: bool   |
+---------------------+
| + set_password(): void |
| + check_password(): bool |
| + login(): void     |
+---------------------+
```

### **Class: DashboardStats**
```
+---------------------+
|  DashboardStats     |
+---------------------+
| - id: int           |
| - stat_name: string |
| - stat_value: float |
| - stat_type: string |
+---------------------+
| + update(): void    |
| + calculate(): void |
+---------------------+
```

### **Class: Predictor**
```
+---------------------+
|     Predictor       |
+---------------------+
| - knn_jurusan: model|
| - knn_perusahaan: model |
| - scaler: StandardScaler |
| - encoders: dict    |
+---------------------+
| + preprocess_data(): dict |
| + make_predictions(): dict |
| + encode_features(): array |
+---------------------+
```

### **Relationships:**
- `User` 1..* ----> `SurveyData` (One-to-Many)
- `SurveyData` ----> `DashboardStats` (Data source)
- `Predictor` ----> `SurveyData` (Uses for prediction)

---

## 🔄 **ACTIVITY DIAGRAM DETAIL**

### **Activity Diagram: Complete User Journey**

```
Start: User visits website

1. [Homepage]
   ├── Display survey form
   ├── User fills Section 1 (Basic Info)
   └── Decision: Status Bekerja?

2. [Branch: Sudah Bekerja]
   ├── Fill Section 2 (Employment)
   ├── Validate employment fields
   └── Proceed to prediction

3. [Branch: Belum Bekerja]
   ├── Fill Section 3 (Unemployment)
   ├── Validate unemployment fields
   └── Proceed to prediction

4. [Data Preprocessing]
   ├── Clean form data
   ├── Encode categorical features
   ├── Scale numerical features
   └── Prepare feature array

5. [ML Prediction]
   ├── Load KNN models
   ├── Predict jurusan_cocok
   ├── Predict perusahaan_tepat
   └── Generate confidence scores

6. [Generate Recommendations]
   ├── Map predictions to job recommendations
   ├── Create career advice
   └── Format display data

7. [Display Results]
   ├── Show user profile
   ├── Display job recommendations
   ├── Show prediction confidence
   └── Offer to save data

8. [Optional: Save to Database]
   ├── Store survey data
   ├── Store predictions
   └── Update dashboard stats

End: User sees recommendations
```

### **Activity Diagram: Admin Dashboard**

```
Start: Admin login

1. [Login Process]
   ├── Enter credentials
   ├── Validate against database
   └── Check role permissions

2. [Dashboard Access]
   ├── Load dashboard page
   ├── Query survey statistics
   └── Load chart data

3. [Data Visualization]
   ├── Generate employment rate chart
   ├── Generate major distribution chart
   ├── Generate location charts
   └── Generate salary statistics

4. [Data Management]
   ├── Display data table
   ├── Enable filtering options
   └── Allow data export

5. [Real-time Updates]
   ├── Auto-refresh statistics
   ├── Update on new data
   └── Cache performance

End: Admin monitors system
```

---

## 📋 **DATA FLOW & BUSINESS RULES**

### **Business Rules:**

1. **Survey Validation:**
   - Email harus unik
   - Jurusan harus salah satu dari 3 pilihan
   - Status bekerja menentukan section berikutnya

2. **Prediction Logic:**
   - KNN dengan 10 features ternormalisasi
   - Jurusan cocok: 8 kategori berdasarkan SMK major
   - Perusahaan tepat: Binary classification

3. **Access Control:**
   - Admin: Full dashboard access
   - User: Survey access only
   - Guest: Read-only access

4. **Data Integrity:**
   - Foreign key constraints
   - Data validation pada form
   - Error handling untuk missing data

### **Data Constraints:**

1. **Domain Constraints:**
   - jurusan ∈ {'Akuntansi', 'Perkantoran', 'Pemasaran'}
   - status_bekerja ∈ {'Ya', 'Tidak'}
   - role ∈ {'admin', 'user'}

2. **Range Constraints:**
   - gaji > 0
   - lama_kerja_1 >= 0
   - waktu_kerja_pertama >= 0

3. **Referential Integrity:**
   - User email harus exist sebelum survey
   - Stats calculated from survey_data

---

## 🎯 **GUIDELINES UNTUK AI PEMBUAT DIAGRAM**

### **Untuk ERD:**
- Gunakan crow's foot notation
- Show cardinality (1:1, 1:N, N:M)
- Include all entities dan attributes
- Show primary keys dan foreign keys
- Add relationship names

### **Untuk Sequence Diagram:**
- Show chronological order
- Include all system components
- Show method calls dan returns
- Add activation bars
- Include error handling paths

### **Untuk Activity Diagram:**
- Use swimlanes untuk aktor berbeda
- Show decision points
- Include parallel activities
- Add guards pada transitions
- Show start dan end states

### **Untuk UML Class:**
- Show attributes dengan visibility
- Include methods dengan parameters
- Show inheritance jika ada
- Add multiplicities pada associations
- Include constraints

---

**📅 Dibuat:** November 14, 2025  
**🎯 Tujuan:** Membantu AI membuat diagram UML & ERD yang akurat  
**📋 Coverage:** Complete system documentation for diagram generation</content>
<parameter name="filePath">c:\xampp\htdocs\python\Job-Requirement-System\DIAGRAM_DOCUMENTATION.md