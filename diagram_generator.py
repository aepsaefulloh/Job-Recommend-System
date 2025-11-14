"""
DIAGRAM GENERATOR - Job Recommendation System
Tools untuk generate ERD, Activity Diagram, Sequence Diagram, dan UML
"""

import os
import subprocess
from pathlib import Path

class DiagramGenerator:
    """Generator untuk berbagai jenis diagram"""

    def __init__(self, output_dir="diagrams"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_erd_plantuml(self):
        """Generate ERD using PlantUML with standard English terminology"""

        plantuml_code = """
@startuml ERD - Job Recommendation System

' Entities
entity "SURVEY_DATA" as survey {
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

entity "USERS" as users {
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

entity "DASHBOARD_STATS" as stats {
    + id : INT <<PK>>
    --
    stat_name : VARCHAR(50) <<UK>>
    stat_value : FLOAT
    stat_type : VARCHAR(20)
    --
    updated_at : DATETIME
}

' Relationships
survey ||..o{ users : "owned by"
stats ||..o{ survey : "calculated from"
users ||..o{ stats : "admin access"

' Legend
legend right
    |= Symbol |= Meaning |
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
        """Generate Activity Diagram using PlantUML with standard English terminology"""

        plantuml_code = """
@startuml Activity Diagram - User Survey Flow

start

:User accesses homepage;

:Display survey form;

:User fills Section 1;
note right: Basic information (name, email, major, etc)

if (Currently Working?) then (Yes)
    :User fills Section 2;
    note right: Employment data
else (No)
    :User fills Section 3;
    note right: Unemployment data
endif

:Submit form;

:Validate input data;

if (Valid?) then (Yes)
    :Preprocess form data;
    :Encode categorical features;
    :Scale numerical features;

    :Load ML model;
    :Make predictions;
    note right
        - Suitable major (8 categories)
        - Company type (2 categories)
    end note

    :Generate recommendations;
    :Display result page;

    if (Save to database?) then (Yes)
        :Save survey data;
        :Update dashboard statistics;
    endif

    :Show final recommendations;
    stop

else (No)
    :Display validation errors;
    :Return to form;
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
        """Generate Sequence Diagram using PlantUML with standard English terminology"""

        plantuml_code = """
@startuml Sequence Diagram - Survey & Prediction

actor "SMK Alumni" as User
participant "Flask App" as Flask
participant "predictor.py" as Predictor
participant "ML Model" as ML
participant "Database" as DB
participant "Result Page" as Result

== Survey Submission ==
User -> Flask: GET / (homepage)
Flask --> User: survey form

User -> Flask: POST /result (submit survey)
Flask -> Predictor: preprocess_form_data(form_data)

Predictor -> Predictor: encode_features()
Predictor -> ML: Load model & scaler
ML --> Predictor: Model loaded

Predictor -> ML: make_predictions()
ML --> Predictor: prediction results

Predictor --> Flask: prediction results

Flask -> DB: Save survey (optional)
DB --> Flask: Data saved

Flask -> Result: Render result.html
Result --> User: Display recommendations

== Admin Dashboard ==
actor "Administrator" as Admin
Admin -> Flask: GET /login
Flask --> Admin: login form

Admin -> Flask: POST /login
Flask -> DB: validate credentials
DB --> Flask: user authenticated

Flask --> Admin: redirect to /dashboard
Admin -> Flask: GET /dashboard
Flask -> DB: query survey_data & stats
DB --> Flask: dashboard data
Flask --> Admin: dashboard with charts

@enduml
"""

        output_file = self.output_dir / "sequence_diagram.puml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)

        print(f"✅ Sequence Diagram PlantUML generated: {output_file}")
        return output_file

    def generate_uml_class_diagram_plantuml(self):
        """Generate UML Class Diagram using PlantUML with standard English terminology"""

        plantuml_code = """
@startuml UML Class Diagram - Job Recommendation System

class SurveyData {
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
    + save(): void
    + update(): void
    + delete(): void
    + get_recommendations(): list
}

class User {
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

class DashboardStats {
    - id: int
    - stat_name: string
    - stat_value: float
    - stat_type: string
    - updated_at: datetime
    --
    + update(): void
    + calculate(): float
    + get_value(): float
}

class Predictor {
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

class KNNModel {
    - n_neighbors: int
    - weights: string
    - metric: string
    --
    + fit(X, y): void
    + predict(X): array
    + predict_proba(X): array
}

' Relationships
SurveyData "1" -- "*" User : owned by
DashboardStats "*" -- "1" SurveyData : calculated from
Predictor --> SurveyData : uses
Predictor --> KNNModel : contains
User --> DashboardStats : admin access

' Interface
interface "MLModel" {
    + fit(X, y): void
    + predict(X): array
}

KNNModel ..|> MLModel : implements

@enduml
"""

        output_file = self.output_dir / "uml_class_diagram.puml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)

        print(f"✅ UML Class Diagram PlantUML generated: {output_file}")
        return output_file

    def generate_use_case_diagram_plantuml(self):
        """Generate Use Case Diagram using PlantUML with standard English terminology"""

        plantuml_code = """
@startuml Use Case Diagram - Job Recommendation System

left to right direction

actor "SMK Alumni" as Alumni
actor "Administrator" as Admin

rectangle "Job Recommendation System" {
    usecase "UC-001: Fill Job Survey" as UC1
    usecase "UC-002: View Recommendations" as UC2
    usecase "UC-003: Login to Dashboard" as UC3
    usecase "UC-004: View Dashboard Analytics" as UC4
    usecase "UC-005: Filter Survey Data" as UC5
    usecase "UC-006: Export Data" as UC6
}

' Alumni use cases
Alumni --> UC1
Alumni --> UC2

' Admin use cases
Admin --> UC3
Admin --> UC4
Admin --> UC5
Admin --> UC6

' Include relationships
UC1 ..> UC2 : <<include>>

' Extend relationships
UC4 ..> UC5 : <<extend>>
UC4 ..> UC6 : <<extend>>

' Generalization
Admin --|> Alumni : inherits

note right of UC1
    **Precondition:**
    User not logged in

    **Postcondition:**
    Receives job
    recommendations
end note

note right of UC4
    **Precondition:**
    Admin logged in

    **Postcondition:**
    Display statistics
    & charts
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