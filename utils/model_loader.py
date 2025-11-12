"""
Model loader module for Job Recommendation System
Handles loading of all ML models and data files
"""

import pickle
import os


def load_models():
    """
    Load all required models and data files
    
    Returns:
        dict: Dictionary containing all loaded models and data:
            - knn_jurusan: KNN model for major recommendation
            - knn_perusahaan: KNN model for company compatibility
            - scaler: StandardScaler for feature normalization
            - label_encoders: Dict of LabelEncoders for categorical features
            - metrics_data: Model performance metrics
            - visualization_data: Data for visualization plots (optional)
            - clustering_data: K-Means clustering data (optional)
            
    Raises:
        FileNotFoundError: If required model files are not found
    """
    models = {}
    
    print("Loading models and encoders...")
    
    try:
        # Load KNN Jurusan Model
        with open('knn_jurusan_model.pkl', 'rb') as f:
            models['knn_jurusan'] = pickle.load(f)
        
        # Load KNN Perusahaan Model
        with open('knn_perusahaan_model.pkl', 'rb') as f:
            models['knn_perusahaan'] = pickle.load(f)
        
        # Load Scaler
        with open('scaler.pkl', 'rb') as f:
            models['scaler'] = pickle.load(f)
        
        # Load Label Encoders
        with open('label_encoders.pkl', 'rb') as f:
            models['label_encoders'] = pickle.load(f)
        
        # Load Metrics Data
        with open('metrics.pkl', 'rb') as f:
            models['metrics_data'] = pickle.load(f)
        print("✓ Metrics loaded!")
        
        # Load Visualization Data (optional)
        try:
            with open('visualization_data.pkl', 'rb') as f:
                models['visualization_data'] = pickle.load(f)
            print(f"✓ Visualization data loaded! ({models['visualization_data']['sample_size']} samples)")
        except FileNotFoundError:
            print("⚠ Visualization data not found. Run preprocessing.py to generate.")
            models['visualization_data'] = None
        
        # Load Clustering Data (optional)
        try:
            with open('clustering_data.pkl', 'rb') as f:
                models['clustering_data'] = pickle.load(f)
            print("✓ Clustering data loaded! (K-Means with Elbow Method)")
        except FileNotFoundError:
            print("⚠ Clustering data not found. Run preprocessing.py to generate.")
            models['clustering_data'] = None
        
        print("✓ Models and encoders loaded successfully!")
        return models
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run preprocessing.py first!")
        raise


def check_models_exist():
    """
    Check if all required model files exist
    
    Returns:
        bool: True if all required files exist, False otherwise
    """
    required_files = [
        'knn_jurusan_model.pkl',
        'knn_perusahaan_model.pkl',
        'scaler.pkl',
        'label_encoders.pkl',
        'metrics.pkl'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    return True
