"""
Synthetic Medical Data Generator
Generates realistic symptom-disease associations for testing
"""

import pandas as pd
import numpy as np
import random
from itertools import combinations

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define comprehensive symptom and disease lists
SYMPTOMS = [
    'fever', 'cough', 'fatigue', 'headache', 'sore_throat',
    'runny_nose', 'shortness_of_breath', 'body_ache', 'chills',
    'nausea', 'vomiting', 'diarrhea', 'abdominal_pain', 'loss_of_appetite',
    'chest_pain', 'dizziness', 'weakness', 'sweating', 'rash',
    'itching', 'sneezing', 'watery_eyes', 'congestion', 'wheezing',
    'joint_pain', 'muscle_pain', 'back_pain', 'neck_pain',
    'loss_of_smell', 'loss_of_taste', 'confusion', 'anxiety',
    'insomnia', 'rapid_heartbeat', 'high_blood_pressure',
    'low_blood_pressure', 'swelling', 'numbness', 'tingling',
    'blurred_vision', 'sensitivity_to_light', 'ear_pain',
    'difficulty_swallowing', 'hoarseness', 'dry_cough', 'productive_cough',
    'night_sweats', 'weight_loss', 'weight_gain', 'frequent_urination'
]

# Define disease patterns with typical symptom combinations
DISEASE_PATTERNS = {
    'Common Cold': {
        'core': ['runny_nose', 'sneezing', 'sore_throat', 'cough'],
        'common': ['congestion', 'headache', 'fatigue', 'watery_eyes'],
        'rare': ['fever', 'body_ache']
    },
    'Influenza': {
        'core': ['fever', 'cough', 'body_ache', 'fatigue'],
        'common': ['headache', 'chills', 'sore_throat', 'weakness'],
        'rare': ['nausea', 'vomiting', 'diarrhea']
    },
    'COVID-19': {
        'core': ['fever', 'dry_cough', 'fatigue', 'loss_of_smell', 'loss_of_taste'],
        'common': ['shortness_of_breath', 'body_ache', 'headache', 'sore_throat'],
        'rare': ['diarrhea', 'rash', 'confusion']
    },
    'Pneumonia': {
        'core': ['fever', 'productive_cough', 'chest_pain', 'shortness_of_breath'],
        'common': ['fatigue', 'sweating', 'chills', 'weakness'],
        'rare': ['nausea', 'confusion', 'rapid_heartbeat']
    },
    'Bronchitis': {
        'core': ['productive_cough', 'chest_pain', 'fatigue'],
        'common': ['shortness_of_breath', 'wheezing', 'sore_throat', 'fever'],
        'rare': ['body_ache', 'headache']
    },
    'Allergic Rhinitis': {
        'core': ['sneezing', 'runny_nose', 'watery_eyes', 'itching'],
        'common': ['congestion', 'sore_throat', 'cough'],
        'rare': ['headache', 'fatigue']
    },
    'Asthma': {
        'core': ['wheezing', 'shortness_of_breath', 'chest_pain', 'cough'],
        'common': ['fatigue', 'rapid_heartbeat', 'anxiety'],
        'rare': ['sweating', 'dizziness']
    },
    'Gastroenteritis': {
        'core': ['nausea', 'vomiting', 'diarrhea', 'abdominal_pain'],
        'common': ['fever', 'weakness', 'loss_of_appetite', 'headache'],
        'rare': ['muscle_pain', 'chills']
    },
    'Migraine': {
        'core': ['headache', 'sensitivity_to_light', 'nausea'],
        'common': ['vomiting', 'dizziness', 'blurred_vision'],
        'rare': ['numbness', 'tingling', 'confusion']
    },
    'Hypertension': {
        'core': ['high_blood_pressure', 'headache', 'dizziness'],
        'common': ['chest_pain', 'shortness_of_breath', 'blurred_vision'],
        'rare': ['nausea', 'anxiety', 'sweating']
    },
    'Anxiety Disorder': {
        'core': ['anxiety', 'rapid_heartbeat', 'sweating'],
        'common': ['dizziness', 'shortness_of_breath', 'insomnia', 'fatigue'],
        'rare': ['nausea', 'abdominal_pain', 'headache']
    },
    'Strep Throat': {
        'core': ['sore_throat', 'fever', 'difficulty_swallowing'],
        'common': ['headache', 'rash', 'body_ache', 'swelling'],
        'rare': ['nausea', 'vomiting', 'abdominal_pain']
    },
    'Sinusitis': {
        'core': ['congestion', 'headache', 'facial_pain', 'runny_nose'],
        'common': ['fever', 'cough', 'fatigue', 'loss_of_smell'],
        'rare': ['ear_pain', 'sore_throat']
    },
    'Arthritis': {
        'core': ['joint_pain', 'swelling', 'stiffness'],
        'common': ['fatigue', 'weakness', 'muscle_pain'],
        'rare': ['fever', 'weight_loss', 'rash']
    },
    'Diabetes': {
        'core': ['frequent_urination', 'fatigue', 'weight_loss'],
        'common': ['blurred_vision', 'numbness', 'tingling', 'weakness'],
        'rare': ['nausea', 'dizziness', 'confusion']
    }
}

# Add facial_pain and stiffness to symptoms if not present
if 'facial_pain' not in SYMPTOMS:
    SYMPTOMS.extend(['facial_pain', 'stiffness'])


def generate_patient_record(disease, pattern):
    """Generate a single patient record with symptoms for a disease"""
    symptoms_present = []
    
    # Core symptoms (90% probability each)
    for symptom in pattern['core']:
        if random.random() < 0.9:
            symptoms_present.append(symptom)
    
    # Common symptoms (50% probability each)
    for symptom in pattern['common']:
        if random.random() < 0.5:
            symptoms_present.append(symptom)
    
    # Rare symptoms (10% probability each)
    for symptom in pattern['rare']:
        if random.random() < 0.1:
            symptoms_present.append(symptom)
    
    # Add 1-2 random noise symptoms (5% probability)
    if random.random() < 0.05:
        noise_symptoms = random.sample([s for s in SYMPTOMS if s not in symptoms_present], 
                                      min(2, len(SYMPTOMS) - len(symptoms_present)))
        symptoms_present.extend(noise_symptoms)
    
    return symptoms_present


def generate_dataset(n_samples=1000):
    """Generate complete synthetic medical dataset"""
    print(f"Generating {n_samples} patient records...")
    
    records = []
    diseases = list(DISEASE_PATTERNS.keys())
    
    for i in range(n_samples):
        # Select random disease
        disease = random.choice(diseases)
        pattern = DISEASE_PATTERNS[disease]
        
        # Generate symptoms
        symptoms = generate_patient_record(disease, pattern)
        
        # Create record
        record = {
            'patient_id': f'P{i+1:04d}',
            'disease': disease,
            'num_symptoms': len(symptoms),
            'symptoms': ','.join(symptoms)
        }
        
        # Add binary columns for each symptom
        for symptom in SYMPTOMS:
            record[symptom] = 1 if symptom in symptoms else 0
        
        records.append(record)
    
    df = pd.DataFrame(records)
    
    print(f"✓ Generated {len(df)} records")
    print(f"✓ Diseases: {len(diseases)}")
    print(f"✓ Unique symptoms: {len(SYMPTOMS)}")
    print(f"✓ Average symptoms per patient: {df['num_symptoms'].mean():.2f}")
    
    return df


def save_dataset(df, filepath='data/medical_data.csv'):
    """Save dataset to CSV"""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"\n✓ Dataset saved to: {filepath}")
    return filepath


def generate_transaction_format(df):
    """Convert to transaction format for Apriori"""
    transactions = []
    
    for _, row in df.iterrows():
        symptoms = row['symptoms'].split(',')
        transactions.append(symptoms)
    
    return transactions


if __name__ == "__main__":
    print("=" * 60)
    print("MEDICAL DATA GENERATOR")
    print("=" * 60)
    
    # Generate dataset
    df = generate_dataset(n_samples=1000)
    
    # Save to CSV
    filepath = save_dataset(df, 'data/medical_data.csv')
    
    # Display sample
    print("\n" + "=" * 60)
    print("SAMPLE RECORDS")
    print("=" * 60)
    print(df[['patient_id', 'disease', 'num_symptoms', 'symptoms']].head(10))
    
    # Display statistics
    print("\n" + "=" * 60)
    print("DISEASE DISTRIBUTION")
    print("=" * 60)
    print(df['disease'].value_counts())
    
    print("\n" + "=" * 60)
    print("TOP 10 MOST COMMON SYMPTOMS")
    print("=" * 60)
    symptom_counts = df[SYMPTOMS].sum().sort_values(ascending=False)
    print(symptom_counts.head(10))
    
    print("\n✓ Data generation complete!")
