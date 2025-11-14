# Dynamic Data Integration - Job Requirement System

## Overview
Sistem sekarang mendukung **data dinamis** untuk halaman **Metrics** dan **Visualize**, mengambil data langsung dari `job_survey.csv` secara real-time.

## Fitur Dinamis

### 1. **Dynamic Metrics** (`/metrics`)
Menghitung metrics model secara real-time dari CSV:

#### Metrics yang Dihitung:
- **Jurusan Accuracy**: Persentase kesesuaian jurusan (kolom `kesesuaian_jurusan`)
- **Perusahaan Accuracy**: Persentase ketepatan perusahaan (kolom `perusahaan_tepat`)
- **Total Records**: Jumlah total records alumni yang sudah bekerja
- **Confusion Matrix**: Matrix untuk evaluasi model perusahaan

#### Data Source:
```python
# Membaca dari job_survey.csv
df = pd.read_csv('job_survey.csv')
df_employed = df[df['status_bekerja'] == 'Ya']  # Filter hanya yang bekerja
```

#### Current Statistics (Based on Latest CSV):
- **Total Records**: 7,000 entries
- **Employed Alumni**: 5,198 records
- **Jurusan Accuracy**: 70.72%
- **Perusahaan Accuracy**: 64.51%

### 2. **Dynamic Visualizations** (`/visualize`)
8 grafik visualisasi yang dihasilkan secara real-time:

1. **Plot 1**: Hubungan Pengalaman Kerja dengan Gaji
   - X-axis: `lama_kerja_2` (pengalaman kerja)
   - Y-axis: `gaji`
   - Color: `perusahaan_tepat` (Tepat/Tidak Tepat)

2. **Plot 2**: Waktu Kerja Pertama vs Kepuasan
   - X-axis: `waktu_kerja_pertama_bulan`
   - Y-axis: `kepuasan` (mapped ke numeric)
   - Color: `nyaman` (Ya/Tidak)

3. **Plot 3**: Kepuasan Kerja per Jenis Perusahaan
   - Bar chart: `jenis_perusahaan` vs `kepuasan`
   - Stacked/grouped by satisfaction level

4. **Plot 4**: Distribusi Gaji Berdasarkan Kepuasan
   - Histogram: `gaji` distribution
   - Colored by: `kepuasan`

5. **Plot 5**: Matriks Korelasi (placeholder)
   - Currently disabled due to seaborn issues
   - Will show correlation between numeric features

6. **Plot 6**: Distribusi Pengalaman Kerja
   - Box plot: `lama_kerja_2`
   - Grouped by: `perusahaan_tepat`

7. **Plot 7**: Top 10 Bidang Karir Paling Cocok
   - Bar chart: `jurusan_cocok` frequency
   - Top 10 most recommended careers

8. **Plot 8**: Distribusi Kepuasan Kerja
   - Pie chart: `kepuasan` distribution
   - Shows percentage per satisfaction level

## Keuntungan Dynamic Data

### 1. **Real-Time Updates**
- Data metrics dan visualisasi selalu up-to-date dengan CSV terbaru
- Tidak perlu menjalankan `preprocessing.py` untuk update metrics
- Perubahan pada `job_survey.csv` langsung tercermin di dashboard

### 2. **Automatic Fallback**
- Jika CSV tidak tersedia, sistem fallback ke cached data dari `preprocessing.py`
- Memastikan aplikasi tetap berjalan meskipun ada masalah dengan CSV

### 3. **Error Handling**
- Semua fungsi visualisasi memiliki error handling
- Jika kolom tidak tersedia, menampilkan pesan "Data tidak tersedia"
- Tidak akan crash meskipun ada missing data

### 4. **Column Mapping**
- Sistem secara otomatis map kolom alternatif:
  - `kenyamanan` → `nyaman`
  - `tempat_kerja_saat_ini` → `tempat_kerja`
- Support untuk berbagai format CSV

## Implementation Details

### Backend Functions (`app.py`)

#### 1. Load Survey Data
```python
def load_survey_data():
    """Load job_survey.csv and return dataframe"""
    try:
        df = pd.read_csv('job_survey.csv')
        return df
    except Exception as e:
        print(f"Error loading survey data: {e}")
        return None
```

#### 2. Calculate Metrics
```python
def calculate_dynamic_metrics():
    """Calculate model metrics dynamically from job_survey.csv"""
    df = load_survey_data()
    df_employed = df[df['status_bekerja'] == 'Ya'].copy()
    
    # Calculate accuracies
    jurusan_accuracy = ...
    perusahaan_accuracy = ...
    
    return metrics_data
```

### Visualization Functions (`utils/visualization.py`)

Semua fungsi visualisasi telah diupdate dengan:
- Column existence checking
- Missing data handling
- Alternative column mapping
- Error messages untuk missing data

Example:
```python
def generate_gpa_vs_salary_scatter(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Check if required columns exist
    if 'lama_kerja_2' not in df.columns or 'gaji' not in df.columns:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ...)
        return plot_to_base64(fig)
    
    # Generate plot...
```

## Usage

### Accessing Dynamic Pages

1. **Metrics Page**: 
   ```
   http://127.0.0.1:5000/metrics
   ```
   - Menampilkan accuracy, confusion matrix, dataset info

2. **Visualize Page**:
   ```
   http://127.0.0.1:5000/visualize
   ```
   - Menampilkan 8 grafik visualisasi data

### Updating Data

1. Edit `job_survey.csv` dengan data baru
2. Refresh halaman `/metrics` atau `/visualize`
3. Data akan otomatis ter-update tanpa restart server

### CSV Requirements

Kolom minimal yang diperlukan:
```
- email
- nama
- tempat_tinggal
- jurusan
- status_bekerja
- profesi_sekarang
- jenis_perusahaan
- kesesuaian_jurusan
- kepuasan
- perusahaan_tepat
- lama_kerja_1
- lama_kerja_2
- gaji
- waktu_kerja_pertama_bulan
- nyaman (atau kenyamanan)
```

## Testing

Test dynamic data loading:
```bash
cd /c/xampp/htdocs/python/Job-Requirement-System
py -c "
import pandas as pd
df = pd.read_csv('job_survey.csv')
print(f'Total records: {len(df)}')
df_employed = df[df['status_bekerja'] == 'Ya']
print(f'Employed: {len(df_employed)}')
"
```

## Future Enhancements

1. **Caching**: Implement Redis/Memcached untuk cache visualisasi
2. **Lazy Loading**: Generate plots on-demand untuk performance
3. **Export**: Export metrics dan visualisasi ke PDF/Excel
4. **Filtering**: UI untuk filter data berdasarkan tahun, jurusan, dll
5. **Real-time Updates**: WebSocket untuk auto-refresh saat CSV berubah

## Notes

- Sistem saat ini menggunakan **fallback mechanism** ke cached data jika CSV tidak tersedia
- Plot 5 (Correlation Heatmap) sementara disabled karena seaborn import issues
- Semua visualisasi menggunakan matplotlib dengan Agg backend (non-GUI)
- Base64 encoding digunakan untuk embed images di HTML

---

**Last Updated**: November 14, 2025
**Version**: 2.0 (Dynamic Data)
