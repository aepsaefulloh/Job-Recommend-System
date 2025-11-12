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
    # Extract basic information (Section 1)
    nama = form_data.get('nama', 'Anonymous')
    email = form_data.get('email', 'unknown@email.com')
    tempat_tinggal = form_data.get('tempat_tinggal', 'Jakarta')
    jurusan = form_data.get('jurusan', 'Akuntansi')
    status_bekerja = form_data.get('status_bekerja', 'Tidak')
    
    # Initialize default values
    waktu_kerja_pertama = 3  # Default: 3 months
    profesi_sekarang = form_data.get('profesi_sekarang', 'Other')
    tempat_kerja = form_data.get('tempat_kerja_saat_ini', tempat_tinggal)
    kepuasan = form_data.get('kepuasan', 'Puas')
    lama_kerja_1 = 0
    lama_kerja_2 = 0
    nyaman = form_data.get('kenyamanan', 'Iya')
    gaji = 5000000  # Default
    
    # New SMK survey fields (initialized with defaults)
    cara_mendapat_pekerjaan = 'Mencari sendiri'
    kemudahan_cari_kerja = 'Mudah'
    bantuan_sekolah = 'Tidak'
    kesesuaian_minat = 'Sesuai'
    jenis_perusahaan = 'Perusahaan Swasta'
    kesesuaian_jurusan = 'Ya'
    rencana_pindah_kerja = 'Tidak'
    alasan_belum_kerja = 'Sedang mencari pekerjaan'
    rencana_kerja_sesuai_jurusan = 'Ya'
    kendala_utama = 'Kurangnya pengalaman kerja'
    ikut_pelatihan = 'Tidak'
    gunakan_platform_online = 'Ya'
    kepercayaan_keterampilan = 'Yakin'
    bersedia_rekomendasi_sekolah = 'Ya'
    
    # ====== SCENARIO 1: SUDAH BEKERJA (Section 2) ======
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
        
        # NEW: Get additional SMK survey fields for employed
        cara_mendapat_pekerjaan_list = form_data.getlist('cara_mendapat_pekerjaan')
        cara_mendapat_pekerjaan = ', '.join(cara_mendapat_pekerjaan_list) if cara_mendapat_pekerjaan_list else 'Mencari sendiri'
        
        kemudahan_cari_kerja = form_data.get('kemudahan_cari_kerja', 'Mudah')
        bantuan_sekolah = form_data.get('bantuan_sekolah', 'Tidak')
        kesesuaian_minat = form_data.get('kesesuaian_minat', 'Sesuai')
        jenis_perusahaan = form_data.get('jenis_perusahaan', 'Perusahaan Swasta')
        kesesuaian_jurusan = form_data.get('kesesuaian_jurusan', 'Ya')
        rencana_pindah_kerja = form_data.get('rencana_pindah_kerja', 'Tidak')
    
    # ====== SCENARIO 2: BELUM BEKERJA (Section 3) ======
    else:  # status_bekerja == 'Tidak'
        # For those not yet working, use default values
        waktu_kerja_pertama = 0  # Haven't gotten job yet
        lama_kerja_1 = 0
        lama_kerja_2 = 0
        nyaman = 'Tidak'  # Haven't worked yet
        
        # NEW: Get additional SMK survey fields for unemployed
        alasan_belum_kerja = form_data.get('alasan_belum_kerja', 'Sedang mencari pekerjaan')
        kemudahan_cari_kerja = form_data.get('kemudahan_cari_kerja_belum', 'Sulit')
        bantuan_sekolah = form_data.get('bantuan_sekolah_belum', 'Tidak')
        rencana_kerja_sesuai_jurusan = form_data.get('rencana_kerja_sesuai_jurusan', 'Ya')
        kendala_utama = form_data.get('kendala_utama', 'Kurangnya pengalaman kerja')
        ikut_pelatihan = form_data.get('ikut_pelatihan', 'Tidak')
        gunakan_platform_online = form_data.get('gunakan_platform_online', 'Ya')
        kepercayaan_keterampilan = form_data.get('kepercayaan_keterampilan', 'Tidak yakin')
        bersedia_rekomendasi_sekolah = form_data.get('bersedia_rekomendasi_sekolah', 'Ya')
    
    # Return processed data (without nilai_rata - SMK doesn't use GPA)
    return {
        'nama': nama,
        'email': email,
        'tempat_tinggal': tempat_tinggal,
        'jurusan': jurusan,
        'status_bekerja': status_bekerja,
        'waktu_kerja_pertama': waktu_kerja_pertama,
        'profesi_sekarang': profesi_sekarang,
        'tempat_kerja': tempat_kerja,
        'kepuasan': kepuasan,
        'lama_kerja_1': lama_kerja_1,
        'lama_kerja_2': lama_kerja_2,
        'nyaman': nyaman,
        'gaji': gaji,
        # New SMK survey fields
        'cara_mendapat_pekerjaan': cara_mendapat_pekerjaan,
        'kemudahan_cari_kerja': kemudahan_cari_kerja,
        'bantuan_sekolah': bantuan_sekolah,
        'kesesuaian_minat': kesesuaian_minat,
        'jenis_perusahaan': jenis_perusahaan,
        'kesesuaian_jurusan': kesesuaian_jurusan,
        'rencana_pindah_kerja': rencana_pindah_kerja,
        'alasan_belum_kerja': alasan_belum_kerja,
        'rencana_kerja_sesuai_jurusan': rencana_kerja_sesuai_jurusan,
        'kendala_utama': kendala_utama,
        'ikut_pelatihan': ikut_pelatihan,
        'gunakan_platform_online': gunakan_platform_online,
        'kepercayaan_keterampilan': kepercayaan_keterampilan,
        'bersedia_rekomendasi_sekolah': bersedia_rekomendasi_sekolah
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
    # NOTE: nilai_rata removed - SMK doesn't use GPA system
    features = np.array([[
        tempat_tinggal_encoded,
        jurusan_encoded,
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
