# How to Run on Kaggle

## Step 1: Upload Notebook

1. Go to [Kaggle.com](https://www.kaggle.com)
2. Click "Code" → "New Notebook"
3. Click "File" → "Upload Notebook"
4. Select `kaggle_notebook.ipynb`

## Step 2: Add Dataset (Optional)

### Option A: Use Kaggle Dataset
1. Click "Add Data" in the right sidebar
2. Search for "Disease Symptom Prediction" or similar
3. Add the dataset to your notebook

### Option B: Generate Synthetic Data
The notebook will automatically generate synthetic data if no dataset is found.

## Step 3: Run the Notebook

1. Click "Run All" or run cells sequentially
2. Wait for analysis to complete (~2-3 minutes)
3. View visualizations inline

## Step 4: Download Results

1. Scroll to the bottom of the notebook
2. Click on `association_rules.json` in the output
3. Download the file
4. Use this file in the Flutter mobile app

## Expected Output

- **Frequent Itemsets**: 50-200 itemsets
- **Association Rules**: 100-300 rules
- **Visualizations**: 4 charts (scatter, bar, heatmap, network)
- **JSON Export**: `association_rules.json` (ready for mobile app)

## Troubleshooting

### "No module named 'mlxtend'"
Run this cell at the top:
```python
!pip install mlxtend networkx plotly kaleido -q
```

### "No data found"
The notebook will automatically generate synthetic data. Check the output of the data generation cell.

### Visualizations not showing
Make sure you're running in Kaggle's notebook environment, not a script.

## Tips

- Adjust `MIN_SUPPORT`, `MIN_CONFIDENCE`, `MIN_LIFT` thresholds for more/fewer rules
- Use GPU accelerator for faster processing (Settings → Accelerator → GPU)
- Save your work frequently (Ctrl+S)
- Make notebook public to share with others
