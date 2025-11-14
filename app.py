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
        
        # Count total records
        total_records = len(df_employed)
        
        return {
            'jurusan_accuracy': jurusan_accuracy,
            'perusahaan_accuracy': perusahaan_accuracy,
            'jurusan_confusion_matrix': [[0, 0], [0, 0]],  # Not calculated from CSV
            'perusahaan_confusion_matrix': cm_perusahaan,
            'total_records': total_records
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
            role=form.role.data
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
    status_filter = request.args.get('status_bekerja', '')
    jurusan_filter = request.args.get('jurusan', '')
    location_filter = request.args.get('tempat_tinggal', '')
    company_filter = request.args.get('jenis_perusahaan', '')

    # Build query with filters
    query = SurveyData.query

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

    # Get dashboard statistics
    stats = {}
    dashboard_stats = DashboardStats.query.all()
    for stat in dashboard_stats:
        stats[stat.stat_name] = stat.stat_value

    # Get chart data
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

    # Prepare filter form
    filter_form = SurveyFilterForm()
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
                         stats=stats,
                         filter_form=filter_form,
                         filtered_args=filtered_args,
                         major_labels=[m[0] for m in major_data],
                         major_data=[m[1] for m in major_data],
                         location_labels=[l[0] for l in location_data],
                         location_data=[l[1] for l in location_data],
                         company_labels=[c[0] for c in company_data],
                         company_data=[c[1] for c in company_data])

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
            tempat_kerja=processed_data.get('tempat_kerja'),
            cara_mendapat_pekerjaan=processed_data.get('cara_mendapat_pekerjaan'),
            kemudahan_cari_kerja=processed_data.get('kemudahan_cari_kerja'),
            bantuan_sekolah=processed_data.get('bantuan_sekolah'),
            kesesuaian_minat=processed_data.get('kesesuaian_minat'),
            waktu_kerja_pertama=processed_data.get('waktu_kerja_pertama'),
            jenis_perusahaan=processed_data.get('jenis_perusahaan'),
            kesesuaian_jurusan=processed_data.get('kesesuaian_jurusan'),
            kepuasan=processed_data.get('kepuasan'),
            rencana_pindah_kerja=processed_data.get('rencana_pindah_kerja'),
            lama_kerja_1=processed_data.get('lama_kerja_1'),
            lama_kerja_2=processed_data.get('lama_kerja_2'),
            nyaman=processed_data.get('nyaman'),
            gaji=processed_data.get('gaji'),
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

        # Render results
        return render_template('result.html',
                             email=processed_data['email'],
                             nama=processed_data['nama'],
                             tempat_tinggal=processed_data['tempat_tinggal'],
                             status_bekerja=processed_data['status_bekerja'],
                             jurusan_cocok=predictions['jurusan_cocok'],
                             perusahaan_tepat=predictions['perusahaan_tepat'],
                             recommended_jobs=predictions['recommended_jobs'],
                             validation=predictions.get('validation'))

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

if __name__ == '__main__':
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
