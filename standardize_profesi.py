"""
Script untuk standardisasi profesi di dataset CSV
Mengubah format profesi lama ke format profesional baru
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Mapping profesi lama ke profesi baru (standar profesional)
PROFESI_MAPPING = {
    # Administrasi & Perkantoran
    'Staff Administrasi': 'Staff Administrasi',
    'Sekretaris': 'Sekretaris',
    'Data Entry': 'Data Entry Clerk',
    'Receptionist': 'Resepsionis',
    
    # Customer Service
    'Customer Service': 'Customer Service Representative',
    
    # Marketing & Sales
    'Marketing Staff': 'Marketing Staff',
    'Digital Marketing': 'Digital Marketing Specialist',
    'Sales Executive': 'Sales Executive',
    'Brand Ambassador': 'Brand Ambassador',
    
    # Keuangan & Akuntansi
    'Akuntan': 'Akuntan',
    'Finance Staff': 'Staff Keuangan',
    'Staff Accounting': 'Accounting Staff',
    'Tax Consultant': 'Tax Staff',
    'Auditor': 'Auditor',
    'Kasir': 'Kasir',
    
    # Lainnya
    'N/A': 'N/A',
}

def standardize_profesi(profesi_value):
    """
    Standardisasi nilai profesi
    
    Args:
        profesi_value: Nilai profesi dari dataset
        
    Returns:
        str: Profesi yang sudah distandarisasi
    """
    if pd.isna(profesi_value) or profesi_value == 'N/A':
        return 'N/A'
    
    # Cek apakah ada mapping langsung
    if profesi_value in PROFESI_MAPPING:
        return PROFESI_MAPPING[profesi_value]
    
    # Jika tidak ada mapping, kembalikan nilai asli
    return profesi_value

def main():
    """Main function untuk standardisasi profesi"""
    
    print("\n" + "="*70)
    print("STANDARDISASI PROFESI DATASET")
    print("="*70)
    
    # 1. Load dataset
    print("\n1. Loading dataset...")
    try:
        df = pd.read_csv('job_survey.csv')
        print(f"   ✓ Dataset loaded: {len(df)} records")
    except Exception as e:
        print(f"   ✗ Error loading dataset: {e}")
        return
    
    # 2. Backup dataset asli
    backup_filename = f"job_survey_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    print(f"\n2. Creating backup: {backup_filename}...")
    try:
        df.to_csv(backup_filename, index=False)
        print(f"   ✓ Backup created successfully")
    except Exception as e:
        print(f"   ✗ Error creating backup: {e}")
        return
    
    # 3. Analisis profesi saat ini
    print("\n3. Analyzing current professions...")
    profesi_counts = df[df['status_bekerja'] == 'Ya']['profesi_sekarang'].value_counts()
    print(f"   Total unique professions: {len(profesi_counts)}")
    print("\n   Current professions:")
    for profesi, count in profesi_counts.items():
        print(f"   - {profesi}: {count} records")
    
    # 4. Standardisasi profesi
    print("\n4. Standardizing professions...")
    df['profesi_sekarang'] = df['profesi_sekarang'].apply(standardize_profesi)
    print(f"   ✓ Professions standardized")
    
    # 5. Analisis profesi setelah standardisasi
    print("\n5. Analyzing standardized professions...")
    profesi_counts_new = df[df['status_bekerja'] == 'Ya']['profesi_sekarang'].value_counts()
    print(f"   Total unique professions: {len(profesi_counts_new)}")
    print("\n   Standardized professions:")
    for profesi, count in profesi_counts_new.items():
        print(f"   - {profesi}: {count} records")
    
    # 6. Save dataset yang sudah distandarisasi
    print("\n6. Saving standardized dataset...")
    try:
        df.to_csv('job_survey.csv', index=False)
        print(f"   ✓ Dataset saved successfully")
    except Exception as e:
        print(f"   ✗ Error saving dataset: {e}")
        return
    
    # 7. Summary
    print("\n" + "="*70)
    print("✅ STANDARDIZATION COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"\n📊 Summary:")
    print(f"   - Total records: {len(df)}")
    print(f"   - Employed records: {len(df[df['status_bekerja'] == 'Ya'])}")
    print(f"   - Unique professions (before): {len(profesi_counts)}")
    print(f"   - Unique professions (after): {len(profesi_counts_new)}")
    print(f"\n💾 Files:")
    print(f"   - Backup: {backup_filename}")
    print(f"   - Updated: job_survey.csv")
    print("\n⚠️  NEXT STEPS:")
    print("   1. Run preprocessing.py to retrain models with standardized data")
    print("   2. Test the application with new profession values")
    print("   3. Update database records if needed (run setup_database.py)")
    print("\n")

if __name__ == '__main__':
    main()
