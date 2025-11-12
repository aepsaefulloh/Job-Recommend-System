"""
PREPROCESSING FOR NEW SURVEY DATASET - job_survey.csv
Trains KNN models and generates clustering data using 1000-record synthetic dataset
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, silhouette_score
import pickle

print("="*70)
print("JOB RECOMMENDATION SYSTEM - PREPROCESSING (NEW DATASET)")
print("="*70)

# Load new survey dataset
print("\n1. Loading new survey dataset...")
df = pd.read_csv('job_survey.csv')
print(f"✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Filter to only employed records (have full employment data)
print("\n2. Filtering for employed alumni (status_bekerja = 'Ya')...")
df = df[df['status_bekerja'] == 'Ya'].copy()
print(f"✓ Employed records: {len(df)} rows")

if len(df) < 50:
    print("❌ Error: Not enough employed records for training!")
    exit(1)

print(f"\nDataset Info:")
print(f"  Columns: {len(df.columns)}")
print(f"  Features available: {list(df.columns)[:15]}...")

# Check for required columns (UPDATED: removed nilai_rata - SMK doesn't use GPA)
required_cols = ['tempat_tinggal', 'jurusan', 'jurusan_cocok', 'perusahaan_tepat']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    print(f"❌ Error: Missing required columns: {missing_cols}")
    exit(1)

# Prepare features for training
print("\n3. Preparing features and targets...")

# Map/create features needed for KNN
features_needed = {
    'tempat_tinggal': 'tempat_tinggal',
    'jurusan': 'jurusan',
    'profesi_sekarang': 'profesi_sekarang',
    'tempat_kerja': 'tempat_kerja_saat_ini',
    'kepuasan': 'kepuasan',
    'nyaman': 'kenyamanan'
}

# Create working dataframe with renamed columns
df_work = df.copy()

# Ensure all required features exist
for feat_name, df_col in features_needed.items():
    if df_col not in df_work.columns:
        print(f"  ⚠ Missing: {df_col}, using default values")
        df_work[feat_name] = 'Other'
    else:
        df_work[feat_name] = df_work[df_col]

# Create features for other needed columns
if 'waktu_kerja_pertama' not in df_work.columns:
    df_work['waktu_kerja_pertama'] = 0.5  # Default: ~2 weeks
    
if 'lama_kerja_1' not in df_work.columns:
    df_work['lama_kerja_1'] = df_work['lama_kerja'].astype(float) if 'lama_kerja' in df_work.columns else 0

if 'lama_kerja_2' not in df_work.columns:
    df_work['lama_kerja_2'] = df_work['lama_kerja'].astype(float) if 'lama_kerja' in df_work.columns else 0

# Ensure gaji is numeric
if 'gaji' in df_work.columns:
    df_work['gaji'] = pd.to_numeric(df_work['gaji'], errors='coerce').fillna(5000000)
else:
    df_work['gaji'] = 5000000

# Map time strings to numeric if needed
if 'waktu_kerja_pertama' in df_work.columns and isinstance(df_work['waktu_kerja_pertama'].iloc[0], str):
    waktu_map = {
        '< 3 bulan': 1,
        '3–6 bulan': 3,
        '6–12 bulan': 9,
        '1 tahun': 12
    }
    df_work['waktu_kerja_pertama'] = df_work['waktu_kerja_pertama'].map(waktu_map).fillna(3)

print("✓ Features prepared")

# Encode categorical features
print("\n4. Encoding categorical features...")
categorical_features = ['tempat_tinggal', 'jurusan', 'profesi_sekarang', 'tempat_kerja', 'kepuasan', 'nyaman']
label_encoders = {}

for feature in categorical_features:
    le = LabelEncoder()
    df_work[feature + '_encoded'] = le.fit_transform(df_work[feature].astype(str))
    label_encoders[feature] = le
    print(f"  ✓ '{feature}': {len(le.classes_)} unique values")

# Encode target variables
print("\n5. Encoding target variables...")
le_jurusan = LabelEncoder()
df_work['jurusan_cocok_encoded'] = le_jurusan.fit_transform(df_work['jurusan_cocok'].astype(str))
label_encoders['jurusan_cocok'] = le_jurusan
print(f"  ✓ 'jurusan_cocok': {len(le_jurusan.classes_)} categories")
print(f"    Categories: {list(le_jurusan.classes_[:5])}...")

le_perusahaan = LabelEncoder()
df_work['perusahaan_tepat_encoded'] = le_perusahaan.fit_transform(df_work['perusahaan_tepat'].astype(str))
label_encoders['perusahaan_tepat'] = le_perusahaan
print(f"  ✓ 'perusahaan_tepat': {len(le_perusahaan.classes_)} categories")
print(f"    Categories: {list(le_perusahaan.classes_)}")

# Prepare feature matrix (10 features - WITHOUT nilai_rata for SMK)
print("\n6. Building feature matrix...")
feature_columns = [
    'tempat_tinggal_encoded', 'jurusan_encoded',
    'waktu_kerja_pertama', 'profesi_sekarang_encoded', 
    'tempat_kerja_encoded', 'kepuasan_encoded',
    'lama_kerja_1', 'lama_kerja_2', 'nyaman_encoded', 'gaji'
]

X = df_work[feature_columns].values
y_jurusan = df_work['jurusan_cocok_encoded'].values
y_perusahaan = df_work['perusahaan_tepat_encoded'].values

print(f"  ✓ Feature matrix shape: {X.shape}")
print(f"  ✓ Jurusan target shape: {y_jurusan.shape}")
print(f"  ✓ Perusahaan target shape: {y_perusahaan.shape}")

# Validate no NaN values
if np.isnan(X).any():
    print("  ⚠ Found NaN values in features, filling with median...")
    col_medians = np.nanmedian(X, axis=0)
    inds = np.where(np.isnan(X))
    X[inds] = np.take(col_medians, inds[1])

# Split data
print("\n7. Splitting data (80% train, 20% test)...")
X_train, X_test, y_jurusan_train, y_jurusan_test, y_perusahaan_train, y_perusahaan_test = train_test_split(
    X, y_jurusan, y_perusahaan, test_size=0.2, random_state=42
)
print(f"  ✓ Training set: {X_train.shape[0]} samples")
print(f"  ✓ Test set: {X_test.shape[0]} samples")

# Scale features
print("\n8. Scaling features with StandardScaler...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("  ✓ Features scaled successfully!")

# Train KNN model for Jurusan prediction
print("\n9. Training KNN model for 'Jurusan Cocok' prediction...")
knn_jurusan = KNeighborsClassifier(n_neighbors=5)
knn_jurusan.fit(X_train_scaled, y_jurusan_train)
y_jurusan_pred = knn_jurusan.predict(X_test_scaled)
acc_jurusan = accuracy_score(y_jurusan_test, y_jurusan_pred)
print(f"  ✓ Accuracy: {acc_jurusan*100:.2f}%")
print("\n  Classification Report (Jurusan):")
print(classification_report(y_jurusan_test, y_jurusan_pred, 
                          target_names=le_jurusan.classes_, zero_division=0))

# Train KNN model for Perusahaan prediction
print("\n10. Training KNN model for 'Perusahaan Tepat' prediction...")
knn_perusahaan = KNeighborsClassifier(n_neighbors=5)
knn_perusahaan.fit(X_train_scaled, y_perusahaan_train)
y_perusahaan_pred = knn_perusahaan.predict(X_test_scaled)
acc_perusahaan = accuracy_score(y_perusahaan_test, y_perusahaan_pred)
print(f"  ✓ Accuracy: {acc_perusahaan*100:.2f}%")
print("\n  Classification Report (Perusahaan):")
print(classification_report(y_perusahaan_test, y_perusahaan_pred, 
                           target_names=le_perusahaan.classes_, zero_division=0))

# Confusion matrices
cm_jurusan = confusion_matrix(y_jurusan_test, y_jurusan_pred)
cm_perusahaan = confusion_matrix(y_perusahaan_test, y_perusahaan_pred)

print("\n11. Confusion Matrix (Jurusan):")
print(cm_jurusan)
print("\n    Confusion Matrix (Perusahaan):")
print(cm_perusahaan)

# Save models and encoders
print("\n12. Saving models, scaler, and encoders...")
with open('knn_jurusan_model.pkl', 'wb') as f:
    pickle.dump(knn_jurusan, f)
print("    ✓ knn_jurusan_model.pkl saved")

with open('knn_perusahaan_model.pkl', 'wb') as f:
    pickle.dump(knn_perusahaan, f)
print("    ✓ knn_perusahaan_model.pkl saved")

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("    ✓ scaler.pkl saved")

with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
print("    ✓ label_encoders.pkl saved")

# Save metrics
metrics = {
    'jurusan_accuracy': acc_jurusan,
    'perusahaan_accuracy': acc_perusahaan,
    'jurusan_confusion_matrix': cm_jurusan,
    'perusahaan_confusion_matrix': cm_perusahaan,
    'feature_columns': feature_columns,
    'jurusan_labels': le_jurusan.classes_,
    'perusahaan_labels': le_perusahaan.classes_,
    'dataset_source': 'job_survey.csv',
    'total_records_used': len(df_work)
}

with open('metrics.pkl', 'wb') as f:
    pickle.dump(metrics, f)
print("    ✓ metrics.pkl saved")

# Save sample data for visualization
print("\n13. Saving visualization data...")
sample_size = min(500, len(df_work))
df_sample = df_work.sample(n=sample_size, random_state=42)
visualization_data = {
    'data': df_sample,
    'sample_size': sample_size,
    'dataset_source': 'job_survey.csv'
}
with open('visualization_data.pkl', 'wb') as f:
    pickle.dump(visualization_data, f)
print(f"    ✓ visualization_data.pkl saved ({sample_size} samples)")

# UNSUPERVISED LEARNING - K-MEANS CLUSTERING
print("\n14. UNSUPERVISED LEARNING: K-Means Clustering...")
print("    Selecting features for clustering (gaji, lama_kerja_2, waktu_kerja_pertama)...")

# Ensure numeric values (UPDATED: removed nilai_rata for SMK)
df_work['gaji'] = pd.to_numeric(df_work['gaji'], errors='coerce').fillna(5000000)
df_work['lama_kerja_2'] = pd.to_numeric(df_work['lama_kerja_2'], errors='coerce').fillna(2)
df_work['waktu_kerja_pertama'] = pd.to_numeric(df_work['waktu_kerja_pertama'], errors='coerce').fillna(3)

clustering_features = ['gaji', 'lama_kerja_2', 'waktu_kerja_pertama']
X_clustering = df_work[clustering_features].values

# Scale for clustering
scaler_clustering = StandardScaler()
X_clustering_scaled = scaler_clustering.fit_transform(X_clustering)
print(f"    ✓ Clustering data shape: {X_clustering_scaled.shape}")

# Elbow method to find optimal k
print("\n15. Applying Elbow Method to find optimal k...")
inertias = []
silhouette_scores = []
K_range = range(1, 11)

for k in K_range:
    kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans_temp.fit(X_clustering_scaled)
    inertias.append(kmeans_temp.inertia_)
    if k > 1:
        try:
            sil_score = silhouette_score(X_clustering_scaled, kmeans_temp.labels_)
            silhouette_scores.append(sil_score)
        except:
            silhouette_scores.append(0)
    print(f"    k={k}: Inertia={kmeans_temp.inertia_:.2f}", end="")
    if k > 1:
        print(f", Silhouette={silhouette_scores[-1]:.4f}")
    else:
        print()

# Use optimal k (typically k=3)
optimal_k = 3
print(f"\n16. Training K-Means with optimal k={optimal_k}...")
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_clustering_scaled)
df_work['cluster'] = cluster_labels

print(f"    ✓ Cluster distribution:")
for i in range(optimal_k):
    count = (cluster_labels == i).sum()
    pct = (count/len(cluster_labels))*100
    print(f"      Cluster {i}: {count} samples ({pct:.1f}%)")

# Calculate cluster centers (inverse transform to original scale)
cluster_centers_original = scaler_clustering.inverse_transform(kmeans.cluster_centers_)
print(f"\n    Cluster Centers (Original Scale):")
for i, center in enumerate(cluster_centers_original):
    print(f"      Cluster {i}: gaji={center[0]:,.0f}, lama_kerja_2={center[1]:.2f}, waktu_kerja_pertama={center[2]:.2f}")

# Save clustering data
clustering_data = {
    'kmeans_model': kmeans,
    'scaler_clustering': scaler_clustering,
    'inertias': inertias,
    'silhouette_scores': silhouette_scores,
    'optimal_k': optimal_k,
    'cluster_labels': cluster_labels,
    'cluster_centers': cluster_centers_original,
    'X_clustering_original': X_clustering,
    'feature_names': clustering_features,
    'dataset_source': 'job_survey.csv'
}

with open('clustering_data.pkl', 'wb') as f:
    pickle.dump(clustering_data, f)
print("\n    ✓ clustering_data.pkl saved")

print("\n" + "="*70)
print("✅ PREPROCESSING COMPLETED SUCCESSFULLY!")
print("="*70)
print(f"\n📊 Model Performance:")
print(f"  - Jurusan Cocok Accuracy: {acc_jurusan*100:.2f}%")
print(f"  - Perusahaan Tepat Accuracy: {acc_perusahaan*100:.2f}%")

print(f"\n📈 Dataset Statistics:")
print(f"  - Source: job_survey_1000.csv")
print(f"  - Employed Records Used: {len(df_work)}")
print(f"  - Training Samples: {X_train.shape[0]}")
print(f"  - Test Samples: {X_test.shape[0]}")
print(f"  - Clustering Samples: {X_clustering.shape[0]}")

print(f"\n💾 Files saved:")
print("  1. knn_jurusan_model.pkl")
print("  2. knn_perusahaan_model.pkl")
print("  3. scaler.pkl")
print("  4. label_encoders.pkl")
print("  5. metrics.pkl (updated with new data)")
print("  6. visualization_data.pkl (updated with new data)")
print("  7. clustering_data.pkl (K-Means with Elbow Method)")

print("\n🎯 Ready to use with:")
print("  - Form submissions via app.py")
print("  - Metrics visualization")
print("  - Feature distribution analysis")
print("  - K-Means clustering analysis")
