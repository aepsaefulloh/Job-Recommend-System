"""
Predictor module for Job Recommendation System
Handles data preprocessing and predictions
"""

import numpy as np


def preprocess_form_data(form_data, label_encoders):
    """
    Preprocess form data for prediction
    
    Args:
        form_data: Flask request.form data
        label_encoders: Dict of LabelEncoders
        
    Returns:
        dict: Processed data ready for prediction
    """
    # Extract basic information
    nama = form_data.get('nama', 'Anonymous')
    email = form_data.get('email', 'unknown@email.com')
    tempat_tinggal = form_data.get('tempat_tinggal', 'Jakarta')
    jurusan = form_data.get('jurusan', 'Teknik Informatika')
    status_bekerja = form_data.get('status_bekerja', 'Tidak')
    
    # Initialize default values
    nilai_rata = 75.0
    waktu_kerja_pertama = 3  # Default: 3 months
    profesi_sekarang = form_data.get('profesi_sekarang', 'Other')
    tempat_kerja = form_data.get('tempat_kerja_saat_ini', tempat_tinggal)
    kepuasan = form_data.get('kepuasan', 'Puas')
    lama_kerja_1 = 0
    lama_kerja_2 = 0
    nyaman = form_data.get('kenyamanan', 'Iya')
    gaji = 5000000  # Default
    
    # ====== SCENARIO 1: SUDAH BEKERJA ======
    if status_bekerja == 'Ya':
        # Get employment data
        waktu_kerja_str = form_data.get('waktu_kerja_pertama', '< 3 bulan')
        # Convert time string to months
        waktu_map = {
            '< 3 bulan': 2,
            '3–6 bulan': 4,
            '6–12 bulan': 9,
            '1 tahun': 12
        }
        waktu_kerja_pertama = waktu_map.get(waktu_kerja_str, 3)
        
        # Get profesi
        profesi_sekarang = form_data.get('profesi_sekarang', 'Other')
        
        # Get tempat kerja
        tempat_kerja = form_data.get('tempat_kerja_saat_ini', tempat_tinggal)
        
        # Get kepuasan
        kepuasan = form_data.get('kepuasan', 'Puas')
        
        # Get lama kerja
        lama_kerja_str = form_data.get('lama_kerja', '0')
        lama_kerja_1 = int(float(lama_kerja_str))  # Current job duration
        lama_kerja_2 = int(float(lama_kerja_str))  # Total experience (same if only one job)
        
        # Get nyaman
        nyaman = form_data.get('kenyamanan', 'Iya')
        
        # Get gaji
        gaji_kategori = form_data.get('gaji', 'UMR')
        gaji_map = {'Dibawah UMR': 2000000, 'UMR': 5000000, 'Diatas UMR': 10000000}
        gaji = gaji_map.get(gaji_kategori, 5000000)
        
        # Estimate nilai_rata from employment success (heuristic)
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
        kepercayaan = form_data.get('kepercayaan_keterampilan', 'Tidak yakin')
        if kepercayaan == 'Yakin':
            nilai_rata = 78.0  # Slightly boost if confident
    
    # Return processed data
    return {
        'nama': nama,
        'email': email,
        'tempat_tinggal': tempat_tinggal,
        'jurusan': jurusan,
        'status_bekerja': status_bekerja,
        'nilai_rata': nilai_rata,
        'waktu_kerja_pertama': waktu_kerja_pertama,
        'profesi_sekarang': profesi_sekarang,
        'tempat_kerja': tempat_kerja,
        'kepuasan': kepuasan,
        'lama_kerja_1': lama_kerja_1,
        'lama_kerja_2': lama_kerja_2,
        'nyaman': nyaman,
        'gaji': gaji
    }


def encode_features(processed_data, label_encoders):
    """
    Encode categorical features for prediction
    
    Args:
        processed_data: Dict of processed form data
        label_encoders: Dict of LabelEncoders
        
    Returns:
        numpy.ndarray: Encoded feature array
    """
    # Encode categorical features
    tempat_tinggal_encoded = label_encoders['tempat_tinggal'].transform([processed_data['tempat_tinggal']])[0]
    jurusan_encoded = label_encoders['jurusan'].transform([processed_data['jurusan']])[0]
    profesi_encoded = label_encoders['profesi_sekarang'].transform([processed_data['profesi_sekarang']])[0]
    tempat_kerja_encoded = label_encoders['tempat_kerja'].transform([processed_data['tempat_kerja']])[0]
    kepuasan_encoded = label_encoders['kepuasan'].transform([processed_data['kepuasan']])[0]
    nyaman_encoded = label_encoders['nyaman'].transform([processed_data['nyaman']])[0]
    
    # Prepare feature array (must match training order)
    features = np.array([[
        tempat_tinggal_encoded,
        jurusan_encoded,
        processed_data['nilai_rata'],
        processed_data['waktu_kerja_pertama'],
        profesi_encoded,
        tempat_kerja_encoded,
        kepuasan_encoded,
        processed_data['lama_kerja_1'],
        processed_data['lama_kerja_2'],
        nyaman_encoded,
        processed_data['gaji']
    ]])
    
    return features


def make_predictions(form_data, models):
    """
    Make predictions based on form data
    
    Args:
        form_data: Flask request.form data
        models: Dict containing all loaded models
        
    Returns:
        dict: Prediction results including:
            - processed_data: Preprocessed input data
            - jurusan_cocok: Predicted suitable major
            - perusahaan_tepat: Predicted company compatibility
            - jurusan_proba: Prediction probabilities for major
            - perusahaan_proba: Prediction probabilities for company
    """
    # Extract models
    knn_jurusan = models['knn_jurusan']
    knn_perusahaan = models['knn_perusahaan']
    scaler = models['scaler']
    label_encoders = models['label_encoders']
    
    # Preprocess form data
    processed_data = preprocess_form_data(form_data, label_encoders)
    
    # Encode features
    features = encode_features(processed_data, label_encoders)
    
    # Scale features
    features_scaled = scaler.transform(features)
    
    # Make predictions
    jurusan_pred_encoded = knn_jurusan.predict(features_scaled)[0]
    perusahaan_pred_encoded = knn_perusahaan.predict(features_scaled)[0]
    
    # Get prediction probabilities
    jurusan_proba = knn_jurusan.predict_proba(features_scaled)[0]
    perusahaan_proba = knn_perusahaan.predict_proba(features_scaled)[0]
    
    # Decode predictions
    jurusan_cocok = label_encoders['jurusan_cocok'].inverse_transform([jurusan_pred_encoded])[0]
    perusahaan_tepat = label_encoders['perusahaan_tepat'].inverse_transform([perusahaan_pred_encoded])[0]
    
    # Return results
    return {
        'processed_data': processed_data,
        'jurusan_cocok': jurusan_cocok,
        'perusahaan_tepat': perusahaan_tepat,
        'jurusan_proba': jurusan_proba,
        'perusahaan_proba': perusahaan_proba
    }
