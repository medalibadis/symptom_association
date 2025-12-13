"""
Algorithm Comparison Script
Compares Apriori, FP-Growth, and ECLAT (Custom Implementation) performance.
"""

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, fpgrowth
from mlxtend.preprocessing import TransactionEncoder
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12})

# ==================== DATA LOADING (Reused) ====================
def load_and_preprocess():
    print("[*] Loading and preprocessing data...")
    if os.path.exists('data/processed_medical_data.csv'):
        df = pd.read_csv('data/processed_medical_data.csv')
    else:
        # Fallback if file doesn't exist, though it should
        print("[!] Data file not found. Please run symptom_analysis.py first.")
        return None

    # Symptom columns analysis
    symptom_cols = [col for col in df.columns 
                   if col not in ['patient_id', 'disease', 'num_symptoms', 'symptoms']]
    
    transactions = []
    for _, row in df.iterrows():
        patient_symptoms = [col for col in symptom_cols if row[col] == 1]
        if patient_symptoms:
            transactions.append(patient_symptoms)
            
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_binary = pd.DataFrame(te_ary, columns=te.columns_)
    
    return df_binary, transactions

# ==================== ECLAT IMPLEMENTATION ====================
class ECLAT:
    def __init__(self, min_support=0.05, min_items=1):
        self.min_support = min_support
        self.min_items = min_items
        self.item_tid_sets = {}
        self.frequent_itemsets = []
        self.start_time = 0
        self.end_time = 0

    def fit(self, df_binary):
        self.start_time = time.time()
        self.n_transactions = len(df_binary)
        self.min_support_count = self.min_support * self.n_transactions
        
        # 1. Transform horizontal to vertical format (Item -> TID set)
        # Using index as TID
        for col in df_binary.columns:
            # get indices where value is 1 (True)
            tids = set(df_binary.index[df_binary[col]].tolist())
            if len(tids) >= self.min_support_count:
                self.item_tid_sets[frozenset([col])] = tids
                
        # 2. Mine recursively
        self._mine(list(self.item_tid_sets.keys()))
        
        self.end_time = time.time()
        return self

    def _mine(self, itemsets):
        for i in range(len(itemsets)):
            itemset_i = itemsets[i]
            tids_i = self.item_tid_sets[itemset_i]
            
            # Add to frequent itemsets
            self.frequent_itemsets.append((itemset_i, len(tids_i)/self.n_transactions))
            
            suffix_itemsets = []
            
            for j in range(i + 1, len(itemsets)):
                itemset_j = itemsets[j]
                tids_j = self.item_tid_sets[itemset_j]
                
                # Intersection
                tids_join = tids_i.intersection(tids_j)
                
                if len(tids_join) >= self.min_support_count:
                    # New candidate
                    new_itemset = itemset_i.union(itemset_j)
                    self.item_tid_sets[new_itemset] = tids_join
                    suffix_itemsets.append(new_itemset)
            
            # Recursive call
            if suffix_itemsets:
                self._mine(suffix_itemsets)

# ==================== ALGORITHM RUNNERS ====================
def run_apriori(df, min_support):
    start = time.time()
    res = apriori(df, min_support=min_support, use_colnames=True)
    end = time.time()
    return end - start, len(res)

def run_fpgrowth(df, min_support):
    start = time.time()
    res = fpgrowth(df, min_support=min_support, use_colnames=True)
    end = time.time()
    return end - start, len(res)

def run_eclat(df, min_support):
    model = ECLAT(min_support=min_support)
    model.fit(df)
    return model.end_time - model.start_time, len(model.frequent_itemsets)

# ==================== MAIN COMPARISON ====================
import tracemalloc

def measure_performance(func, *args):
    """Measures execution time and peak memory usage."""
    tracemalloc.start()
    start_time = time.time()
    
    # Run algorithm
    result = func(*args)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    exec_time = end_time - start_time
    peak_memory_mb = peak / (1024 * 1024)
    
    return exec_time, peak_memory_mb, result

def plot_algorithm_performance(supports, times, memory, name, color):
    """Generates individual plots for Time and Memory."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Time Plot
    ax1.plot(supports, times, marker='o', color=color, linewidth=2)
    ax1.set_title(f'{name}: Execution Time', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Min Support', fontsize=10)
    ax1.set_ylabel('Time (s)', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.invert_xaxis()
    
    # Memory Plot
    ax2.plot(supports, memory, marker='o', color=color, linestyle='--', linewidth=2)
    ax2.set_title(f'{name}: Peak Memory Usage', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Min Support', fontsize=10)
    ax2.set_ylabel('Memory (MB)', fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.invert_xaxis()
    
    plt.tight_layout()
    filename = f"visualizations/{name.lower().replace('-', '_')}_performance.png"
    plt.savefig(filename, dpi=300)
    print(f"[OK] Saved {filename}")
    plt.close()

def main():
    df, _ = load_and_preprocess()
    if df is None:
        return

    # Supports to test (removed 0.01 for speed)
    supports = [0.2, 0.1, 0.05, 0.03]
    
    results = {
        'Support': supports,
        'Apriori_Time': [], 'Apriori_Mem': [],
        'FP_Growth_Time': [], 'FP_Growth_Mem': [],
        'ECLAT_Time': [], 'ECLAT_Mem': []
    }

    print("\nStarting Benchmarks (Time/Memory)...")
    print("-" * 80)
    print(f"{'Support':<8} | {'Apriori (s/MB)':<20} | {'FP-Growth (s/MB)':<20} | {'ECLAT (s/MB)':<20}")
    print("-" * 80)

    for sup in supports:
        # Apriori
        t_ap, m_ap, (_, n_ap) = measure_performance(lambda: run_apriori(df, sup))
        
        # FP-Growth
        t_fp, m_fp, (_, n_fp) = measure_performance(lambda: run_fpgrowth(df, sup))
        
        # ECLAT
        t_ec, m_ec, (_, n_ec) = measure_performance(lambda: run_eclat(df, sup))
        
        results['Apriori_Time'].append(t_ap)
        results['Apriori_Mem'].append(m_ap)
        results['FP_Growth_Time'].append(t_fp)
        results['FP_Growth_Mem'].append(m_fp)
        results['ECLAT_Time'].append(t_ec)
        results['ECLAT_Mem'].append(m_ec)
        
        print(f"{sup:<8.2f} | {t_ap:.4f}s / {m_ap:.2f}MB   | {t_fp:.4f}s / {m_fp:.2f}MB   | {t_ec:.4f}s / {m_ec:.2f}MB")

    # 1. Individual Plots
    plot_algorithm_performance(supports, results['Apriori_Time'], results['Apriori_Mem'], 'Apriori', 'blue')
    plot_algorithm_performance(supports, results['FP_Growth_Time'], results['FP_Growth_Mem'], 'FP-Growth', 'green')
    plot_algorithm_performance(supports, results['ECLAT_Time'], results['ECLAT_Mem'], 'ECLAT', 'red')

    # 2. Comparison Plot (Time)
    plt.figure(figsize=(10, 6))
    plt.plot(supports, results['Apriori_Time'], marker='o', label='Apriori', linewidth=2)
    plt.plot(supports, results['FP_Growth_Time'], marker='s', label='FP-Growth', linewidth=2)
    plt.plot(supports, results['ECLAT_Time'], marker='^', label='ECLAT', linewidth=2)
    plt.title('Algorithm Execution Time Comparison', fontsize=14, fontweight='bold')
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().invert_xaxis()
    plt.savefig('visualizations/algorithm_comparison_time.png', dpi=300)
    print("\n[OK] Saved visualizations/algorithm_comparison_time.png")
    
    # 3. Comparison Plot (Memory)
    plt.figure(figsize=(10, 6))
    plt.plot(supports, results['Apriori_Mem'], marker='o', label='Apriori', linewidth=2)
    plt.plot(supports, results['FP_Growth_Mem'], marker='s', label='FP-Growth', linewidth=2)
    plt.plot(supports, results['ECLAT_Mem'], marker='^', label='ECLAT', linewidth=2)
    plt.title('Algorithm Memory Usage Comparison', fontsize=14, fontweight='bold')
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Peak Memory (MB)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().invert_xaxis()
    plt.savefig('visualizations/algorithm_comparison_memory.png', dpi=300)
    print("[OK] Saved visualizations/algorithm_comparison_memory.png")

    # Save CSV
    pd.DataFrame(results).to_csv('visualizations/algorithm_metrics.csv', index=False)
    print("[OK] Metrics saved to visualizations/algorithm_metrics.csv")

if __name__ == "__main__":
    main()
