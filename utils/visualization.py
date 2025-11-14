"""
Visualization helper functions for Job Recommendation System
Generates various plots and charts for data analysis
"""

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns  # Temporarily commented out due to import issues
import io
import base64


def plot_to_base64(fig):
    """
    Convert matplotlib figure to base64 encoded image
    
    Args:
        fig: matplotlib figure object
        
    Returns:
        str: Base64 encoded PNG image string
    """
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=80)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return plot_url


def generate_gpa_vs_salary_scatter(df):
    """
    Generate scatter plot: Experience vs Salary (replaces GPA plot for SMK)
    
    Args:
        df: DataFrame with 'lama_kerja_2', 'gaji', 'perusahaan_tepat' columns
        
    Returns:
        str: Base64 encoded plot image
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Check if required columns exist
    if 'lama_kerja_2' not in df.columns or 'gaji' not in df.columns:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
        ax.set_title('Hubungan Pengalaman Kerja dengan Gaji', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plot_to_base64(fig)
    
    # Handle perusahaan_tepat mapping
    tepat_map = {'Tepat': 0, 'Tidak Tepat': 1}
    if 'perusahaan_tepat' in df.columns:
        colors = [tepat_map.get(x, 0) for x in df['perusahaan_tepat']]
    else:
        colors = 'blue'
    
    scatter = ax.scatter(df['lama_kerja_2'], df['gaji'], 
                        c=colors, cmap='RdYlGn_r', alpha=0.6, s=50)
    ax.set_xlabel('Lama Kerja (Tahun)', fontsize=12)
    ax.set_ylabel('Gaji (IDR)', fontsize=12)
    ax.set_title('Hubungan Pengalaman Kerja dengan Gaji', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_work_time_vs_satisfaction(df):
    """
    Generate plot: Work time first vs Satisfaction
    
    Args:
        df: DataFrame with 'waktu_kerja_pertama', 'kepuasan', 'nyaman' columns
        
    Returns:
        str: Base64 encoded plot image
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Check if required columns exist
    if 'waktu_kerja_pertama_bulan' not in df.columns or 'kepuasan' not in df.columns:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
        ax.set_title('Waktu Kerja Pertama vs Kepuasan', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plot_to_base64(fig)
    
    satisfaction_map = {'Tidak puas': 1, 'Kurang Puas': 1, 'Puas': 2, 'Sangat Puas': 3}
    df_plot = df.copy()
    df_plot['satisfaction_num'] = df_plot['kepuasan'].map(satisfaction_map).fillna(2)
    
    if 'nyaman' in df_plot.columns:
        df_plot['nyaman_num'] = (df_plot['nyaman'] == 'Ya').astype(int)
        colors = df_plot['nyaman_num']
    else:
        colors = 'blue'
    
    scatter = ax.scatter(df_plot['waktu_kerja_pertama_bulan'], df_plot['satisfaction_num'],
                        c=colors, cmap='coolwarm', alpha=0.6, s=50)
    ax.set_xlabel('Waktu Kerja Pertama (Bulan)', fontsize=12)
    ax.set_ylabel('Kepuasan Kerja', fontsize=12)
    ax.set_title('Waktu Kerja Pertama vs Kepuasan', fontsize=14, fontweight='bold')
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['Kurang Puas', 'Puas', 'Sangat Puas'])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_gpa_distribution(df):
    """
    Generate bar chart: Satisfaction by Company Type (replaces GPA distribution for SMK)
    
    Args:
        df: DataFrame with 'jenis_perusahaan', 'kepuasan' columns
        
    Returns:
        str: Base64 encoded plot image
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create satisfaction count by company type
    if 'jenis_perusahaan' in df.columns and 'kepuasan' in df.columns:
        # Count satisfaction levels by company type
        satisfaction_data = df.groupby(['jenis_perusahaan', 'kepuasan']).size().unstack(fill_value=0)
        satisfaction_data.plot(kind='bar', ax=ax, color=['#e74c3c', '#f39c12', '#27ae60'], alpha=0.8)
    else:
        # Fallback if columns don't exist
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
    
    ax.set_xlabel('Jenis Perusahaan', fontsize=12)
    ax.set_ylabel('Jumlah Alumni', fontsize=12)
    ax.set_title('Kepuasan Kerja per Jenis Perusahaan', fontsize=14, fontweight='bold')
    ax.legend(title='Kepuasan', labels=['Tidak Puas', 'Puas', 'Sangat Puas'])
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_salary_distribution(df):
    """
    Generate histogram: Salary distribution by satisfaction
    
    Args:
        df: DataFrame with 'gaji', 'kepuasan' columns
        
    Returns:
        str: Base64 encoded plot image
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if 'gaji' not in df.columns or 'kepuasan' not in df.columns:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
        ax.set_title('Distribusi Gaji Berdasarkan Kepuasan', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plot_to_base64(fig)
    
    satisfaction_types = df['kepuasan'].unique()
    colors = {'Tidak puas': 'red', 'Kurang Puas': 'red', 'Puas': 'yellow', 'Sangat Puas': 'green'}
    
    for sat in satisfaction_types:
        if pd.notna(sat):
            data = df[df['kepuasan'] == sat]['gaji']
            if len(data) > 0:
                ax.hist(data, bins=15, alpha=0.5, label=sat, color=colors.get(sat, 'blue'))
    
    ax.set_xlabel('Gaji (IDR)', fontsize=12)
    ax.set_ylabel('Frekuensi', fontsize=12)
    ax.set_title('Distribusi Gaji Berdasarkan Kepuasan', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    return plot_to_base64(fig)


# def generate_correlation_heatmap(df):
#     """
#     Generate correlation heatmap (without nilai_rata for SMK)
#     
#     Args:
#         df: DataFrame with numeric columns
#         
#     Returns:
#         str: Base64 encoded plot image
#     """
#     fig, ax = plt.subplots(figsize=(10, 8))
#     # Removed 'nilai_rata' - SMK doesn't use GPA
#     numeric_cols = ['gaji', 'lama_kerja_1', 'lama_kerja_2', 'waktu_kerja_pertama']
#     
#     # Filter only existing columns
#     available_cols = [col for col in numeric_cols if col in df.columns]
#     numeric_data = df[available_cols].corr()
#     
#     sns.heatmap(numeric_data, annot=True, fmt='.2f', cmap='coolwarm', 
#                 center=0, square=True, ax=ax, cbar_kws={'label': 'Korelasi'})
#     ax.set_title('Matriks Korelasi Fitur Numerik', fontsize=14, fontweight='bold')
#     plt.tight_layout()
#     return plot_to_base64(fig)


def generate_experience_box(df):
    """
    Generate box plot: Experience distribution
    
    Args:
        df: DataFrame with 'lama_kerja_2', 'perusahaan_tepat' columns
        
    Returns:
        str: Base64 encoded plot image
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if 'lama_kerja_2' not in df.columns or 'perusahaan_tepat' not in df.columns:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
        ax.set_title('Distribusi Pengalaman Kerja', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plot_to_base64(fig)
    
    data_tepat = [df[df['perusahaan_tepat'] == 'Tepat']['lama_kerja_2'].astype(float).dropna(),
                  df[df['perusahaan_tepat'] == 'Tidak Tepat']['lama_kerja_2'].astype(float).dropna()]
    
    if len(data_tepat[0]) == 0 and len(data_tepat[1]) == 0:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
        ax.set_title('Distribusi Pengalaman Kerja', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plot_to_base64(fig)
    
    bp = ax.boxplot(data_tepat, labels=['Tepat', 'Tidak Tepat'], patch_artist=True)
    for patch, color in zip(bp['boxes'], ['lightgreen', 'lightcoral']):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Pengalaman Kerja (Tahun)', fontsize=12)
    ax.set_title('Distribusi Pengalaman Kerja', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_top_jurusan_bar(df):
    """
    Generate bar chart: Top 10 majors
    
    Args:
        df: DataFrame with 'jurusan_cocok' column
        
    Returns:
        str: Base64 encoded plot image
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if 'jurusan_cocok' not in df.columns:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
        ax.set_title('Top 10 Bidang Karir Paling Cocok', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plot_to_base64(fig)
    
    top_jurusan = df['jurusan_cocok'].value_counts().head(10)
    
    if len(top_jurusan) == 0:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
        ax.set_title('Top 10 Bidang Karir Paling Cocok', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plot_to_base64(fig)
    
    ax.barh(range(len(top_jurusan)), top_jurusan.values, color='steelblue')
    ax.set_yticks(range(len(top_jurusan)))
    ax.set_yticklabels(top_jurusan.index)
    ax.set_xlabel('Jumlah Rekomendasi', fontsize=12)
    ax.set_title('Top 10 Bidang Karir Paling Cocok', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_satisfaction_pie(df):
    """
    Generate pie chart: Satisfaction distribution
    
    Args:
        df: DataFrame with 'kepuasan' column
        
    Returns:
        str: Base64 encoded plot image
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    if 'kepuasan' not in df.columns:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
        ax.set_title('Distribusi Kepuasan Kerja', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plot_to_base64(fig)
    
    satisfaction_counts = df['kepuasan'].value_counts()
    
    if len(satisfaction_counts) == 0:
        ax.text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center', fontsize=14)
        ax.set_title('Distribusi Kepuasan Kerja', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plot_to_base64(fig)
    
    colors = {'Tidak puas': '#ff6666', 'Kurang Puas': '#ff9999', 'Puas': '#ffcc99', 'Sangat Puas': '#99ff99'}
    
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
    """
    Generate elbow curve plot for K-Means
    
    Args:
        clustering_data: Dict with 'inertias', 'optimal_k' keys
        
    Returns:
        str: Base64 encoded plot image
    """
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
    """
    Generate cluster scatter plot for K-Means
    
    Args:
        clustering_data: Dict with 'X_clustering_original', 'cluster_labels', 'cluster_centers' keys
        
    Returns:
        str: Base64 encoded plot image
    """
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
            ax.text(0.5, 0.5, 'Data tidak cukup untuk visualisasi 2D', 
                   ha='center', va='center', fontsize=14)
    else:
        ax.text(0.5, 0.5, 'Data clustering tidak tersedia', 
               ha='center', va='center', fontsize=14)
    
    plt.tight_layout()
    return plot_to_base64(fig)
