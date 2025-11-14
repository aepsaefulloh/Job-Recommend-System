"""
Database Setup and Data Import Script
Creates database tables and imports survey data from job_survey.csv
"""

import os
import pandas as pd
from flask import Flask
from models import db, SurveyData, DashboardStats
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Create Flask application with database configuration"""
    app = Flask(__name__)

    # Database configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app

def create_database():
    """Create database if it doesn't exist"""
    import mysql.connector

    try:
        # Connect to MySQL server (without specifying database)
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD', '')
        )
        cursor = conn.cursor()

        # Create database if it doesn't exist
        db_name = os.getenv('DB_NAME')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✓ Database '{db_name}' created or already exists")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Error creating database: {err}")
        return False

    return True

def create_tables():
    """Create all database tables"""
    try:
        db.create_all()
        print("✓ All tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def import_survey_data():
    """Import survey data from job_survey.csv"""
    try:
        # Read CSV file
        csv_file = 'job_survey.csv'
        if not os.path.exists(csv_file):
            print(f"❌ CSV file '{csv_file}' not found")
            return False

        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"✓ Loaded {len(df)} records from {csv_file}")

        # Clear existing data
        SurveyData.query.delete()
        print("✓ Cleared existing survey data")

        # Import data row by row
        imported_count = 0
        for _, row in df.iterrows():
            try:
                # Helper function to handle NaN values and numeric conversion
                def clean_value(value):
                    if pd.isna(value) or value == 'nan' or str(value).lower() == 'nan':
                        return None
                    return value

                def clean_numeric(value):
                    if pd.isna(value) or value == 'nan' or str(value).lower() == 'nan':
                        return None
                    try:
                        return float(value)
                    except (ValueError, TypeError):
                        return None

                survey_record = SurveyData(
                    email=clean_value(row.get('email', '')),
                    nama=clean_value(row.get('nama', '')),
                    tempat_tinggal=clean_value(row.get('tempat_tinggal', '')),
                    jurusan=clean_value(row.get('jurusan', '')),
                    status_bekerja=clean_value(row.get('status_bekerja', '')),

                    # Employment data
                    profesi_sekarang=clean_value(row.get('profesi_sekarang')),
                    tempat_kerja=clean_value(row.get('tempat_kerja_saat_ini')),
                    cara_mendapat_pekerjaan=clean_value(row.get('cara_mendapat_pekerjaan')),
                    kemudahan_cari_kerja=clean_value(row.get('kemudahan_cari_kerja')),
                    bantuan_sekolah=clean_value(row.get('bantuan_sekolah')),
                    kesesuaian_minat=clean_value(row.get('kesesuaian_minat')),
                    waktu_kerja_pertama=clean_numeric(row.get('waktu_kerja_pertama')),
                    waktu_kerja_pertama_bulan=clean_numeric(row.get('waktu_kerja_pertama_bulan')),
                    jenis_perusahaan=clean_value(row.get('jenis_perusahaan')),
                    kesesuaian_jurusan=clean_value(row.get('kesesuaian_jurusan')),
                    kepuasan=clean_value(row.get('kepuasan')),
                    rencana_pindah_kerja=clean_value(row.get('rencana_pindah_kerja')),
                    lama_kerja_1=clean_numeric(row.get('lama_kerja_1')),
                    lama_kerja_2=clean_numeric(row.get('lama_kerja_2')),
                    nyaman=clean_value(row.get('kenyamanan')),
                    gaji_kategori=clean_value(row.get('gaji_kategori')),
                    gaji=clean_numeric(row.get('gaji')),

                    # Unemployment data
                    alasan_belum_kerja=clean_value(row.get('alasan_belum_kerja')),
                    rencana_kerja_sesuai_jurusan=clean_value(row.get('rencana_kerja_sesuai_jurusan')),
                    kendala_utama=clean_value(row.get('kendala_utama')),
                    ikut_pelatihan=clean_value(row.get('ikut_pelatihan')),
                    gunakan_platform_online=clean_value(row.get('gunakan_platform_online')),
                    kepercayaan_keterampilan=clean_value(row.get('kepercayaan_keterampilan')),
                    bersedia_rekomendasi_sekolah=clean_value(row.get('bersedia_rekomendasi_sekolah')),

                    # Prediction results
                    jurusan_cocok=clean_value(row.get('jurusan_cocok')),
                    perusahaan_tepat=clean_value(row.get('perusahaan_tepat'))
                )

                db.session.add(survey_record)
                imported_count += 1

            except Exception as e:
                print(f"⚠️ Error importing row: {e}")
                continue

        db.session.commit()
        print(f"✓ Successfully imported {imported_count} survey records")

        # Update dashboard statistics
        update_dashboard_stats()

        return True

    except Exception as e:
        print(f"❌ Error importing survey data: {e}")
        db.session.rollback()
        return False

def update_dashboard_stats():
    """Update dashboard statistics"""
    try:
        # Clear existing stats
        DashboardStats.query.delete()

        # Calculate statistics
        total_surveys = SurveyData.query.count()
        employed_count = SurveyData.query.filter_by(status_bekerja='Ya').count()
        unemployed_count = SurveyData.query.filter_by(status_bekerja='Tidak').count()

        # Employment rate
        employment_rate = (employed_count / total_surveys * 100) if total_surveys > 0 else 0

        # Average salary (for employed)
        avg_salary = db.session.query(db.func.avg(SurveyData.gaji)).filter(
            SurveyData.status_bekerja == 'Ya',
            SurveyData.gaji.isnot(None)
        ).scalar() or 0

        # Most common major
        major_stats = db.session.query(
            SurveyData.jurusan,
            db.func.count(SurveyData.jurusan).label('count')
        ).group_by(SurveyData.jurusan).order_by(db.desc('count')).first()

        most_common_major = major_stats[0] if major_stats else "N/A"
        major_count = major_stats[1] if major_stats else 0

        # Location distribution
        location_stats = db.session.query(
            SurveyData.tempat_tinggal,
            db.func.count(SurveyData.tempat_tinggal).label('count')
        ).group_by(SurveyData.tempat_tinggal).order_by(db.desc('count')).first()

        most_common_location = location_stats[0] if location_stats else "N/A"
        location_count = location_stats[1] if location_stats else 0

        # Insert statistics
        stats_data = [
            DashboardStats(stat_name='total_surveys', stat_value=total_surveys, stat_type='count'),
            DashboardStats(stat_name='employed_count', stat_value=employed_count, stat_type='count'),
            DashboardStats(stat_name='unemployed_count', stat_value=unemployed_count, stat_type='count'),
            DashboardStats(stat_name='employment_rate', stat_value=employment_rate, stat_type='percentage'),
            DashboardStats(stat_name='average_salary', stat_value=avg_salary, stat_type='average'),
            DashboardStats(stat_name='most_common_major', stat_value=major_count, stat_type='count'),
            DashboardStats(stat_name='most_common_location', stat_value=location_count, stat_type='count'),
        ]

        # Add string stats separately
        db.session.add_all(stats_data)
        db.session.commit()

        print("✓ Dashboard statistics updated")

    except Exception as e:
        print(f"❌ Error updating dashboard stats: {e}")
        db.session.rollback()

def main():
    """Main setup function"""
    print("="*60)
    print("JOB RECOMMENDATION SYSTEM - DATABASE SETUP")
    print("="*60)

    # Create Flask app
    app = create_app()

    with app.app_context():
        # Create database
        if not create_database():
            return

        # Create tables
        if not create_tables():
            return

        # Import survey data
        if not import_survey_data():
            return

    print("\n" + "="*60)
    print("✅ DATABASE SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📊 Database Summary:")
    print("  - Database: job_recommendation_db")
    print("  - Tables: users, survey_data, dashboard_stats")
    print("  - Survey Records: Imported from job_survey.csv")
    print("  - Statistics: Auto-calculated and cached")
    print("\n🚀 Ready to run the application!")

if __name__ == '__main__':
    main()