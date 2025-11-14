# 🎓 Job Recommendation System with Admin Dashboard

Sistem rekomendasi pekerjaan berbasis machine learning untuk alumni universitas dengan **Dashboard Admin** untuk monitoring data survey. Aplikasi web lengkap yang memprediksi kecocokan alumni dengan posisi pekerjaan dan menyediakan analytics dashboard untuk administrator.

---

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Instalasi & Setup](#instalasi--setup)
- [Database Setup](#database-setup)
- [Cara Menjalankan](#cara-menjalankan)
- [Dashboard Admin](#dashboard-admin)
- [Struktur Projek](#struktur-projek)
- [Dataset](#dataset)
- [Model Machine Learning](#model-machine-learning)
- [Rute & Halaman](#rute--halaman)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)

---

## 🚀 Fitur Utama

### 1. **Survey Form Interaktif (28 Pertanyaan)**
- Formulir komprehensif dengan 28 pertanyaan terstruktur
- 3 bagian otomatis berdasarkan status bekerja
- Validasi form real-time
- Interface responsif dengan TailwindCSS

### 2. **Prediksi Rekomendasi Pekerjaan**
- **Kecocokan Perusahaan**: 96.67% accuracy (KNN)
- **Jurusan Cocok**: 13 kategori jurusan
- Hasil disimpan ke database MySQL

### 3. **Dashboard Admin dengan Authentication**
- ✅ **Login/Register System** - User authentication dengan Flask-Login
- ✅ **Dashboard Analytics** - Real-time statistics dari survey data
- ✅ **Data Table** - Paginated table dengan 3000+ records
- ✅ **Interactive Charts** - Chart.js untuk visualisasi data
- ✅ **Advanced Filtering** - Filter by status, jurusan, lokasi, perusahaan
- ✅ **MySQL Database** - XAMPP MySQL integration
- ✅ **Role-based Access** - Admin dan user roles

### 4. **Analytics & Visualisasi**
- Dashboard metrik performa model
- 8 chart distribusi data alumni
- K-Means clustering analysis

---

## 🔧 Instalasi & Setup

### Persyaratan Sistem
- **Python 3.7+** (Direkomendasikan: Python 3.13.2 ✅)
- **XAMPP** dengan MySQL aktif
- pip (package manager)
- Browser modern

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables
File `.env` sudah tersedia dengan konfigurasi default:
```env
# Database Configuration (XAMPP MySQL)
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=job_recommendation_db

# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
```

### 3. Setup Database
```bash
# Jalankan setup database (akan membuat tabel dan import data)
python setup_database.py
```

**Output yang diharapkan:**
```
============================================================
JOB RECOMMENDATION SYSTEM - DATABASE SETUP
============================================================
✓ Database 'job_recommendation_db' created or already exists
✓ All tables created successfully
✓ Loaded 3000 records from job_survey.csv
✓ Successfully imported 3000 survey records
✓ Dashboard statistics updated
✅ DATABASE SETUP COMPLETED SUCCESSFULLY!
============================================================
```

### 4. Create Admin User
```bash
# Buat user admin default
python -c "
from app import app, db
from models import User
with app.app_context():
    admin = User(username='admin', email='admin@example.com', full_name='Administrator', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('Admin user created: admin/admin123')
"
```

---

## 🗄️ Database Setup

### Database Schema
- **users**: User authentication (id, username, email, password_hash, role)
- **survey_data**: Survey responses (3000 records, 31 columns)
- **dashboard_stats**: Cached statistics untuk dashboard

### Default Admin Account
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator

### Database Connection
- **Host**: localhost (XAMPP MySQL)
- **Database**: job_recommendation_db
- **User**: root
- **Password**: (empty)

---

## ▶️ Cara Menjalankan

### 1. Jalankan Aplikasi
```bash
python app.py
```

### 2. Akses Aplikasi
- **Home/Survey**: http://127.0.0.1:5000/
- **Login**: http://127.0.0.1:5000/login
- **Dashboard**: http://127.0.0.1:5000/dashboard (login required)

### 3. Login ke Dashboard
1. Buka http://127.0.0.1:5000/login
2. Login dengan: `admin` / `admin123`
3. Akses dashboard untuk melihat analytics

---

## 📊 Dashboard Admin

### Fitur Dashboard
- **📈 Real-time Statistics**: Total surveys, employment rate, avg salary
- **📊 Interactive Charts**: Major distribution, location, company types
- **📋 Data Table**: Paginated survey data (25 records per page)
- **🔍 Advanced Filtering**: Filter by employment status, major, location, company
- **👤 User Management**: Role-based access control

### Dashboard Routes
- `/login` - User login page
- `/register` - User registration
- `/dashboard` - Admin dashboard (login required)
- `/logout` - User logout

### Chart.js Visualizations
- **Major Distribution**: Top 10 jurusan alumni
- **Location Distribution**: Top 5 lokasi tinggal
- **Company Types**: Distribusi jenis perusahaan

---

## 📁 Struktur Projek

```
job-recommendation-system/
│
├── 🗄️ Database & Auth:
│   ├── models.py              # SQLAlchemy models (User, SurveyData, DashboardStats)
│   ├── forms.py               # WTForms (LoginForm, RegistrationForm, SurveyFilterForm)
│   ├── setup_database.py      # Database creation & data import
│   └── .env                   # Environment configuration
│
├── 🤖 ML Models:
│   ├── preprocessing.py       # Model training script
│   ├── knn_jurusan_model.pkl  # Jurusan prediction model
│   ├── knn_perusahaan_model.pkl # Company fit model
│   ├── scaler.pkl            # Feature scaler
│   └── label_encoders.pkl    # Categorical encoders
│
├── 🌐 Web Application:
│   ├── app.py                # ⭐ Main Flask app with auth & dashboard
│   ├── job_survey.csv        # Dataset (3000 records)
│   ├── requirements.txt      # Python dependencies
│   └── README.md            # This file
│
├── 🎨 Frontend:
│   ├── templates/
│   │   ├── index.html        # Survey form
│   │   ├── result.html       # Prediction results
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration page
│   │   ├── dashboard.html    # ⭐ Admin dashboard with charts
│   │   ├── metrics.html      # Model performance
│   │   └── visualize.html    # Data visualizations
│   └── static/
│       ├── css/             # TailwindCSS styles
│       └── js/              # Chart.js scripts
│
└── 📝 Documentation:
    ├── PROJECT_NOTES.md     # Development notes
    ├── IMPROVEMENT.md       # Future improvements
    └── DOCUMENTATION_FOR_AI_AGENT.md
```

---

## 📊 Dataset

### Dataset Info
- **File**: `job_survey.csv`
- **Records**: 3000 survey responses
- **Database**: MySQL (XAMPP)
- **Tables**: users, survey_data, dashboard_stats

### Survey Data Fields
- Personal info: email, nama, tempat_tinggal, jurusan
- Employment status & details
- Job satisfaction & recommendations
- Unemployment challenges
- ML predictions stored in database

---

## 🤖 Model Machine Learning

### KNN Models
- **Company Fit**: 96.67% accuracy (2 classes)
- **Major Recommendation**: 13 categories
- **Clustering**: K-Means (3 clusters)

### Database Integration
- Survey predictions saved to MySQL
- Dashboard statistics auto-calculated
- Real-time analytics from live data

---

## 🌐 Rute & Halaman

### Public Routes
- `/` - Survey form
- `/result` - Prediction results
- `/metrics` - Model performance
- `/visualize` - Data visualizations

### Authentication Routes
- `/login` - User login
- `/register` - User registration
- `/logout` - User logout

### Protected Routes (Login Required)
- `/dashboard` - Admin dashboard with analytics

---

## 💻 Teknologi yang Digunakan

### Backend
- **Flask 3.1.0** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Login** - User authentication
- **Flask-WTF** - Form handling
- **MySQL Connector** - Database driver

### Frontend
- **TailwindCSS** - Modern UI framework
- **Chart.js** - Interactive charts
- **HTML5/CSS3** - Responsive design

### Machine Learning
- **scikit-learn** - KNN & K-Means models
- **pandas/numpy** - Data processing
- **matplotlib/seaborn** - Visualizations

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python setup_database.py

# 3. Create admin user
python -c "
from app import app, db
from models import User
with app.app_context():
    admin = User(username='admin', email='admin@example.com', full_name='Administrator', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
"

# 4. Run application
python app.py

# 5. Access dashboard
# - Survey: http://127.0.0.1:5000/
# - Login: http://127.0.0.1:5000/login (admin/admin123)
# - Dashboard: http://127.0.0.1:5000/dashboard
```

---

## ✅ Status Implementation

- ✅ **Survey Form**: 28 questions, conditional logic
- ✅ **ML Predictions**: KNN models with 96.67% accuracy
- ✅ **Database Integration**: MySQL with 3000 records
- ✅ **User Authentication**: Login/register with Flask-Login
- ✅ **Admin Dashboard**: Charts, filtering, pagination
- ✅ **Real-time Analytics**: Live statistics from database
- ✅ **Responsive UI**: TailwindCSS design
- ✅ **Data Visualization**: Chart.js integration

---

## 📞 Support

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

**Database:** XAMPP MySQL (localhost, root, no password)

**Last Updated:** November 14, 2025
**Status:** ✅ Production Ready with Full Dashboard

---

**🎉 Job Recommendation System with Complete Admin Dashboard - Ready to Use!**
