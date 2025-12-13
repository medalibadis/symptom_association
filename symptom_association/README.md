# Healthcare Symptom Association Discovery

## Project Overview
Complete unsupervised learning system using **Association Rule Mining (Apriori Algorithm)** to discover symptom patterns and disease associations.

## Features
- 🔍 Symptom co-occurrence discovery
- 📊 Association rule mining (support, confidence, lift)
- 📈 Network visualization of symptom relationships
- 📱 Flutter mobile app for symptom checking
- 💾 Model export for deployment

## Project Structure
```
symptom_association/
├── kaggle_notebook.ipynb        # Complete Kaggle notebook
├── symptom_analysis.py          # Standalone Python script
├── data_generator.py            # Synthetic data generator
├── requirements.txt             # Python dependencies
├── models/
│   └── association_rules.json   # Exported rules
├── visualizations/              # Generated charts
└── flutter_app/                 # Mobile application
    └── symptom_checker/
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Analysis
```bash
# Generate synthetic data and run analysis
python symptom_analysis.py

# Or use Kaggle notebook
# Upload kaggle_notebook.ipynb to Kaggle
```

### 3. Launch Mobile App
```bash
cd flutter_app/symptom_checker
flutter run
```

## Datasets
**Recommended Kaggle Datasets:**
1. Disease-Symptom Dataset (773 diseases, 377 symptoms)
2. Disease and Symptoms dataset (800+ diseases)
3. Symptom-Based Disease Prediction Dataset

**Or use included synthetic data generator**

## Technologies
- **ML**: mlxtend (Apriori), pandas, numpy
- **Visualization**: matplotlib, seaborn, networkx, plotly
- **Mobile**: Flutter, Dart
- **Export**: JSON for cross-platform compatibility

## Documentation
- `README.md` - This file
- `KAGGLE_GUIDE.md` - How to run on Kaggle
- `FLUTTER_GUIDE.md` - Mobile app setup
- `API_DOCUMENTATION.md` - Model format specification
