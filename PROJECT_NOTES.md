# Job Recommendation System - Project Notes for AI Agent

## 📋 Project Overview
**Project Name:** Job Recommendation System (JRC)  
**Type:** Flask Web Application with Machine Learning  
**Algorithm:** K-Nearest Neighbors (KNN) - Optimized  
**Language:** Python, HTML, CSS  
**Repository:** Job-Requirement-System (Owner: aepsaefulloh)  
**Branch:** main

**Current Performance:**
- 📊 Dataset: **2,303 training samples** (3,000 total generated)
- 🎯 Jurusan Model: **50.76% accuracy** (K=11, distance-weighted)
- 🏢 Perusahaan Model: **72.89% accuracy** (K=15, distance-weighted)
- 📚 Classes: **8 jurusan categories** (optimized from 13)

---

## 🎨 Design System

### Color Scheme (Modern Emerald Green Theme)
- **Primary Color:** `#10b981` (Emerald Green)
- **Accent Color:** `#059669` (Dark Emerald)
- **Background Gradient:** `linear-gradient(135deg, #10b981 0%, #059669 100%)`
- **Success/Positive:** `#dcfce7` (Light Green Background)
- **Error/Negative:** `#fee2e2` (Light Red Background)
- **Text Primary:** `#374151`, `#333`
- **Text Secondary:** `#666`, `#888`
- **Border:** `#e0e0e0`

### Previous Color Scheme (Replaced)
- OLD: Purple `#667eea`, `#764ba2` → NEW: Emerald `#10b981`, `#059669`

---

## 📁 Project Structure

```
job recommended system/
├── app.py                          # Main Flask application
├── app_backup.py                   # Backup of original app
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── form.txt                        # Form field reference
├── job_survey.csv                  # Dataset (3,000 samples, 2,303 employed)
├── generate_smk_dataset.py         # Dataset generator
├── preprocessing.py                # Data preprocessing
├── __pycache__/                    # Python cache
├── static/
│   └── css/                        # External CSS files (NEW)
│       ├── index.css               # Home/Survey page (240 lines)
│       ├── metrics.css             # Metrics dashboard (400+ lines)
│       ├── visualize.css           # Visualizations page (310 lines)
│       ├── result.css              # Results page (300 lines)
│       └── clustering.css          # Clustering analysis (340 lines)
├── templates/
│   ├── index.html                  # Survey form page
│   ├── index_old.html              # Old version backup
│   ├── metrics.html                # Model performance metrics
│   ├── visualize.html              # Data visualizations (8 charts)
│   ├── result.html                 # Recommendation results
│   └── clustering.html             # K-Means clustering analysis
└── utils/
    ├── __init__.py
    ├── model_loader.py             # Load ML models
    ├── predictor.py                # Prediction logic
    ├── visualization.py            # Chart generation
    └── __pycache__/
```

---

## 🚀 Application Routes

### 1. **Home/Survey Page** (`/` - GET)
- **File:** `templates/index.html`
- **CSS:** `static/css/index.css`
- **Purpose:** User survey form for job recommendations
- **Form Fields:**
  - Personal: Email, Name, City, Major, Status
  - Professional: Profession, Workplace, Ease of Work, Support, Alignment
  - Additional: Work Time, Company Type, Major Alignment, Satisfaction
  - Career: Career Change, Work Duration, Comfort, Salary

### 2. **Metrics Dashboard** (`/metrics` - GET)
- **File:** `templates/metrics.html`
- **CSS:** `static/css/metrics.css`
- **Purpose:** Display model performance metrics
- **Features:**
  - Model Jurusan Accuracy: ~17.57%
  - Model Perusahaan Accuracy: ~79.73%
  - Algorithm: KNN (K=5)
  - Dataset: 198 samples
  - Confusion Matrix for Perusahaan model
  - Improvement suggestions for Jurusan model
  - Model Information cards

### 3. **Visualizations** (`/visualize` - GET)
- **File:** `templates/visualize.html`
- **CSS:** `static/css/visualize.css`
- **Purpose:** Display 8 data visualization charts
- **Charts:**
  1. Scatter plot
  2. Bar charts
  3. Heatmaps
  4. Pie chart
  5. Distribution plots
  6. Correlation matrix
  7. Feature importance
  8. Trend analysis

### 4. **Clustering Analysis** (`/clustering` - GET)
- **File:** `templates/clustering.html`
- **CSS:** `static/css/clustering.css`
- **Purpose:** K-Means clustering analysis
- **Features:**
  - Algorithm: K-Means
  - Optimal Clusters: 3
  - Features Used: 3
  - Dataset Size: 198
  - Cluster interpretation cards
  - Stat cards with emerald theme

### 5. **Results Page** (`/result` - POST)
- **File:** `templates/result.html`
- **CSS:** `static/css/result.css`
- **Purpose:** Display job recommendations
- **Features:**
  - User profile display
  - Job recommendation cards
  - Similar jobs listing
  - Match score badges
- **Note:** Requires POST request from survey form

---

## 🎯 CSS Architecture

### Common Patterns Across All CSS Files

#### 1. **Reset & Base Styles**
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    padding: 20px;
    min-height: 100vh;
}
```

#### 2. **Container Pattern**
```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 10px 40px rgba(16, 185, 129, 0.3);
}
```

#### 3. **Header Pattern**
```css
.header {
    text-align: center;
    margin-bottom: 40px;
    border-bottom: 3px solid #10b981;
    padding-bottom: 20px;
}

.header h1 {
    color: #10b981;
    font-size: 28px;
}
```

#### 4. **Card Pattern**
```css
.card {
    background: #f8f9fa;
    padding: 30px;
    border-radius: 12px;
    border-left: 5px solid #10b981;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2);
}
```

#### 5. **Button Pattern**
```css
.btn-primary {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 12px 25px;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
```

#### 6. **Responsive Grid Pattern**
```css
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}

@media (max-width: 768px) {
    .grid {
        grid-template-columns: 1fr;
    }
}
```

---

## 🔧 Recent Major Changes

### Phase 1: CSS Separation (Completed)
**Date:** November 2025  
**Changes:**
- Separated all inline `<style>` blocks from HTML files
- Created 5 external CSS files in `static/css/` directory
- Updated all HTML templates to use `{{ url_for('static', filename='css/page.css') }}`
- Total: ~1,470 lines of CSS code extracted

### Phase 2: Color Theme Update (Completed)
**Changes:**
- Changed from purple (#667eea, #764ba2) to emerald green (#10b981, #059669)
- Updated all gradients, borders, buttons, focus states
- Applied consistent emerald theme across all pages

### Phase 3: Metrics Page Improvements (Completed)
**File:** `templates/metrics.html` & `static/css/metrics.css`

#### **3A: Model Jurusan Cocok Section**
**Before:** Plain text with bullet list  
**After:** Modern card-based layout with:
- **Analysis Stats Grid:**
  - 3 stat cards: Jumlah Kategori (22), Dataset Size (198), Accuracy (17.57%)
  - Hover effects with emerald shadow
  - Clean typography with stat-label, stat-value, stat-desc
  
- **Analysis Insight Box:**
  - Light green gradient background (#f0fdf4 → #dcfce7)
  - Left border accent (#10b981)
  - Clear explanation text
  
- **Improvement Suggestions Grid:**
  - 4 suggestion cards with icons (📈, 🎯, ⚙️, 🔧)
  - Each card: icon + title + description
  - Hover effects with border color change
  - Responsive: 4 columns → 1 column on mobile

#### **3B: Model Perusahaan Tepat Section**
**Before:** Basic HTML table with inline styling  
**After:** Modern confusion matrix design with:

**Confusion Matrix Table:**
```css
.confusion-matrix {
    border-collapse: separate;
    border-spacing: 0;
    min-width: 340px;
    background: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(16,185,129,0.08);
}
```

**Cell Styling:**
- Header cells: Emerald background (#10b981), white text
- True Positive cells: Light green (#dcfce7), emerald text (#059669)
- False cells: Light red (#fee2e2), red text (#be123c)
- Bold font, centered alignment, proper padding

**Matrix Interpretation:**
- 2 stat cards below table (True Positive & False)
- Light green background (#f0fdf4)
- Left border accent (#10b981)
- Flex layout (horizontal → vertical on mobile)

---

## 📱 Responsive Design

### Breakpoints
- **Desktop:** 1920px+ (full layout)
- **Tablet:** 768px (grid collapse, 2-column layouts)
- **Mobile:** 375px (single column, vertical stacking)

### Mobile Optimizations (All Pages)
```css
@media (max-width: 768px) {
    .container {
        padding: 20px;
    }
    
    .metrics-grid, .performance-grid, .charts-grid {
        grid-template-columns: 1fr;
    }
    
    .nav-links {
        flex-direction: column;
    }
    
    .confusion-matrix {
        min-width: 100%;
        font-size: 13px;
    }
    
    .matrix-interpretation {
        flex-direction: column;
        gap: 10px;
    }
    
    .analysis-stats {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .suggestion-grid {
        grid-template-columns: 1fr;
    }
}
```

---

## 🧪 Testing & Validation

### Visual Testing (Playwright)
**Status:** Completed (9 screenshots captured)

#### Desktop Testing (1920px)
✅ Home page - Full survey form  
✅ Metrics page - Dashboard with confusion matrix  
✅ Visualizations page - 8 charts displayed  
✅ Clustering page - K-Means analysis  

#### Tablet Testing (768px)
✅ Home page - Responsive grid collapse  

#### Mobile Testing (375px)
✅ Home page - Perfect vertical stacking  
✅ Metrics page - Single column layout  
✅ Visualizations page - Charts responsive  
✅ Clustering page - Mobile optimized  

### Compilation Testing
✅ Flask app runs successfully on `localhost:5000`  
✅ All CSS files loaded correctly  
✅ No syntax errors in HTML/CSS  
✅ Models and encoders loaded properly  

---

## 🐛 Known Issues

### Backend Issues (Not CSS-related)
~~1. **Result Page POST Error:**~~ ✅ **FIXED (Nov 13, 2025)**
   - ~~Error: "y contains previously unseen labels: 'Jakarta'"~~
   - ~~Issue: Label encoding doesn't handle new city values~~
   - ~~Location: Prediction logic in `app.py`~~
   - **Solution Applied:** Added `safe_encode()` function in `utils/predictor.py` that handles unseen labels by using default values
   - **Details:** See `BUGFIX_LABEL_ENCODER.md`

### CSS Issues
- None currently identified

---

## 💡 Improvement Suggestions

### For Model (Current Status: ✅ Already Applied)
1. ✅ **Data Training:** Increased to 2,303 samples (from 198)
2. ✅ **Kategori:** Reduced from 13 to 8 classes
3. ✅ **Feature Engineering:** Improved correlation between features
4. ✅ **Hyperparameter Tuning:** Auto-tested K=3,5,7,9,11,15

### For Future Enhancements
1. **Collect Real Data:** Replace synthetic with actual alumni survey data
2. **Try Other Algorithms:** Random Forest, SVM, Neural Networks
3. **Feature Selection:** Use feature importance analysis
4. **Cross-Validation:** Implement K-Fold validation for robust accuracy

### For UI/UX
1. Add loading animations for predictions
2. Add error handling UI for failed predictions
3. Add tooltips for technical terms
4. Consider adding dark mode option

### For Performance
1. Minify CSS files for production
2. Implement CSS caching strategies
3. Optimize chart rendering (consider Chart.js instead of matplotlib)
4. Add progressive loading for visualizations

---

## 🔑 Key CSS Classes Reference

### Layout Classes
- `.container` - Main content wrapper (max-width: 1200px)
- `.header` - Page header with title
- `.section` - Content section wrapper

### Card Classes
- `.metric-card` - Metric display card
- `.chart-container` - Chart wrapper
- `.stat-item` - Statistic item card
- `.suggestion-card` - Suggestion/recommendation card
- `.cluster-card` - Clustering result card

### Component Classes
- `.confusion-matrix` - Confusion matrix table
- `.matrix-cell` - Matrix data cell
- `.true-positive` - True positive cell styling
- `.false-value` - False value cell styling
- `.matrix-interpretation` - Matrix stats display
- `.jurusan-analysis` - Jurusan model analysis wrapper
- `.analysis-stats` - Statistics grid
- `.analysis-insight` - Insight box
- `.improvement-suggestions` - Suggestions container
- `.suggestion-grid` - Suggestions grid layout

### Button Classes
- `.btn-primary` - Emerald green button
- `.btn-secondary` - Gray button
- `.btn-info` - Blue button

### Navigation
- `.nav-links` - Navigation links container

---

## 🛠 Development Commands

### Run Application
```bash
cd "c:\xampp\htdocs\python\job recommended system"
python app.py
```

### Access URLs
- Home: `http://127.0.0.1:5000/`
- Metrics: `http://127.0.0.1:5000/metrics`
- Visualizations: `http://127.0.0.1:5000/visualize`
- Clustering: `http://127.0.0.1:5000/clustering`
- Results: `http://127.0.0.1:5000/result` (POST only)

### Testing with Playwright
```javascript
// Navigate
await page.goto('http://127.0.0.1:5000/metrics');

// Resize viewport
await page.setViewportSize({ width: 375, height: 812 });

// Screenshot
await page.screenshot({ fullPage: true, path: 'screenshot.png' });
```

---

## 📝 Important Notes for AI Agents

1. **Always maintain the emerald green color scheme** (#10b981, #059669)
2. **Keep CSS external** - Never add inline styles to HTML
3. **Maintain responsive design** - Test all changes at 375px, 768px, 1920px
4. **Follow existing patterns** - Use established card, button, grid patterns
5. **Use Flask url_for()** - Always use `{{ url_for('static', filename='css/file.css') }}`
6. **Test changes** - Run Flask app and verify visually before completing
7. **Preserve functionality** - Don't break Jinja2 template variables or Flask routing
8. **Document changes** - Update this file when making significant modifications

---

## 📋 Future Development

Untuk roadmap pengembangan lengkap dan improvement checklist, lihat: **`IMPROVEMENT.md`**

---

## 🎨 Design System (v2.3 - Modern Neutral Theme)

### Color Palette
**Primary Colors:**
- Primary Blue: `#3b82f6` (Blue 500)
- Secondary Blue: `#2563eb` (Blue 600)

**Neutral Palette:**
- Background: `#f8fafc` → `#e2e8f0` (Gradient)
- Text Primary: `#1e293b` (Slate 800)
- Text Secondary: `#475569` (Slate 600)
- Text Muted: `#64748b` (Slate 500)
- Borders: `#e2e8f0` (Slate 200)

**Accent Colors:**
- Success: `#10b981` (Emerald 500)
- Warning: `#f59e0b` (Amber 500)
- Error: `#ef4444` (Red 500)
- Info: `#3b82f6` (Blue 500)

### Typography
- Font Family: `'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif`
- Headings: 700 weight, Slate 800
- Body: 500 weight, Slate 600
- Small Text: 500 weight, Slate 500

### Components

**Cards:**
- Background: White with soft gradient
- Border: 1px solid Slate 200
- Border Radius: 12px
- Shadow: `0 2px 8px rgba(0,0,0,0.04)`
- Hover: `0 4px 16px rgba(59,130,246,0.08)` + translateY(-2px)

**Buttons:**
- Primary: Blue gradient (#3b82f6 → #2563eb)
- Secondary: Slate 100 background, Slate 600 text
- Padding: 12-16px vertical, 24-32px horizontal
- Border Radius: 8-10px
- Shadow: Soft 0 2px 8px

**Form Inputs:**
- Border: 1.5px solid Slate 300
- Focus: Blue 500 border + soft shadow
- Padding: 12-14px
- Border Radius: 8px

**Data Cards:**
- Gradient backgrounds (50 → 100 shades)
- Border-left accent (4px solid primary)
- Subtle shadows
- Smooth transitions (0.2s ease)

### Design Principles
1. **Soft & Professional**: Tidak mencolok, nyaman di mata
2. **Clear Hierarchy**: Visual hierarchy yang jelas
3. **Consistent Spacing**: 16px base unit
4. **Subtle Shadows**: Depth tanpa terlalu 3D
5. **Smooth Transitions**: 0.2s ease untuk interaksi

---

## 📚 Dependencies

### Python Packages (requirements.txt)
- Flask (1.0+)
- scikit-learn (KNN implementation)
- pandas (data processing)
- numpy (numerical operations)
- matplotlib (chart generation)
- Other dependencies as listed in requirements.txt

### Frontend
- No external CSS frameworks (custom CSS only)
- No JavaScript libraries (vanilla JS if needed)
- Font: Segoe UI (system font)

---

## 🎯 Current State Summary

**Status:** Production Ready ✅

**Completed:**
- ✅ CSS separation from HTML
- ✅ Emerald green theme implementation
- ✅ Responsive design (desktop, tablet, mobile)
- ✅ Metrics page improvements (both sections)
- ✅ Visual testing with Playwright
- ✅ Flask compilation testing

**In Progress:**
- None

**Pending:**
- Backend label encoding fix for Result page
- Optional UI enhancements (loading states, tooltips, dark mode)

---

## 📞 Contact & Repository

**Repository:** Job-Requirement-System  
**Owner:** aepsaefulloh  
**Branch:** main  
**Last Updated:** November 13, 2025  

---

## 🔄 Version History

### v2.3 (November 14, 2025) - Current ⭐
**UX/UI Enhancement - Modern Neutral Theme:**
- Complete redesign with soft neutral color palette
- Color Scheme: Emerald green → Modern blue-gray (#3b82f6, #1e293b, #f8fafc)
- Improved data presentation with better card layouts
- Enhanced visual hierarchy and readability
- Softer shadows and transitions (0.2s ease)
- Documented comprehensive design system
- Unified design across all pages (index, metrics, visualize, clustering, result)
- Better contrast and accessibility
- Professional and not too flashy appearance

**Files Modified:**
- `static/css/index.css`: Soft neutral backgrounds, blue accents
- `static/css/metrics.css`: Modern card gradients, better stat cards
- `static/css/visualize.css`: Enhanced chart containers, soft insight cards
- `static/css/clustering.css`: Refined cluster cards, soft tags
- `templates/result.html`: Tailwind config with neutral palette
- `PROJECT_NOTES.md`: Added Design System documentation

### v2.2 (November 13, 2025)
**Major Model Improvements:**
- Dataset: 198 → **2,303 samples** (+1,062%)
- Jurusan accuracy: 17.57% → **50.76%** (+188% improvement!)
- Classes optimized: 13 → 8 (reduced complexity)
- Hyperparameter tuning: Auto-tested K=3,5,7,9,11,15
- Best K values: **11** (Jurusan), **15** (Perusahaan)
- Distance-weighted KNN for better performance
- Fixed LabelEncoder error with `safe_encode()` function
- Improved error handling with user-friendly error pages

**Technical Details:**
- `generate_smk_dataset.py`: Generate 3,000 records with better feature correlation
- `preprocessing.py`: Added auto hyperparameter tuning loop
- `utils/predictor.py`: Safe encoding for unknown labels
- `templates/metrics.html`: Updated with new performance metrics

### v2.0 (November 2025)
- Separated CSS into external files
- Updated to emerald green theme
- Improved metrics page layout
- Added comprehensive responsive design

### v1.0 (Original)
- Inline CSS styling
- Purple/blue color scheme
- Basic Flask application with KNN model

---

**End of Project Notes**
