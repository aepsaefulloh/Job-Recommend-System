"""
DIAGRAM GENERATOR - Job Recommendation System
Tools untuk generate ERD, Activity Diagram, Sequence Diagram, dan UML
"""

import os
from pathlib import Path

class DiagramGenerator:
    """Generator untuk berbagai jenis diagram"""

    def __init__(self, output_dir="diagrams"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_erd_plantuml(self):
        """Generate ERD menggunakan PlantUML"""

        plantuml_code = """
@startuml Diagram ERD - Sistem Rekomendasi Pekerjaan

' Entitas
entity "DATA_SURVEY" as survey {
    + id : INT <<PK>>
    --
    email : VARCHAR(120) <<UK>>
    nama : VARCHAR(100)
    tempat_tinggal : VARCHAR(50)
    jurusan : VARCHAR(50)
    status_bekerja : VARCHAR(10)
    --
    profesi_sekarang : VARCHAR(100)
    tempat_kerja : VARCHAR(100)
    jenis_perusahaan : VARCHAR(50)
    gaji : FLOAT
    --
    jurusan_cocok : VARCHAR(50)
    perusahaan_tepat : VARCHAR(20)
    --
    created_at : DATETIME
    updated_at : DATETIME
}

entity "PENGGUNA" as users {
    + id : INT <<PK>>
    --
    username : VARCHAR(80) <<UK>>
    email : VARCHAR(120) <<UK>>
    password : VARCHAR(128)
    full_name : VARCHAR(100)
    role : VARCHAR(20)
    is_active : BOOLEAN
    --
    created_at : DATETIME
    last_login : DATETIME
}

entity "STATISTIK_DASHBOARD" as stats {
    + id : INT <<PK>>
    --
    nama_statistik : VARCHAR(50) <<UK>>
    nilai_statistik : FLOAT
    tipe_statistik : VARCHAR(20)
    --
    updated_at : DATETIME
}

' Relasi
survey ||..o{ users : "dimiliki oleh"
stats ||..o{ survey : "dihitung dari"
users ||..o{ stats : "akses admin"

' Legenda
legend right
    |= Simbol |= Arti |
    | PK | Primary Key |
    | UK | Unique Key |
    | FK | Foreign Key |
endlegend

@enduml
"""

        output_file = self.output_dir / "erd_diagram.puml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)

        print(f"✅ ERD PlantUML generated: {output_file}")
        return output_file

    def generate_activity_diagram_plantuml(self):
        """Generate Activity Diagram menggunakan PlantUML"""

        plantuml_code = """
@startuml Diagram Aktivitas - Alur Survey Pengguna

start

:Pengguna mengakses halaman utama;

:Tampilkan formulir survey;

:Pengguna mengisi Bagian 1;
note right: Informasi dasar (nama, email, jurusan, dll)

if (Status bekerja?) then (Ya)
    :Pengguna mengisi Bagian 2;
    note right: Data pekerjaan
else (Tidak)
    :Pengguna mengisi Bagian 3;
    note right: Data pengangguran
endif

:Kirim formulir;

:Validasi data input;

if (Valid?) then (Ya)
    :Pra-pemrosesan data formulir;
    :Encode fitur kategorikal;
    :Skalakan fitur numerik;

    :Muat model ML;
    :Buat prediksi;
    note right
        - Jurusan cocok (8 kategori)
        - Perusahaan tepat (2 kategori)
    end note

    :Generate rekomendasi;
    :Tampilkan halaman hasil;

    if (Simpan ke database?) then (Ya)
        :Simpan data survey;
        :Update statistik dashboard;
    endif

    :Tampilkan rekomendasi akhir;
    stop

else (Tidak)
    :Tampilkan error validasi;
    :Kembali ke formulir;
    stop
endif

@enduml
"""

        output_file = self.output_dir / "activity_diagram.puml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)

        print(f"✅ Activity Diagram PlantUML generated: {output_file}")
        return output_file

    def generate_sequence_diagram_plantuml(self):
        """Generate Sequence Diagram menggunakan PlantUML"""

        plantuml_code = """
@startuml Diagram Sekuens - Survey & Prediksi

actor "Alumni SMK" as User
participant "Aplikasi Flask" as Flask
participant "predictor.py" as Predictor
participant "Model ML" as ML
participant "Database" as DB
participant "Halaman Hasil" as Result

== Pengiriman Survey ==
User -> Flask: GET / (halaman utama)
Flask --> User: formulir survey

User -> Flask: POST /result (kirim survey)
Flask -> Predictor: preprocess_form_data(form_data)

Predictor -> Predictor: encode_features()
Predictor -> ML: Muat model & scaler
ML --> Predictor: Model dimuat

Predictor -> ML: make_predictions()
ML --> Predictor: hasil prediksi

Predictor --> Flask: hasil prediksi

Flask -> DB: Simpan survey (opsional)
DB --> Flask: Data tersimpan

Flask -> Result: Render result.html
Result --> User: Tampilkan rekomendasi

== Dashboard Admin ==
actor "Administrator" as Admin
Admin -> Flask: GET /login
Flask --> Admin: formulir login

Admin -> Flask: POST /login
Flask -> DB: validasi kredensial
DB --> Flask: pengguna terautentikasi

Flask --> Admin: redirect ke /dashboard
Admin -> Flask: GET /dashboard
Flask -> DB: query survey_data & stats
DB --> Flask: data dashboard
Flask --> Admin: dashboard dengan grafik

@enduml
"""

        output_file = self.output_dir / "sequence_diagram.puml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)

        print(f"✅ Sequence Diagram PlantUML generated: {output_file}")
        return output_file

    def generate_uml_class_diagram_plantuml(self):
        """Generate UML Class Diagram menggunakan PlantUML"""

        plantuml_code = """
@startuml Diagram Kelas UML - Sistem Rekomendasi Pekerjaan

class DataSurvey {
    - id: int
    - email: string
    - nama: string
    - tempat_tinggal: string
    - jurusan: string
    - status_bekerja: string
    --
    - profesi_sekarang: string
    - jenis_perusahaan: string
    - gaji: float
    --
    - jurusan_cocok: string
    - perusahaan_tepat: string
    --
    - created_at: datetime
    - updated_at: datetime
    --
    + simpan(): void
    + update(): void
    + hapus(): void
    + dapatkan_rekomendasi(): list
}

class Pengguna {
    - id: int
    - username: string
    - email: string
    - password: string
    - full_name: string
    - role: string
    - is_active: boolean
    --
    - created_at: datetime
    - last_login: datetime
    --
    + set_password(password: string): void
    + check_password(password: string): boolean
    + login(): boolean
    + logout(): void
}

class StatistikDashboard {
    - id: int
    - nama_statistik: string
    - nilai_statistik: float
    - tipe_statistik: string
    - updated_at: datetime
    --
    + update(): void
    + hitung(): float
    + dapatkan_nilai(): float
}

class Prediktor {
    - knn_jurusan: KNeighborsClassifier
    - knn_perusahaan: KNeighborsClassifier
    - scaler: StandardScaler
    - label_encoders: dict
    --
    + preprocess_form_data(form_data: dict): dict
    + encode_features(data: dict): array
    + make_predictions(data: dict): dict
    + load_models(): boolean
}

class ModelKNN {
    - n_neighbors: int
    - weights: string
    - metric: string
    --
    + fit(X, y): void
    + predict(X): array
    + predict_proba(X): array
}

' Relasi
DataSurvey "1" -- "*" Pengguna : dimiliki oleh
StatistikDashboard "*" -- "1" DataSurvey : dihitung dari
Prediktor --> DataSurvey : menggunakan
Prediktor --> ModelKNN : berisi
Pengguna --> StatistikDashboard : akses admin

' Interface
interface "ModelML" {
    + fit(X, y): void
    + predict(X): array
}

ModelKNN ..|> ModelML : mengimplementasi

@enduml
"""

        output_file = self.output_dir / "uml_class_diagram.puml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)

        print(f"✅ UML Class Diagram PlantUML generated: {output_file}")
        return output_file

    def generate_use_case_diagram_plantuml(self):
        """Generate Use Case Diagram menggunakan PlantUML"""

        plantuml_code = """
@startuml Diagram Use Case - Sistem Rekomendasi Pekerjaan

left to right direction

actor "Alumni SMK" as Alumni
actor "Administrator" as Admin

rectangle "Sistem Rekomendasi Pekerjaan" {
    usecase "UC-001: Mengisi Survey Pekerjaan" as UC1
    usecase "UC-002: Melihat Hasil Rekomendasi" as UC2
    usecase "UC-003: Login ke Dashboard" as UC3
    usecase "UC-004: Melihat Analitik Dashboard" as UC4
    usecase "UC-005: Filter Data Survey" as UC5
    usecase "UC-006: Export Data" as UC6
}

' Use case Alumni
Alumni --> UC1
Alumni --> UC2

' Use case Admin
Admin --> UC3
Admin --> UC4
Admin --> UC5
Admin --> UC6

' Relasi Include
UC1 ..> UC2 : <<include>>

' Relasi Extend
UC4 ..> UC5 : <<extend>>
UC4 ..> UC6 : <<extend>>

' Generalisasi
Admin --|> Alumni : mewarisi

note right of UC1
    **Prasyarat:**
    Pengguna belum login

    **Pasca-kondisi:**
    Mendapat rekomendasi
    pekerjaan
end note

note right of UC4
    **Prasyarat:**
    Admin sudah login

    **Pasca-kondisi:**
    Menampilkan statistik
    & grafik
end note

@enduml
"""

        output_file = self.output_dir / "use_case_diagram.puml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)

        print(f"✅ Use Case Diagram PlantUML generated: {output_file}")
        return output_file

    def generate_all_diagrams(self):
        """Generate semua diagram"""
        print("🚀 Membuat semua diagram...")

        self.generate_erd_plantuml()
        self.generate_activity_diagram_plantuml()
        self.generate_sequence_diagram_plantuml()
        self.generate_uml_class_diagram_plantuml()
        self.generate_use_case_diagram_plantuml()

        print(f"\n✅ Semua diagram dibuat di: {self.output_dir}/")
        print("\n📋 File yang dibuat:")
        for file in self.output_dir.glob("*.puml"):
            print(f"   - {file.name}")

        print("\n🔧 Untuk convert PlantUML ke gambar:")
        print("   1. Install PlantUML: https://plantuml.com/download")
        print("   2. Jalankan: plantuml *.puml")
        print("\n🌐 Alternatif: Gunakan editor PlantUML online")
        print("   https://www.plantuml.com/plantuml/uml/")

    def create_online_tools_guide(self):
        """Create guide for online diagram tools dalam bahasa Indonesia"""

        guide_content = """
# 🛠️ TOOLS ONLINE UNTUK GENERATE DIAGRAM

## 1. PlantUML Online Editor
**URL:** https://www.plantuml.com/plantuml/uml/
**Keunggulan:** Gratis, support semua jenis diagram
**Cara pakai:**
1. Copy kode PlantUML dari file .puml
2. Paste ke editor online
3. Download sebagai PNG/SVG

## 2. Draw.io (diagrams.net)
**URL:** https://app.diagrams.net/
**Keunggulan:** User-friendly, drag & drop
**Templates:** ERD, UML, Flowchart

## 3. Lucidchart
**URL:** https://www.lucidchart.com/
**Keunggulan:** Professional, collaboration
**Templates:** Lengkap untuk UML & ERD

## 4. Mermaid Live Editor
**URL:** https://mermaid.live/
**Keunggulan:** Text-based, simple syntax
**Support:** Flowchart, Sequence, Gantt

## 5. ERDPlus
**URL:** https://erdplus.com/
**Keunggulan:** Specialized for ERD
**Features:** Auto-generate SQL dari diagram

## 6. AI Tools untuk Diagram

### ChatGPT + DALL-E
```
Prompt: "Buat diagram ERD yang menunjukkan relasi antara tabel Users, Survey_Data, dan Dashboard_Stats dengan kardinalitas yang tepat"
```

### Claude Artifacts
- Support real-time diagram editing
- Generate PlantUML code automatically

### Gemini
- Can generate ASCII diagrams
- Support Mermaid syntax

## 📋 CONVERSION TOOLS

### PlantUML to Images
```bash
# Install Java & PlantUML
sudo apt install plantuml

# Convert semua file .puml
plantuml *.puml

# Convert file tertentu
plantuml erd_diagram.puml
```

### Python Libraries
```python
# Install graphviz
pip install graphviz

# Install plantuml
pip install plantuml

# Usage
import graphviz
dot = graphviz.Digraph()
# Create diagram secara programmatic
```

### VS Code Extensions
- PlantUML extension
- Draw.io extension
- Mermaid preview

## 🎯 WORKFLOW YANG DIREKOMENDASIKAN

1. **Gunakan PlantUML** untuk diagram teknis (ERD, UML)
2. **Gunakan Draw.io** untuk diagram business (Activity, Use Case)
3. **Gunakan Mermaid** untuk simple flowcharts
4. **Gunakan AI tools** untuk quick drafts

## 📁 FORMAT OUTPUT

- **PNG/JPG:** Untuk presentasi
- **SVG:** Untuk web (scalable)
- **PDF:** Untuk dokumen formal
- **PlantUML/Mermaid:** Untuk version control
"""

        guide_file = self.output_dir / "panduan_tools_online.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)

        print(f"✅ Panduan tools online dibuat: {guide_file}")

def main():
    """Main function"""
    print("="*60)
    print("GENERATOR DIAGRAM - SISTEM REKOMENDASI PEKERJAAN")
    print("="*60)

    generator = DiagramGenerator()

    # Generate all diagrams
    generator.generate_all_diagrams()

    # Create tools guide
    generator.create_online_tools_guide()

    print("\n" + "="*60)
    print("✅ PEMBUATAN DIAGRAM SELESAI!")
    print("="*60)

if __name__ == "__main__":
    main()