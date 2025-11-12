from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from matplotlib import pyplot

app = Flask(__name__)

# Global variables
visualization_data = None
metrics_data = None
clustering_data = None

# Load models and encoders
print("Loading models and encoders...")
try:
    with open('knn_jurusan_model.pkl', 'rb') as f:
        knn_jurusan = pickle.load(f)
    
    with open('knn_perusahaan_model.pkl', 'rb') as f:
        knn_perusahaan = pickle.load(f)
    
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    with open('label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    
    with open('metrics.pkl', 'rb') as f:
        metrics_data = pickle.load(f)
    print("✓ Metrics loaded!")
    
    try:
        with open('visualization_data.pkl', 'rb') as f:
            visualization_data = pickle.load(f)
        print(f"✓ Visualization data loaded! ({visualization_data['sample_size']} samples)")
    except FileNotFoundError:
        print("⚠ Visualization data not found. Run preprocessing.py to generate.")
    
    try:
        with open('clustering_data.pkl', 'rb') as f:
            clustering_data = pickle.load(f)
        print("✓ Clustering data loaded! (K-Means with Elbow Method)")
    except FileNotFoundError:
        print("⚠ Clustering data not found. Run preprocessing.py to generate.")
    
    print("✓ Models and encoders loaded successfully!")
    
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Please run preprocessing.py first!")
    exit(1)

# ============= VISUALIZATION HELPER FUNCTIONS =============

def plot_to_base64(fig):
    """Convert matplotlib figure to base64 encoded image"""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=80)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return plot_url

def generate_gpa_vs_salary_scatter(df):
    """Generate scatter plot: GPA vs Salary"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Handle perusahaan_tepat mapping
    tepat_map = {'Tepat': 0, 'Tidak Tepat': 1}
    colors = [tepat_map.get(x, 0) for x in df['perusahaan_tepat']]
    
    scatter = ax.scatter(df['nilai_rata'], df['gaji'], 
                        c=colors, cmap='RdYlGn_r', alpha=0.6, s=50)
    ax.set_xlabel('Nilai Rata-Rata (IPK)', fontsize=12)
    ax.set_ylabel('Gaji (IDR)', fontsize=12)
    ax.set_title('Hubungan IPK dengan Gaji', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return plot_to_base64(fig)

def generate_work_time_vs_satisfaction(df):
    """Generate plot: Work time first vs Satisfaction"""
    fig, ax = plt.subplots(figsize=(10, 6))
    satisfaction_map = {'Kurang Puas': 1, 'Puas': 2, 'Sangat Puas': 3}
    df_plot = df.copy()
    df_plot['satisfaction_num'] = df_plot['kepuasan'].map(satisfaction_map)
    df_plot['nyaman_num'] = (df_plot['kenyamanan'] == 'Ya').astype(int)
    
    scatter = ax.scatter(df_plot['waktu_kerja_pertama'], df_plot['satisfaction_num'],
                        c=df_plot['nyaman_num'], cmap='coolwarm', alpha=0.6, s=50)
    ax.set_xlabel('Waktu Kerja Pertama (Bulan)', fontsize=12)
    ax.set_ylabel('Kepuasan Kerja', fontsize=12)
    ax.set_title('Waktu Kerja Pertama vs Kepuasan', fontsize=14, fontweight='bold')
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['Kurang Puas', 'Puas', 'Sangat Puas'])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return plot_to_base64(fig)

def generate_gpa_distribution(df):
    """Generate histogram: GPA distribution"""
    fig, ax = plt.subplots(figsize=(10, 6))
    tepat = df[df['perusahaan_tepat'] == 'Tepat']['nilai_rata']
    tidak_tepat = df[df['perusahaan_tepat'] == 'Tidak Tepat']['nilai_rata']
    
    ax.hist(tepat, bins=15, alpha=0.6, label='Tepat', color='green')
    ax.hist(tidak_tepat, bins=15, alpha=0.6, label='Tidak Tepat', color='red')
    ax.set_xlabel('Nilai Rata-Rata (IPK)', fontsize=12)
    ax.set_ylabel('Frekuensi', fontsize=12)
    ax.set_title('Distribusi IPK Berdasarkan Kesesuaian Perusahaan', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    return plot_to_base64(fig)

def generate_salary_distribution(df):
    """Generate histogram: Salary distribution by satisfaction"""
    fig, ax = plt.subplots(figsize=(10, 6))
    satisfaction_types = df['kepuasan'].unique()
    colors = {'Kurang Puas': 'red', 'Puas': 'yellow', 'Sangat Puas': 'green'}
    
    for sat in ['Kurang Puas', 'Puas', 'Sangat Puas']:
        if sat in satisfaction_types:
            data = df[df['kepuasan'] == sat]['gaji']
            ax.hist(data, bins=15, alpha=0.5, label=sat, color=colors.get(sat, 'blue'))
    
    ax.set_xlabel('Gaji (IDR)', fontsize=12)
    ax.set_ylabel('Frekuensi', fontsize=12)
    ax.set_title('Distribusi Gaji Berdasarkan Kepuasan', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    return plot_to_base64(fig)

def generate_correlation_heatmap(df):
    """Generate correlation heatmap"""
    fig, ax = plt.subplots(figsize=(10, 8))
    numeric_cols = ['nilai_rata', 'gaji', 'lama_kerja_1', 'lama_kerja_2']
    numeric_data = df[numeric_cols].corr()
    
    sns.heatmap(numeric_data, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, ax=ax, cbar_kws={'label': 'Korelasi'})
    ax.set_title('Matriks Korelasi Fitur Numerik', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return plot_to_base64(fig)

def generate_experience_box(df):
    """Generate box plot: Experience distribution"""
    fig, ax = plt.subplots(figsize=(10, 6))
    data_tepat = [df[df['perusahaan_tepat'] == 'Tepat']['lama_kerja_2'].astype(float),
                  df[df['perusahaan_tepat'] == 'Tidak Tepat']['lama_kerja_2'].astype(float)]
    
    bp = ax.boxplot(data_tepat, labels=['Tepat', 'Tidak Tepat'], patch_artist=True)
    for patch, color in zip(bp['boxes'], ['lightgreen', 'lightcoral']):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Pengalaman Kerja (Tahun)', fontsize=12)
    ax.set_title('Distribusi Pengalaman Kerja', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    return plot_to_base64(fig)

def generate_top_jurusan_bar(df):
    """Generate bar chart: Top 10 majors"""
    fig, ax = plt.subplots(figsize=(10, 6))
    top_jurusan = df['jurusan_cocok'].value_counts().head(10)
    
    ax.barh(range(len(top_jurusan)), top_jurusan.values, color='steelblue')
    ax.set_yticks(range(len(top_jurusan)))
    ax.set_yticklabels(top_jurusan.index)
    ax.set_xlabel('Jumlah Rekomendasi', fontsize=12)
    ax.set_title('Top 10 Bidang Karir Paling Cocok', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    return plot_to_base64(fig)

def generate_satisfaction_pie(df):
    """Generate pie chart: Satisfaction distribution"""
    fig, ax = plt.subplots(figsize=(8, 8))
    satisfaction_counts = df['kepuasan'].value_counts()
    colors = {'Kurang Puas': '#ff9999', 'Puas': '#ffcc99', 'Sangat Puas': '#99ff99'}
    
    color_list = [colors.get(x, '#cccccc') for x in satisfaction_counts.index]
    wedges, texts, autotexts = ax.pie(satisfaction_counts.values, 
                                        labels=satisfaction_counts.index,
                                        autopct='%1.1f%%',
                                        colors=color_list,
                                        startangle=90)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Distribusi Kepuasan Kerja', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return plot_to_base64(fig)

def generate_elbow_curve(clustering_data):
    """Generate elbow curve plot"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if 'inertias' in clustering_data:
        inertias = clustering_data['inertias']
        k_values = range(1, len(inertias) + 1)
    else:
        k_values = range(1, 11)
        inertias = [500, 350, 250, 200, 180, 165, 155, 150, 148, 147]
    
    ax.plot(k_values, inertias, 'bo-', linewidth=2, markersize=8)
    optimal_k = clustering_data.get('optimal_k', 3)
    ax.axvline(x=optimal_k, color='r', linestyle='--', linewidth=2, 
               label=f"Optimal k = {optimal_k}")
    ax.set_xlabel('Jumlah Cluster (k)', fontsize=12)
    ax.set_ylabel('Inertia', fontsize=12)
    ax.set_title('Metode Elbow untuk K-Means', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    return plot_to_base64(fig)

def generate_cluster_scatter(clustering_data):
    """Generate cluster scatter plot"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if 'X_clustering_original' in clustering_data and 'cluster_labels' in clustering_data:
        X = clustering_data['X_clustering_original']
        labels = clustering_data['cluster_labels']
        centers = clustering_data.get('cluster_centers', None)
        
        # Use first 2 dimensions for visualization
        if X.shape[1] >= 2:
            scatter = ax.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', 
                               alpha=0.6, s=50, edgecolors='k', linewidth=0.5)
            
            if centers is not None and centers.shape[1] >= 2:
                ax.scatter(centers[:, 0], centers[:, 1], c='yellow', marker='*', 
                          s=500, edgecolors='red', linewidth=2, label='Centroid')
            
            ax.set_xlabel('Feature 1 (Scaled)', fontsize=12)
            ax.set_ylabel('Feature 2 (Scaled)', fontsize=12)
            ax.set_title('Visualisasi K-Means Clustering', fontsize=14, fontweight='bold')
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('Cluster')
            ax.legend()
            ax.grid(True, alpha=0.3)
    else:
        # Fallback plot if data structure is different
        ax.text(0.5, 0.5, 'Clustering data available', ha='center', va='center',
               transform=ax.transAxes, fontsize=14)
        ax.set_title('Visualisasi K-Means Clustering', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return plot_to_base64(fig)

@app.route('/')
def index():
    """Display survey form"""
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    """Process form and display prediction"""
    try:
        # Common fields for all
        email = request.form.get('email')
        nama = request.form.get('nama')
        tempat_tinggal = request.form.get('tempat_tinggal')
        jurusan = request.form.get('jurusan')
        status_bekerja = request.form.get('status_bekerja')
        
        # Initialize default values for fields that might not be sent
        nilai_rata = 75.0  # Default for SMK graduates
        waktu_kerja_pertama = 3  # Default: 3 months
        profesi_sekarang = request.form.get('profesi_sekarang', 'Other')
        tempat_kerja = request.form.get('tempat_kerja_saat_ini', tempat_tinggal)
        kepuasan = request.form.get('kepuasan', 'Puas')
        lama_kerja_1 = 0
        lama_kerja_2 = 0
        nyaman = request.form.get('kenyamanan', 'Iya')
        gaji = 5000000  # Default
        
        # ====== SCENARIO 1: SUDAH BEKERJA ======
        if status_bekerja == 'Ya':
            # Get employment data
            waktu_kerja_str = request.form.get('waktu_kerja_pertama', '< 3 bulan')
            # Convert time string to months
            waktu_map = {
                '< 3 bulan': 2,
                '3–6 bulan': 4,
                '6–12 bulan': 9,
                '1 tahun': 12
            }
            waktu_kerja_pertama = waktu_map.get(waktu_kerja_str, 3)
            
            # Get profesi (use existing from form)
            profesi_sekarang = request.form.get('profesi_sekarang', 'Other')
            
            # Get tempat kerja
            tempat_kerja = request.form.get('tempat_kerja_saat_ini', tempat_tinggal)
            
            # Get kepuasan
            kepuasan = request.form.get('kepuasan', 'Puas')
            
            # Get lama kerja
            lama_kerja_str = request.form.get('lama_kerja', '0')
            lama_kerja_1 = int(float(lama_kerja_str))  # Current job duration
            lama_kerja_2 = int(float(lama_kerja_str))  # Total experience (same if only one job)
            
            # Get nyaman
            nyaman = request.form.get('kenyamanan', 'Iya')
            
            # Get gaji
            gaji_kategori = request.form.get('gaji', 'UMR')
            gaji_map = {'Dibawah UMR': 2000000, 'UMR': 5000000, 'Diatas UMR': 10000000}
            gaji = gaji_map.get(gaji_kategori, 5000000)
            
            # Estimate nilai_rata from employment success (heuristic)
            # If comfortable and satisfied, assume better grades
            if nyaman == 'Iya' and kepuasan == 'Puas':
                nilai_rata = 82.0
            else:
                nilai_rata = 75.0
        
        # ====== SCENARIO 2: BELUM BEKERJA ======
        else:  # status_bekerja == 'Tidak'
            # For those not yet working, use default estimated values
            nilai_rata = 70.0  # Slightly lower estimate
            waktu_kerja_pertama = 0  # Haven't gotten job yet
            lama_kerja_1 = 0
            lama_kerja_2 = 0
            nyaman = 'Tidak'  # Haven't worked yet
            
            # Check if they're confident
            kepercayaan = request.form.get('kepercayaan_keterampilan', 'Tidak yakin')
            if kepercayaan == 'Yakin':
                nilai_rata = 78.0  # Slightly boost if confident
        
        # ====== FEATURE ENCODING ======
        # Encode categorical features
        tempat_tinggal_encoded = label_encoders['tempat_tinggal'].transform([tempat_tinggal])[0]
        jurusan_encoded = label_encoders['jurusan'].transform([jurusan])[0]
        profesi_encoded = label_encoders['profesi_sekarang'].transform([profesi_sekarang])[0]
        tempat_kerja_encoded = label_encoders['tempat_kerja'].transform([tempat_kerja])[0]
        kepuasan_encoded = label_encoders['kepuasan'].transform([kepuasan])[0]
        nyaman_encoded = label_encoders['nyaman'].transform([nyaman])[0]
        
        # Prepare feature array (must match training order)
        features = np.array([[
            tempat_tinggal_encoded,
            jurusan_encoded,
            nilai_rata,
            waktu_kerja_pertama,
            profesi_encoded,
            tempat_kerja_encoded,
            kepuasan_encoded,
            lama_kerja_1,
            lama_kerja_2,
            nyaman_encoded,
            gaji
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make predictions
        jurusan_pred_encoded = knn_jurusan.predict(features_scaled)[0]
        perusahaan_pred_encoded = knn_perusahaan.predict(features_scaled)[0]
        
        # Decode predictions
        jurusan_cocok = label_encoders['jurusan_cocok'].inverse_transform([jurusan_pred_encoded])[0]
        perusahaan_tepat = label_encoders['perusahaan_tepat'].inverse_transform([perusahaan_pred_encoded])[0]
        
        return render_template('result.html',
                             email=email,
                             nama=nama,
                             status_bekerja=status_bekerja,
                             jurusan_cocok=jurusan_cocok,
                             perusahaan_tepat=perusahaan_tepat)
    
    except Exception as e:
        return f"Error during prediction: {str(e)}", 500

@app.route('/metrics')
def metrics():
    """Display model performance metrics"""
    if metrics_data is None:
        return "Metrics data not available. Please run preprocessing.py first.", 500
    
    return render_template('metrics.html',
                         jurusan_accuracy=metrics_data['jurusan_accuracy'],
                         perusahaan_accuracy=metrics_data['perusahaan_accuracy'],
                         cm_jurusan=metrics_data['jurusan_confusion_matrix'],
                         cm_perusahaan=metrics_data['perusahaan_confusion_matrix'])

@app.route('/visualize')
def visualize():
    """Display data visualizations"""
    if visualization_data is None:
        return "Visualization data not available. Please run preprocessing.py first.", 500
    
    try:
        df = visualization_data['data']
        
        # Generate visualizations using helper functions
        plot1 = generate_gpa_vs_salary_scatter(df)
        plot2 = generate_work_time_vs_satisfaction(df)
        plot3 = generate_gpa_distribution(df)
        plot4 = generate_salary_distribution(df)
        plot5 = generate_correlation_heatmap(df)
        plot6 = generate_experience_box(df)
        plot7 = generate_top_jurusan_bar(df)
        plot8 = generate_satisfaction_pie(df)
        
        return render_template('visualize.html',
                             plot1=plot1, plot2=plot2, plot3=plot3, plot4=plot4,
                             plot5=plot5, plot6=plot6, plot7=plot7, plot8=plot8)
    
    except Exception as e:
        return f"Error generating visualizations: {str(e)}", 500
@app.route('/clustering')
def clustering():
    """Display K-Means clustering visualizations (Unsupervised Learning)"""
    if clustering_data is None:
        return "Clustering data not available. Please run preprocessing.py first.", 500
    
    try:
        # Generate clustering visualizations using helper functions
        elbow_plot = generate_elbow_curve(clustering_data)
        cluster_plot = generate_cluster_scatter(clustering_data)
        
        return render_template('clustering.html',
                             elbow_plot=elbow_plot,
                             cluster_plot=cluster_plot,
                             optimal_k=clustering_data.get('optimal_k', 3))
    
    except Exception as e:
        return f"Error generating clustering visualizations: {str(e)}", 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("JOB RECOMMENDATION SYSTEM")
    print("="*50)
    print("\nFlask app starting...")
    print("Open browser and go to: http://127.0.0.1:5000")
    print("Routes available:")
    print("  - http://127.0.0.1:5000/ (Home - Prediction Form)")
    print("  - http://127.0.0.1:5000/metrics (Model Performance)")
    print("  - http://127.0.0.1:5000/visualize (Supervised Learning Visualizations)")
    print("  - http://127.0.0.1:5000/clustering (Unsupervised Learning - K-Means)")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
