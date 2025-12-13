# Using Your Real Kaggle Dataset

## Your Dataset Files

You have 4 CSV files:
1. **dataset.csv** - Main disease-symptom data
2. **Symptom-severity.csv** - Symptom severity weights
3. **symptom_Description.csv** - Disease descriptions  
4. **symptom_precaution.csv** - Disease precautions

## Quick Setup

### Step 1: Place Dataset Files

Copy your 4 CSV files to the `data/` folder:

```bash
symptom_association/
└── data/
    ├── dataset.csv
    ├── Symptom-severity.csv
    ├── symptom_Description.csv
    └── symptom_precaution.csv
```

### Step 2: Test Data Loader

```bash
python real_data_loader.py
```

This will:
- Load all 4 CSV files
- Preprocess the data
- Create binary encoding
- Show sample data
- Save to `processed_medical_data.csv`

### Step 3: Run Analysis

```bash
python symptom_analysis_updated.py
```

This will:
- Automatically detect and use your real dataset
- Run Apriori algorithm
- Generate association rules
- Export to JSON for mobile app

## Expected Output

The script will show:
```
[OK] Loaded dataset.csv: (rows, columns)
[OK] Loaded Symptom-severity.csv: (rows, columns)
[OK] Loaded symptom_Description.csv: (rows, columns)
[OK] Loaded symptom_precaution.csv: (rows, columns)
[OK] Created binary matrix: (patients, symptoms)
[OK] Found X frequent itemsets
[OK] Generated Y association rules
```

## Dataset Format

Your `dataset.csv` typically has this structure:
```
Disease | Symptom_1 | Symptom_2 | ... | Symptom_17
--------|-----------|-----------|-----|------------
Flu     | fever     | cough     | ... | headache
Cold    | runny_nose| sneezing  | ... | 
```

The loader will:
1. Extract the disease column (first column)
2. Collect all symptoms from remaining columns
3. Create binary encoding (1 = symptom present, 0 = absent)
4. Remove duplicates and NaN values

## Troubleshooting

### "dataset.csv not found"
- Make sure files are in `data/` folder
- Check file names match exactly (case-sensitive)

### "No rules generated"
- Try lowering thresholds in `symptom_analysis_updated.py`:
  ```python
  MIN_SUPPORT = 0.03  # Lower from 0.05
  MIN_CONFIDENCE = 0.5  # Lower from 0.6
  ```

### Empty symptoms
- The loader automatically handles NaN and empty values
- Check that your dataset has symptom data

## Next Steps

After running the analysis:

1. **Check Results**:
   - `models/association_rules.json` - For mobile app
   - `models/association_rules.csv` - For Excel analysis

2. **Use in Flutter App**:
   ```bash
   copy models\association_rules.json flutter_app\assets\
   cd flutter_app
   flutter run
   ```

3. **Upload to Kaggle**:
   - Use `kaggle_notebook.ipynb`
   - Add your dataset as Kaggle input
   - Run all cells

## Benefits of Real Data

✅ More realistic symptom associations  
✅ Actual medical patterns  
✅ Better for presentation  
✅ Can cite real dataset source  
✅ More credible results
