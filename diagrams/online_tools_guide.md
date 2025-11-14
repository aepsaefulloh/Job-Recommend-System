
# 🛠️ ONLINE TOOLS UNTUK GENERATE DIAGRAM

## 1. PlantUML Online Editor
**URL:** https://www.plantuml.com/plantuml/uml/
**Keunggulan:** Gratis, support semua jenis diagram
**Cara pakai:**
1. Copy PlantUML code dari file .puml
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
Prompt: "Create an ERD diagram showing relationships between Users, Survey_Data, and Dashboard_Stats tables with proper cardinalities"
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

# Convert all .puml files
plantuml *.puml

# Convert specific file
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
# Create diagram programmatically
```

### VS Code Extensions
- PlantUML extension
- Draw.io extension
- Mermaid preview

## 🎯 RECOMMENDED WORKFLOW

1. **Use PlantUML** untuk diagram teknis (ERD, UML)
2. **Use Draw.io** untuk diagram business (Activity, Use Case)
3. **Use Mermaid** untuk simple flowcharts
4. **Use AI tools** untuk quick drafts

## 📁 OUTPUT FORMATS

- **PNG/JPG:** Untuk presentasi
- **SVG:** Untuk web (scalable)
- **PDF:** Untuk dokumen formal
- **PlantUML/Mermaid:** Untuk version control
