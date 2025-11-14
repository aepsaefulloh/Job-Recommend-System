"""
Database Models for Job Recommendation System
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Plain text password for thesis
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='viewer')  # admin, viewer
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = password  # Store plain text password

    def check_password(self, password):
        return self.password == password  # Compare plain text

    def __repr__(self):
        return f'<User {self.username}>'

class SurveyData(db.Model):
    """Survey data model - mirrors job_survey.csv structure"""
    __tablename__ = 'survey_data'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    tempat_tinggal = db.Column(db.String(50), nullable=False)
    jurusan = db.Column(db.String(50), nullable=False)
    status_bekerja = db.Column(db.String(10), nullable=False)

    # Employment data (if working)
    profesi_sekarang = db.Column(db.String(100))
    tempat_kerja = db.Column(db.String(100))
    cara_mendapat_pekerjaan = db.Column(db.Text)
    kemudahan_cari_kerja = db.Column(db.String(20))
    bantuan_sekolah = db.Column(db.String(10))
    kesesuaian_minat = db.Column(db.String(20))
    waktu_kerja_pertama = db.Column(db.Float)
    waktu_kerja_pertama_bulan = db.Column(db.Float)
    jenis_perusahaan = db.Column(db.String(50))
    kesesuaian_jurusan = db.Column(db.String(10))
    kepuasan = db.Column(db.String(20))
    rencana_pindah_kerja = db.Column(db.String(10))
    lama_kerja_1 = db.Column(db.Float)
    lama_kerja_2 = db.Column(db.Float)
    nyaman = db.Column(db.String(10))
    gaji_kategori = db.Column(db.String(20))
    gaji = db.Column(db.Float)

    # Unemployment data (if not working)
    alasan_belum_kerja = db.Column(db.String(100))
    rencana_kerja_sesuai_jurusan = db.Column(db.String(10))
    kendala_utama = db.Column(db.String(100))
    ikut_pelatihan = db.Column(db.String(10))
    gunakan_platform_online = db.Column(db.String(10))
    kepercayaan_keterampilan = db.Column(db.String(20))
    bersedia_rekomendasi_sekolah = db.Column(db.String(10))

    # Prediction results
    jurusan_cocok = db.Column(db.String(50))
    perusahaan_tepat = db.Column(db.String(20))

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SurveyData {self.email} - {self.nama}>'

class DashboardStats(db.Model):
    """Dashboard statistics cache"""
    __tablename__ = 'dashboard_stats'

    id = db.Column(db.Integer, primary_key=True)
    stat_name = db.Column(db.String(50), unique=True, nullable=False)
    stat_value = db.Column(db.Float, nullable=False)
    stat_type = db.Column(db.String(20), nullable=False)  # count, percentage, average
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<DashboardStats {self.stat_name}: {self.stat_value}>'