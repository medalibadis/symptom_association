import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data captured from the interrupted benchmark run
data = {
    'Support': [0.20, 0.10, 0.05],
    'Apriori_Time': [0.0025, 0.0094, 0.0459],
    'Apriori_Mem': [0.37, 2.68, 20.83],
    'FP_Growth_Time': [0.0789, 3.6717, 35.5842],
    'FP_Growth_Mem': [11.15, 11.14, 11.14],
    'ECLAT_Time': [0.0197, 0.0482, 0.0323],
    'ECLAT_Mem': [1.16, 3.33, 13.44]
}

def plot_individual(supports, times, memory, name, color):
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
    # Ensure directory exists
    import os
    os.makedirs('visualizations', exist_ok=True)
    filename = f"visualizations/{name.lower().replace('-', '_')}_performance.png"
    plt.savefig(filename, dpi=300)
    print(f"[OK] Saved {filename}")
    plt.close()

def main():
    supports = data['Support']
    
    # 1. Individual Plots
    plot_individual(supports, data['Apriori_Time'], data['Apriori_Mem'], 'Apriori', 'blue')
    plot_individual(supports, data['FP_Growth_Time'], data['FP_Growth_Mem'], 'FP-Growth', 'green')
    plot_individual(supports, data['ECLAT_Time'], data['ECLAT_Mem'], 'ECLAT', 'red')

    # 2. Comparison Plot (Time)
    plt.figure(figsize=(10, 6))
    plt.plot(supports, data['Apriori_Time'], marker='o', label='Apriori', linewidth=2, color='blue')
    plt.plot(supports, data['FP_Growth_Time'], marker='s', label='FP-Growth', linewidth=2, color='green')
    plt.plot(supports, data['ECLAT_Time'], marker='^', label='ECLAT', linewidth=2, color='red')
    plt.title('Algorithm Execution Time Comparison', fontsize=14, fontweight='bold')
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Time (s) - Log Scale', fontsize=12)
    plt.yscale('log') # Use log scale because FP-Growth is massive
    plt.legend()
    plt.grid(True, alpha=0.3, which="both", ls="-")
    plt.gca().invert_xaxis()
    plt.savefig('visualizations/algorithm_comparison_time.png', dpi=300)
    print("[OK] Saved visualizations/algorithm_comparison_time.png")
    
    # 3. Comparison Plot (Memory)
    plt.figure(figsize=(10, 6))
    plt.plot(supports, data['Apriori_Mem'], marker='o', label='Apriori', linewidth=2, color='blue')
    plt.plot(supports, data['FP_Growth_Mem'], marker='s', label='FP-Growth', linewidth=2, color='green')
    plt.plot(supports, data['ECLAT_Mem'], marker='^', label='ECLAT', linewidth=2, color='red')
    plt.title('Algorithm Memory Usage Comparison', fontsize=14, fontweight='bold')
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Peak Memory (MB)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().invert_xaxis()
    plt.savefig('visualizations/algorithm_comparison_memory.png', dpi=300)
    print("[OK] Saved visualizations/algorithm_comparison_memory.png")

    # Save CSV
    pd.DataFrame(data).to_csv('visualizations/algorithm_metrics.csv', index=False)
    print("[OK] Metrics saved to visualizations/algorithm_metrics.csv")

if __name__ == "__main__":
    main()
