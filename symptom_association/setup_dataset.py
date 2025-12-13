"""
Quick Setup Script - Copy your dataset files to the correct location
Run this after placing your CSV files in the symptom_association folder
"""

import os
import shutil

print("=" * 70)
print("DATASET SETUP HELPER")
print("=" * 70)

# Files to look for
dataset_files = [
    'dataset.csv',
    'Symptom-severity.csv',
    'symptom_Description.csv',
    'symptom_precaution.csv'
]

# Check current directory
current_dir = os.getcwd()
print(f"\nCurrent directory: {current_dir}")

# Create data folder if it doesn't exist
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"\n✓ Created '{data_dir}' folder")
else:
    print(f"\n✓ '{data_dir}' folder already exists")

# Check for files in current directory and move them
found_files = []
missing_files = []

for filename in dataset_files:
    if os.path.exists(filename):
        # File found in current directory, move to data/
        dest_path = os.path.join(data_dir, filename)
        shutil.copy(filename, dest_path)
        found_files.append(filename)
        print(f"  ✓ Copied {filename} to {data_dir}/")
    elif os.path.exists(os.path.join(data_dir, filename)):
        # File already in data/ folder
        found_files.append(filename)
        print(f"  ✓ {filename} already in {data_dir}/")
    else:
        missing_files.append(filename)
        print(f"  ✗ {filename} not found")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Found: {len(found_files)}/{len(dataset_files)} files")

if found_files:
    print("\n✓ Files ready:")
    for f in found_files:
        print(f"  - {f}")

if missing_files:
    print("\n✗ Missing files:")
    for f in missing_files:
        print(f"  - {f}")
    print("\nPlease place these files in the symptom_association folder")
    print("and run this script again.")
else:
    print("\n🎉 All dataset files are in place!")
    print("\nNext steps:")
    print("  1. Run: python real_data_loader.py")
    print("  2. Run: python symptom_analysis_updated.py")

print("=" * 70)
