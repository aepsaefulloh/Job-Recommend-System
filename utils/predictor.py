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
    # Helper function to safely encode with fallback to most common class
    def safe_encode(encoder, value, feature_name):
        try:
            return encoder.transform([value])[0]
        except ValueError:
            # Value not seen during training, use most common class (index 0)
            print(f"Warning: '{value}' not found in {feature_name} encoder. Using default: '{encoder.classes_[0]}'")
            return 0
    
    # Encode categorical features with error handling
    tempat_tinggal_encoded = safe_encode(label_encoders['tempat_tinggal'], processed_data['tempat_tinggal'], 'tempat_tinggal')
    jurusan_encoded = safe_encode(label_encoders['jurusan'], processed_data['jurusan'], 'jurusan')
    profesi_encoded = safe_encode(label_encoders['profesi_sekarang'], processed_data['profesi_sekarang'], 'profesi_sekarang')
    tempat_kerja_encoded = safe_encode(label_encoders['tempat_kerja'], processed_data['tempat_kerja'], 'tempat_kerja')
    kepuasan_encoded = safe_encode(label_encoders['kepuasan'], processed_data['kepuasan'], 'kepuasan')
    nyaman_encoded = safe_encode(label_encoders['nyaman'], processed_data['nyaman'], 'nyaman')
    
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


def get_job_recommendations(jurusan_cocok, perusahaan_tepat, tempat_tinggal):
    """
    Generate job recommendations based on predicted jurusan and company type
    
    Args:
        jurusan_cocok: Predicted suitable major/field
        perusahaan_tepat: Predicted company compatibility
        tempat_tinggal: User's location
        
    Returns:
        list: List of recommended jobs with details
    """
    # Job database mapped to jurusan categories
    job_database = {
        'Akuntansi & Keuangan': [
            {
                'title': 'Staff Accounting',
                'company_type': 'Perusahaan Swasta',
                'description': 'Mengelola pencatatan keuangan, membuat laporan keuangan, dan rekonsiliasi akun',
                'salary_range': 'Rp 5.000.000 - Rp 8.000.000',
                'requirements': ['Lulusan SMK Akuntansi', 'Menguasai Microsoft Excel', 'Teliti dan detail'],
                'icon': '📊'
            },
            {
                'title': 'Tax Consultant',
                'company_type': 'Perusahaan Swasta',
                'description': 'Memberikan konsultasi perpajakan dan membantu perusahaan dalam pelaporan pajak',
                'salary_range': 'Rp 6.000.000 - Rp 10.000.000',
                'requirements': ['Memahami perpajakan', 'Komunikasi baik', 'Analitis'],
                'icon': '💼'
            },
            {
                'title': 'Finance Staff',
                'company_type': 'BUMN',
                'description': 'Mengelola arus kas, membuat budget, dan analisis keuangan perusahaan',
                'salary_range': 'Rp 5.500.000 - Rp 9.000.000',
                'requirements': ['Menguasai akuntansi', 'Microsoft Excel Advanced', 'Teliti'],
                'icon': '💰'
            },
            {
                'title': 'Auditor',
                'company_type': 'PNS',
                'description': 'Melakukan audit internal, memeriksa laporan keuangan, dan memberikan rekomendasi',
                'salary_range': 'Rp 5.000.000 - Rp 8.500.000',
                'requirements': ['Integritas tinggi', 'Analytical thinking', 'Detail oriented'],
                'icon': '🔍'
            }
        ],
        'Administrasi Perkantoran': [
            {
                'title': 'Staff Administrasi',
                'company_type': 'Perusahaan Swasta',
                'description': 'Mengelola dokumen, arsip, dan mendukung operasional kantor sehari-hari',
                'salary_range': 'Rp 4.500.000 - Rp 7.000.000',
                'requirements': ['Menguasai MS Office', 'Organisasi baik', 'Komunikatif'],
                'icon': '📋'
            },
            {
                'title': 'Sekretaris',
                'company_type': 'BUMN',
                'description': 'Membantu pimpinan dalam mengatur jadwal, korespondensi, dan administrasi',
                'salary_range': 'Rp 5.000.000 - Rp 8.500.000',
                'requirements': ['Multitasking', 'Professional', 'Komunikasi excellent'],
                'icon': '👔'
            },
            {
                'title': 'Receptionist',
                'company_type': 'Perusahaan Swasta',
                'description': 'Menyambut tamu, menjawab telepon, dan mengelola administrasi front office',
                'salary_range': 'Rp 4.000.000 - Rp 6.500.000',
                'requirements': ['Ramah', 'Penampilan menarik', 'Komunikasi baik'],
                'icon': '👋'
            },
            {
                'title': 'Data Entry',
                'company_type': 'Perusahaan Swasta',
                'description': 'Input data, verifikasi data, dan maintain database perusahaan',
                'salary_range': 'Rp 4.200.000 - Rp 6.000.000',
                'requirements': ['Typing cepat', 'Teliti', 'Microsoft Excel'],
                'icon': '⌨️'
            }
        ],
        'Bisnis & Pemasaran': [
            {
                'title': 'Digital Marketing',
                'company_type': 'Perusahaan Swasta',
                'description': 'Mengelola social media, membuat konten marketing, dan analisis campaign digital',
                'salary_range': 'Rp 5.000.000 - Rp 9.000.000',
                'requirements': ['Kreatif', 'Menguasai social media', 'Copywriting'],
                'icon': '📱'
            },
            {
                'title': 'Sales Executive',
                'company_type': 'Perusahaan Swasta',
                'description': 'Mencari klien baru, presentasi produk, dan mencapai target penjualan',
                'salary_range': 'Rp 4.500.000 - Rp 8.000.000 + Komisi',
                'requirements': ['Persuasif', 'Target oriented', 'Networking'],
                'icon': '🎯'
            },
            {
                'title': 'Account Executive',
                'company_type': 'BUMN',
                'description': 'Mengelola hubungan dengan klien, memberikan solusi bisnis, dan maintain partnership',
                'salary_range': 'Rp 6.000.000 - Rp 10.000.000',
                'requirements': ['Relationship building', 'Negotiation', 'Presentation skill'],
                'icon': '🤝'
            },
            {
                'title': 'Brand Ambassador',
                'company_type': 'Perusahaan Swasta',
                'description': 'Mempromosikan brand, event activation, dan meningkatkan brand awareness',
                'salary_range': 'Rp 4.000.000 - Rp 7.000.000',
                'requirements': ['Komunikatif', 'Energik', 'Public speaking'],
                'icon': '🌟'
            }
        ],
        'Komunikasi & Media': [
            {
                'title': 'Content Creator',
                'company_type': 'Perusahaan Swasta',
                'description': 'Membuat konten untuk social media, website, dan platform digital lainnya',
                'salary_range': 'Rp 5.000.000 - Rp 9.000.000',
                'requirements': ['Kreatif', 'Video/photo editing', 'Storytelling'],
                'icon': '🎬'
            },
            {
                'title': 'Customer Service',
                'company_type': 'BUMN',
                'description': 'Melayani customer, menangani komplain, dan memberikan solusi',
                'salary_range': 'Rp 4.500.000 - Rp 7.500.000',
                'requirements': ['Sabar', 'Problem solving', 'Komunikasi excellent'],
                'icon': '☎️'
            }
        ],
        'Teknologi Informasi': [
            {
                'title': 'IT Support',
                'company_type': 'Perusahaan Swasta',
                'description': 'Maintenance komputer, troubleshooting, dan support teknis IT',
                'salary_range': 'Rp 5.000.000 - Rp 8.000.000',
                'requirements': ['Hardware/software knowledge', 'Problem solving', 'Technical skill'],
                'icon': '💻'
            },
            {
                'title': 'Web Developer',
                'company_type': 'Perusahaan Swasta',
                'description': 'Membuat dan maintain website menggunakan HTML, CSS, JavaScript',
                'salary_range': 'Rp 6.000.000 - Rp 12.000.000',
                'requirements': ['HTML/CSS/JS', 'Framework knowledge', 'Problem solving'],
                'icon': '🌐'
            }
        ]
    }
    
    # Default to general recommendations if jurusan not found
    default_jobs = [
        {
            'title': 'Staff Administrasi',
            'company_type': 'Perusahaan Swasta',
            'description': 'Mengelola dokumen, arsip, dan mendukung operasional kantor',
            'salary_range': 'Rp 4.500.000 - Rp 7.000.000',
            'requirements': ['MS Office', 'Organisasi', 'Komunikasi'],
            'icon': '📋'
        }
    ]
    
    # Get jobs for the predicted jurusan
    jobs = job_database.get(jurusan_cocok, default_jobs)
    
    # Filter or prioritize by company type match
    recommended_jobs = []
    for job in jobs:
        # Check if company type matches
        match_score = 100 if job['company_type'] == perusahaan_tepat else 85
        
        job_copy = job.copy()
        job_copy['match_score'] = match_score
        job_copy['location'] = tempat_tinggal
        recommended_jobs.append(job_copy)
    
    # Sort by match score (highest first)
    recommended_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Return top 4 recommendations
    return recommended_jobs[:4]


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
            - recommended_jobs: List of recommended jobs
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
    
    # Generate job recommendations
    recommended_jobs = get_job_recommendations(
        jurusan_cocok, 
        perusahaan_tepat, 
        processed_data['tempat_tinggal']
    )
    
    # Return results
    return {
        'processed_data': processed_data,
        'jurusan_cocok': jurusan_cocok,
        'perusahaan_tepat': perusahaan_tepat,
        'jurusan_proba': jurusan_proba,
        'perusahaan_proba': perusahaan_proba,
        'recommended_jobs': recommended_jobs
    }
