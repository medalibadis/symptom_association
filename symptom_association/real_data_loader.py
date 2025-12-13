"""
Real Dataset Loader for Kaggle Disease-Symptom Dataset
Handles: dataset.csv, Symptom-severity.csv, symptom_Description.csv, symptom_precaution.csv
"""

import pandas as pd
import numpy as np
import os

def load_real_dataset(data_dir='data'):
    """
    Load and process real Kaggle disease-symptom dataset
    
    Expected files:
    - dataset.csv: Main disease-symptom data
    - Symptom-severity.csv: Symptom severity weights
    - symptom_Description.csv: Disease descriptions
    - symptom_precaution.csv: Disease precautions
    """
    print("\n[*] Loading real Kaggle dataset...")
    
    # Load main dataset
    dataset_path = os.path.join(data_dir, 'dataset.csv')
    if not os.path.exists(dataset_path):
        print(f"[!] dataset.csv not found in {data_dir}")
        return None
    
    df_main = pd.read_csv(dataset_path)
    print(f"[OK] Loaded dataset.csv: {df_main.shape}")
    
    # Load additional files if available
    severity_path = os.path.join(data_dir, 'Symptom-severity.csv')
    if os.path.exists(severity_path):
        df_severity = pd.read_csv(severity_path)
        print(f"[OK] Loaded Symptom-severity.csv: {df_severity.shape}")
    else:
        df_severity = None
        print("[!] Symptom-severity.csv not found (optional)")
    
    description_path = os.path.join(data_dir, 'symptom_Description.csv')
    if os.path.exists(description_path):
        df_description = pd.read_csv(description_path)
        print(f"[OK] Loaded symptom_Description.csv: {df_description.shape}")
    else:
        df_description = None
        print("[!] symptom_Description.csv not found (optional)")
    
    precaution_path = os.path.join(data_dir, 'symptom_precaution.csv')
    if os.path.exists(precaution_path):
        df_precaution = pd.read_csv(precaution_path)
        print(f"[OK] Loaded symptom_precaution.csv: {df_precaution.shape}")
    else:
        df_precaution = None
        print("[!] symptom_precaution.csv not found (optional)")
    
    return df_main, df_severity, df_description, df_precaution


def preprocess_dataset(df_main):
    """
    Preprocess the main dataset for association rule mining
    
    The dataset typically has format:
    Disease | Symptom_1 | Symptom_2 | ... | Symptom_17
    """
    print("\n[*] Preprocessing dataset...")
    
    # Display dataset info
    print(f"   Columns: {list(df_main.columns)}")
    print(f"   Shape: {df_main.shape}")
    
    # Get disease column (usually first column)
    disease_col = df_main.columns[0]
    print(f"   Disease column: {disease_col}")
    
    # Get symptom columns (all except disease)
    symptom_cols = [col for col in df_main.columns if col != disease_col]
    print(f"   Symptom columns: {len(symptom_cols)}")
    
    # Create binary matrix
    # Replace NaN with empty string
    df_processed = df_main.copy()
    df_processed = df_processed.fillna('')
    
    # Get all unique symptoms
    all_symptoms = set()
    for col in symptom_cols:
        symptoms = df_processed[col].unique()
        all_symptoms.update([s.strip() for s in symptoms if s and s.strip()])
    
    all_symptoms = sorted(list(all_symptoms))
    print(f"   Unique symptoms found: {len(all_symptoms)}")
    
    # Create binary encoding
    binary_data = []
    
    for idx, row in df_processed.iterrows():
        disease = row[disease_col]
        patient_symptoms = []
        
        # Collect all symptoms for this patient
        for col in symptom_cols:
            symptom = str(row[col]).strip()
            if symptom and symptom != '' and symptom != 'nan':
                patient_symptoms.append(symptom)
        
        # Create binary row
        binary_row = {'patient_id': f'P{idx+1:04d}', 'disease': disease}
        for symptom in all_symptoms:
            binary_row[symptom] = 1 if symptom in patient_symptoms else 0
        
        binary_data.append(binary_row)
    
    df_binary = pd.DataFrame(binary_data)
    
    print(f"[OK] Created binary matrix: {df_binary.shape}")
    print(f"   Patients: {len(df_binary)}")
    print(f"   Symptoms: {len(all_symptoms)}")
    
    return df_binary, all_symptoms


def create_transaction_list(df_binary, all_symptoms):
    """
    Convert binary matrix to transaction list for Apriori
    """
    print("\n[*] Creating transaction list...")
    
    transactions = []
    for idx, row in df_binary.iterrows():
        patient_symptoms = [symptom for symptom in all_symptoms if row[symptom] == 1]
        if patient_symptoms:
            transactions.append(patient_symptoms)
    
    print(f"[OK] Created {len(transactions)} transactions")
    print(f"   Avg symptoms per transaction: {sum(len(t) for t in transactions)/len(transactions):.2f}")
    
    return transactions


def save_processed_data(df_binary, filepath='data/processed_medical_data.csv'):
    """Save processed binary data"""
    df_binary.to_csv(filepath, index=False)
    print(f"\n[OK] Saved processed data to: {filepath}")


if __name__ == "__main__":
    print("=" * 70)
    print("REAL DATASET LOADER TEST")
    print("=" * 70)
    
    # Load dataset
    result = load_real_dataset('data')
    
    if result:
        df_main, df_severity, df_description, df_precaution = result
        
        # Preprocess
        df_binary, all_symptoms = preprocess_dataset(df_main)
        
        # Create transactions
        transactions = create_transaction_list(df_binary, all_symptoms)
        
        # Save processed data
        save_processed_data(df_binary)
        
        # Display sample
        print("\n" + "=" * 70)
        print("SAMPLE DATA")
        print("=" * 70)
        print(df_binary[['patient_id', 'disease'] + all_symptoms[:5]].head(10))
        
        print("\n" + "=" * 70)
        print("SAMPLE TRANSACTIONS")
        print("=" * 70)
        for i, trans in enumerate(transactions[:5], 1):
            print(f"{i}. {', '.join(trans)}")
        
        print("\n✓ Dataset loaded and processed successfully!")
    else:
        print("\n[!] Failed to load dataset. Please check file paths.")
