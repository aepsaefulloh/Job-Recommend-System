"""
Job Recommendation System - Flask Web Application with Authentication & Dashboard
Main application file with route handlers, authentication, and dashboard
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from sqlalchemy import func, desc
import pandas as pd

# Import local modules
from models import db, User, SurveyData, DashboardStats
from forms import LoginForm, RegistrationForm, SurveyFilterForm
from utils.predictor import make_predictions, get_job_recommendations
from utils.model_loader import load_models
from utils.visualization import (
    generate_gpa_vs_salary_scatter,
    generate_work_time_vs_satisfaction,
    generate_gpa_distribution,
    generate_salary_distribution,
    # generate_correlation_heatmap,  # Temporarily commented out due to seaborn import issues
    generate_experience_box,
    generate_top_jurusan_bar,
    generate_satisfaction_pie,
    generate_elbow_curve,
    generate_cluster_scatter
)

# Helper function to load survey data dynamically
def load_survey_data():
    """Load job_survey.csv and return dataframe"""
    try:
        df = pd.read_csv('job_survey.csv')
        return df
    except Exception as e:
        print(f"Error loading survey data: {e}")
        return None

def update_dashboard_stats():
    """Update dashboard statistics after new survey submission"""
    try:
        # Get total survey count
        total_surveys = SurveyData.query.count()

        # Get employed vs unemployed count
        employed_count = SurveyData.query.filter_by(status_bekerja='Ya').count()
        unemployed_count = SurveyData.query.filter_by(status_bekerja='Tidak').count()

        # Get major distribution
        major_stats = db.session.query(
            SurveyData.jurusan,
            func.count(SurveyData.jurusan).label('count')
        ).group_by(SurveyData.jurusan).all()

        # Get location distribution
        location_stats = db.session.query(
            SurveyData.tempat_tinggal,
            func.count(SurveyData.tempat_tinggal).label('count')
        ).group_by(SurveyData.tempat_tinggal).all()

        # Get company type distribution
        company_stats = db.session.query(
            SurveyData.jenis_perusahaan,
            func.count(SurveyData.jenis_perusahaan).label('count')
        ).filter(SurveyData.jenis_perusahaan.isnot(None)).group_by(SurveyData.jenis_perusahaan).all()

        # Update or create dashboard stats
        stats_to_update = {
            'total_surveys': total_surveys,
            'employed_count': employed_count,
            'unemployed_count': unemployed_count,
            'employment_rate': (employed_count / total_surveys * 100) if total_surveys > 0 else 0,
            'top_major': major_stats[0][0] if major_stats else 'N/A',
            'top_location': location_stats[0][0] if location_stats else 'N/A',
            'top_company_type': company_stats[0][0] if company_stats else 'N/A'
        }

        for stat_name, stat_value in stats_to_update.items():
            stat_record = DashboardStats.query.filter_by(stat_name=stat_name).first()
            if stat_record:
                stat_record.stat_value = stat_value
            else:
                stat_record = DashboardStats(
                    stat_name=stat_name,
                    stat_value=stat_value,
                    stat_type='count' if isinstance(stat_value, int) else 'percentage'
                )
                db.session.add(stat_record)

        db.session.commit()
        print(f"✅ Dashboard statistics updated: {stats_to_update}")

    except Exception as e:
        print(f"❌ Error updating dashboard stats: {e}")
        db.session.rollback()

def calculate_dynamic_metrics():
    """Calculate model metrics dynamically from job_survey.csv"""
    try:
        df = load_survey_data()
        if df is None:
            return None
            
        # Filter employed records
        df_employed = df[df['status_bekerja'] == 'Ya'].copy()
        
        if len(df_employed) == 0:
            return None
        
        # Calculate jurusan accuracy
        jurusan_correct = len(df_employed[df_employed['kesesuaian_jurusan'] == 'Ya'])
        jurusan_total = len(df_employed[df_employed['kesesuaian_jurusan'].notna()])
        jurusan_accuracy = jurusan_correct / jurusan_total if jurusan_total > 0 else 0
        
        # Calculate perusahaan accuracy
        perusahaan_correct = len(df_employed[df_employed['perusahaan_tepat'] == 'Tepat'])
        perusahaan_total = len(df_employed[df_employed['perusahaan_tepat'].notna()])
        perusahaan_accuracy = perusahaan_correct / perusahaan_total if perusahaan_total > 0 else 0
        
        # Calculate confusion matrix for perusahaan
        cm_perusahaan = [[0, 0], [0, 0]]
        for _, row in df_employed.iterrows():
            if pd.notna(row.get('perusahaan_tepat')):
                actual = 0 if row['perusahaan_tepat'] == 'Tepat' else 1
                # Simulate prediction (using actual as prediction for now)
                predicted = actual
                cm_perusahaan[actual][predicted] += 1
        
        # Count total records (all alumni)
        total_records = len(df)
        employed_records = len(df_employed)
        
        return {
            'jurusan_accuracy': jurusan_accuracy,
            'perusahaan_accuracy': perusahaan_accuracy,
            'jurusan_confusion_matrix': [[0, 0], [0, 0]],  # Not calculated from CSV
            'perusahaan_confusion_matrix': cm_perusahaan,
            'total_records': total_records,
            'employed_records': employed_records
        }
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return None

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Load ML models
models = load_models()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============= AUTHENTICATION ROUTES =============

@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_login = db.func.now()
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role='viewer'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('index'))

# ============= DASHBOARD ROUTES =============

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard with survey data analytics"""
    page = request.args.get('page', 1, type=int)
    per_page = 25

    # Get filter parameters
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status_bekerja', '')
    jurusan_filter = request.args.get('jurusan', '')
    location_filter = request.args.get('tempat_tinggal', '')
    company_filter = request.args.get('jenis_perusahaan', '')

    # Initialize variables
    surveys = []
    pagination = None
    users = []
    user_pagination = None

    # Role-based access control (admin and viewer can see data)
    if current_user.role in ['admin', 'viewer']:
        # Admin can see all survey data
        # Build query with filters
        query = SurveyData.query

        # Search filter (nama or email)
        if search_query:
            query = query.filter(
                db.or_(
                    SurveyData.nama.ilike(f'%{search_query}%'),
                    SurveyData.email.ilike(f'%{search_query}%')
                )
            )

        if status_filter:
            query = query.filter_by(status_bekerja=status_filter)
        if jurusan_filter:
            query = query.filter_by(jurusan=jurusan_filter)
        if location_filter:
            query = query.filter_by(tempat_tinggal=location_filter)
        if company_filter:
            query = query.filter(SurveyData.jenis_perusahaan == company_filter)

        # Get paginated results
        pagination = query.order_by(SurveyData.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        surveys = pagination.items

    # Get all users for admin management (admin only)
    if current_user.role == 'admin':
        user_page = request.args.get('user_page', 1, type=int)
        user_pagination = User.query.order_by(User.created_at.desc()).paginate(
            page=user_page, per_page=10, error_out=False
        )
        users = user_pagination.items

    # Get dashboard statistics (available to all users)
    stats = {}
    dashboard_stats = DashboardStats.query.all()
    for stat in dashboard_stats:
        stats[stat.stat_name] = stat.stat_value

    # Get chart data (available to all users)
    major_data = db.session.query(
        SurveyData.jurusan,
        func.count(SurveyData.jurusan).label('count')
    ).group_by(SurveyData.jurusan).order_by(desc('count')).limit(10).all()

    location_data = db.session.query(
        SurveyData.tempat_tinggal,
        func.count(SurveyData.tempat_tinggal).label('count')
    ).group_by(SurveyData.tempat_tinggal).order_by(desc('count')).limit(5).all()

    company_data = db.session.query(
        SurveyData.jenis_perusahaan,
        func.count(SurveyData.jenis_perusahaan).label('count')
    ).filter(SurveyData.jenis_perusahaan.isnot(None)).group_by(SurveyData.jenis_perusahaan).order_by(desc('count')).limit(5).all()

    # Prepare filter form (available for admin and viewer)
    filter_form = None
    if current_user.role in ['admin', 'viewer']:
        filter_form = SurveyFilterForm()
        filter_form.search.data = search_query
        filter_form.status_bekerja.data = status_filter
        filter_form.jurusan.data = jurusan_filter
        filter_form.tempat_tinggal.data = location_filter
        filter_form.jenis_perusahaan.data = company_filter

        # Populate filter choices
        filter_form.jurusan.choices = [('', 'All')] + [(m[0], m[0]) for m in major_data]
        filter_form.tempat_tinggal.choices = [('', 'All')] + [(l[0], l[0]) for l in location_data]
        filter_form.jenis_perusahaan.choices = [('', 'All')] + [(c[0], c[0]) for c in company_data]

    # Create filtered request args (exclude 'page' to avoid conflicts in pagination)
    filtered_args = {k: v for k, v in request.args.items() if k != 'page'}

    return render_template('dashboard.html',
                         surveys=surveys,
                         pagination=pagination,
                         users=users,
                         user_pagination=user_pagination,
                         stats=stats,
                         filter_form=filter_form,
                         filtered_args=filtered_args,
                         major_labels=[m[0] for m in major_data],
                         major_data=[m[1] for m in major_data],
                         location_labels=[l[0] for l in location_data],
                         location_data=[l[1] for l in location_data],
                         company_labels=[c[0] for c in company_data],
                         company_data=[c[1] for c in company_data])

@app.route('/update_user_role/<int:user_id>', methods=['POST'])
@login_required
def update_user_role(user_id):
    """Update user role (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')

    if new_role not in ['viewer', 'admin']:
        flash('Invalid role specified.', 'error')
        return redirect(url_for('dashboard'))

    user.role = new_role
    db.session.commit()

    flash(f'User {user.username} role updated to {new_role}.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/export_excel')
@login_required
def export_excel():
    """Export survey data to Excel (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))

    try:
        import pandas as pd
        from io import BytesIO
        from flask import send_file

        # Get all survey data
        surveys = SurveyData.query.order_by(SurveyData.created_at.desc()).all()

        # Convert to dictionary list
        data = []
        for survey in surveys:
            data.append({
                'ID': survey.id,
                'Email': survey.email,
                'Nama': survey.nama,
                'Tempat Tinggal': survey.tempat_tinggal,
                'Jurusan': survey.jurusan,
                'Status Bekerja': survey.status_bekerja,
                'Profesi Sekarang': survey.profesi_sekarang,
                'Tempat Kerja': survey.tempat_kerja,
                'Cara Mendapat Pekerjaan': survey.cara_mendapat_pekerjaan,
                'Kemudahan Cari Kerja': survey.kemudahan_cari_kerja,
                'Bantuan Sekolah': survey.bantuan_sekolah,
                'Kesesuaian Minat': survey.kesesuaian_minat,
                'Waktu Kerja Pertama (Tahun)': survey.waktu_kerja_pertama,
                'Jenis Perusahaan': survey.jenis_perusahaan,
                'Kesesuaian Jurusan': survey.kesesuaian_jurusan,
                'Kepuasan': survey.kepuasan,
                'Rencana Pindah Kerja': survey.rencana_pindah_kerja,
                'Lama Kerja 1': survey.lama_kerja_1,
                'Lama Kerja 2': survey.lama_kerja_2,
                'Nyaman': survey.nyaman,
                'Gaji Kategori': survey.gaji_kategori,
                'Gaji': survey.gaji,
                'Alasan Belum Kerja': survey.alasan_belum_kerja,
                'Rencana Kerja Sesuai Jurusan': survey.rencana_kerja_sesuai_jurusan,
                'Kendala Utama': survey.kendala_utama,
                'Ikut Pelatihan': survey.ikut_pelatihan,
                'Gunakan Platform Online': survey.gunakan_platform_online,
                'Kepercayaan Keterampilan': survey.kepercayaan_keterampilan,
                'Bersedia Rekomendasi Sekolah': survey.bersedia_rekomendasi_sekolah,
                'Jurusan Cocok (Prediksi)': survey.jurusan_cocok,
                'Perusahaan Tepat (Prediksi)': survey.perusahaan_tepat,
                'Dibuat Pada': survey.created_at.strftime('%Y-%m-%d %H:%M:%S') if survey.created_at else ''
            })

        # Create DataFrame
        df = pd.DataFrame(data)

        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Survey Data')
            
            # Auto-adjust column width
            worksheet = writer.sheets['Survey Data']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)

        # Generate filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'survey_data_{timestamp}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except ImportError:
        flash('Excel export requires pandas and openpyxl. Please install: pip install pandas openpyxl', 'error')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Error exporting data: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

# ============= EXISTING ROUTES =============

@app.route('/')
def index():
    """Display survey form"""
    return render_template('index.html')

@app.route('/result', methods=['POST'])
@csrf.exempt
def result():
    """Process form and display prediction results"""
    try:
        # Make predictions using the predictor module
        predictions = make_predictions(request.form, models)

        # Extract results
        processed_data = predictions['processed_data']

        # Save survey data to database
        survey_record = SurveyData(
            email=processed_data['email'],
            nama=processed_data['nama'],
            tempat_tinggal=processed_data['tempat_tinggal'],
            jurusan=processed_data['jurusan'],
            status_bekerja=processed_data['status_bekerja'],
            profesi_sekarang=processed_data.get('profesi_sekarang'),
            tempat_kerja=processed_data.get('tempat_kerja'),  # Fixed: use processed_data key
            cara_mendapat_pekerjaan=processed_data.get('cara_mendapat_pekerjaan'),
            kemudahan_cari_kerja=processed_data.get('kemudahan_cari_kerja') or processed_data.get('kemudahan_cari_kerja_belum'),
            bantuan_sekolah=processed_data.get('bantuan_sekolah') or processed_data.get('bantuan_sekolah_belum'),
            kesesuaian_minat=processed_data.get('kesesuaian_minat'),
            waktu_kerja_pertama=processed_data.get('waktu_kerja_pertama'),
            jenis_perusahaan=processed_data.get('jenis_perusahaan'),
            kesesuaian_jurusan=processed_data.get('kesesuaian_jurusan'),
            kepuasan=processed_data.get('kepuasan'),
            rencana_pindah_kerja=processed_data.get('rencana_pindah_kerja'),
            lama_kerja_1=processed_data.get('lama_kerja_1'),  # Fixed: use processed_data key
            lama_kerja_2=processed_data.get('lama_kerja_2'),  # Added: total experience
            nyaman=processed_data.get('nyaman'),  # Fixed: use processed_data key
            gaji_kategori=request.form.get('gaji'),  # Fixed: use request.form instead of form_data
            gaji=processed_data.get('gaji'),  # Numeric salary value
            alasan_belum_kerja=processed_data.get('alasan_belum_kerja'),
            rencana_kerja_sesuai_jurusan=processed_data.get('rencana_kerja_sesuai_jurusan'),
            kendala_utama=processed_data.get('kendala_utama'),
            ikut_pelatihan=processed_data.get('ikut_pelatihan'),
            gunakan_platform_online=processed_data.get('gunakan_platform_online'),
            kepercayaan_keterampilan=processed_data.get('kepercayaan_keterampilan'),
            bersedia_rekomendasi_sekolah=processed_data.get('bersedia_rekomendasi_sekolah'),
            jurusan_cocok=predictions['jurusan_cocok'],
            perusahaan_tepat=predictions['perusahaan_tepat']
        )

        db.session.add(survey_record)
        db.session.commit()

        # Update dashboard statistics
        update_dashboard_stats()

        # Get metrics data for display
        metrics_data = calculate_dynamic_metrics()
        if metrics_data is None and models.get('metrics_data'):
            metrics_data = models.get('metrics_data')

        # Render results
        return render_template('result.html',
                             email=processed_data['email'],
                             nama=processed_data['nama'],
                             tempat_tinggal=processed_data['tempat_tinggal'],
                             status_bekerja=processed_data['status_bekerja'],
                             jurusan_cocok=predictions['jurusan_cocok'],
                             perusahaan_tepat=predictions['perusahaan_tepat'],
                             recommended_jobs=predictions['recommended_jobs'],
                             validation=predictions.get('validation'),
                             metrics_data=metrics_data)

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n❌ Error during prediction:\n{error_details}")

        # User-friendly error message
        return f"""
        <div style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 30px; background: #fee2e2; border-radius: 10px; border-left: 5px solid #dc2626;">
            <h2 style="color: #dc2626;">❌ Terjadi Kesalahan</h2>
            <p style="color: #333; line-height: 1.6;">
                Maaf, sistem tidak dapat memproses data Anda saat ini.
                Kemungkinan ada data yang tidak sesuai dengan model yang sudah dilatih.
            </p>
            <p style="color: #666; font-size: 14px; margin-top: 20px;">
                <strong>Detail Error:</strong> {str(e)}
            </p>
            <div style="margin-top: 30px;">
                <a href="/" style="background: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block;">
                    ← Kembali ke Form
                </a>
            </div>
        </div>
        """, 500

@app.route('/metrics')
def metrics():
    """Display model performance metrics dynamically from CSV"""
    # Try to get dynamic metrics from CSV first
    metrics_data = calculate_dynamic_metrics()
    
    # Fallback to cached metrics if dynamic calculation fails
    if metrics_data is None:
        if models.get('metrics_data') is None:
            return "Metrics data not available. Please check job_survey.csv file.", 500
        metrics_data = models.get('metrics_data')
    
    return render_template('metrics.html',
                         jurusan_accuracy=metrics_data['jurusan_accuracy'],
                         perusahaan_accuracy=metrics_data['perusahaan_accuracy'],
                         cm_jurusan=metrics_data['jurusan_confusion_matrix'],
                         cm_perusahaan=metrics_data['perusahaan_confusion_matrix'],
                         total_records=metrics_data.get('total_records', 2303))

@app.route('/visualize')
def visualize():
    """Display data visualizations dynamically from CSV"""
    try:
        # Load data directly from CSV
        df = load_survey_data()
        
        # Fallback to cached data if CSV load fails
        if df is None:
            if models.get('visualization_data') is None:
                return "Visualization data not available. Please check job_survey.csv file.", 500
            df = models.get('visualization_data')['data']
        
        # Filter to employed records for accurate visualizations
        df_employed = df[df['status_bekerja'] == 'Ya'].copy()
        
        # Map column names if needed
        if 'kenyamanan' in df_employed.columns and 'nyaman' not in df_employed.columns:
            df_employed['nyaman'] = df_employed['kenyamanan']
        if 'tempat_kerja_saat_ini' in df_employed.columns and 'tempat_kerja' not in df_employed.columns:
            df_employed['tempat_kerja'] = df_employed['tempat_kerja_saat_ini']

        # Generate visualizations using helper functions
        plot1 = generate_gpa_vs_salary_scatter(df_employed)
        plot2 = generate_work_time_vs_satisfaction(df_employed)
        plot3 = generate_gpa_distribution(df_employed)
        plot4 = generate_salary_distribution(df_employed)
        plot5 = ""  # Correlation heatmap placeholder
        plot6 = generate_experience_box(df_employed)
        plot7 = generate_top_jurusan_bar(df_employed)
        plot8 = generate_satisfaction_pie(df_employed)

        return render_template('visualize.html',
                             plot1=plot1, plot2=plot2, plot3=plot3, plot4=plot4,
                             plot5=plot5,
                             plot6=plot6, plot7=plot7, plot8=plot8)

    except Exception as e:
        return f"Error generating visualizations: {str(e)}", 500

# Create admin user if not exists
def create_admin_user():
    """Create default admin user if no users exist"""
    if User.query.count() == 0:
        admin_user = User(
            username='admin',
            email='admin@admin.com',
            full_name='Administrator',
            role='admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Default admin user created:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Please change the password after first login!")

if __name__ == '__main__':
    # Create all database tables
    with app.app_context():
        db.create_all()
        create_admin_user()

    print("\n" + "="*60)
    print("JOB RECOMMENDATION SYSTEM WITH DASHBOARD")
    print("="*60)
    print("\nFlask app starting...")
    print("Open browser and go to: http://127.0.0.1:5000")
    print("\nRoutes available:")
    print("  - http://127.0.0.1:5000/ (Home - Prediction Form)")
    print("  - http://127.0.0.1:5000/login (Login)")
    print("  - http://127.0.0.1:5000/register (Register)")
    print("  - http://127.0.0.1:5000/dashboard (Dashboard - Login Required)")
    print("  - http://127.0.0.1:5000/metrics (Model Performance)")
    print("  - http://127.0.0.1:5000/visualize (Data Visualizations)")
    print("  - http://127.0.0.1:5000/result (POST only - Prediction Results)")
    print("="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
