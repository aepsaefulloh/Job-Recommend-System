"""
Job Recommendation System - Flask Web Application
Main application file with route handlers
"""

from flask import Flask, render_template, request

# Import utility modules
from utils.model_loader import load_models
from utils.predictor import make_predictions
from utils.visualization import (
    generate_gpa_vs_salary_scatter,
    generate_work_time_vs_satisfaction,
    generate_gpa_distribution,
    generate_salary_distribution,
    generate_correlation_heatmap,
    generate_experience_box,
    generate_top_jurusan_bar,
    generate_satisfaction_pie,
    generate_elbow_curve,
    generate_cluster_scatter
)

# Initialize Flask app
app = Flask(__name__)

# Load all models and data
models = load_models()

# Extract frequently used data
visualization_data = models.get('visualization_data')
metrics_data = models.get('metrics_data')
clustering_data = models.get('clustering_data')



# ============= ROUTE HANDLERS =============

@app.route('/')
def index():
    """Display survey form"""
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    """Process form and display prediction results"""
    try:
        # Make predictions using the predictor module
        predictions = make_predictions(request.form, models)
        
        # Extract results
        processed_data = predictions['processed_data']
        
        # Render results
        return render_template('result.html',
                             email=processed_data['email'],
                             nama=processed_data['nama'],
                             status_bekerja=processed_data['status_bekerja'],
                             jurusan_cocok=predictions['jurusan_cocok'],
                             perusahaan_tepat=predictions['perusahaan_tepat'])
    
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
