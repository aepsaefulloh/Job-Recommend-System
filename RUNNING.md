# 🚀 Setup Cepat - Sistem Rekomendasi Pekerjaan

## Prasyarat
- Python 3.7+
- XAMPP dengan MySQL berjalan
- pip terinstall

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Setup Database & Import Data
```bash
python setup_database.py
```

**Output yang Diharapkan:**
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

## 3. Jalankan Aplikasi
```bash
python app.py
```

## 4. Akses Aplikasi
- **Form Survey**: http://127.0.0.1:5000/
- **Login**: http://127.0.0.1:5000/login
- **Dashboard**: http://127.0.0.1:5000/dashboard

## Kredensial Admin Default
- **Username**: admin
- **Password**: admin123

## Konfigurasi Database (.env)
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=job_recommendation_db
```

## Troubleshooting
- Pastikan XAMPP MySQL sedang berjalan
- Periksa apakah port 5000 tersedia
- Verifikasi versi Python: `python --version`