"""
Healthcare Symptom Association Discovery - Updated for Real Dataset
Complete implementation with Apriori algorithm and visualizations
Now supports real Kaggle disease-symptom dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Import real data loader
from real_data_loader import load_real_dataset, preprocess_dataset, create_transaction_list

# Configuration
MIN_SUPPORT = 0.05  # Minimum support threshold (5%)
MIN_CONFIDENCE = 0.6  # Minimum confidence threshold (60%)
MIN_LIFT = 1.2  # Minimum lift threshold

# Create output directories
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)
os.makedirs('visualizations', exist_ok=True)

print("=" * 70)
print("HEALTHCARE SYMPTOM ASSOCIATION DISCOVERY")
print("=" * 70)
print(f"Min Support: {MIN_SUPPORT}")
print(f"Min Confidence: {MIN_CONFIDENCE}")
print(f"Min Lift: {MIN_LIFT}")
print("=" * 70)


# ==================== DATA LOADING ====================
def load_data():
    """Load medical dataset - supports both real and synthetic data"""
    print("\n[*] Loading data...")
    
    # Try to load real dataset first
    result = load_real_dataset('data')
    
    if result and result[0] is not None:
        print("[OK] Using real Kaggle dataset")
        df_main, df_severity, df_description, df_precaution = result
        
        # Preprocess
        df_binary, all_symptoms = preprocess_dataset(df_main)
        
        # Save processed data
        df_binary.to_csv('data/processed_medical_data.csv', index=False)
        
        return df_binary, all_symptoms
    else:
        # Fall back to synthetic data
        print("[!] Real dataset not found. Generating synthetic data...")
        import data_generator
        df = data_generator.generate_dataset(n_samples=1000)
        data_generator.save_dataset(df, 'data/medical_data.csv')
        
        # Extract symptom columns
        symptom_cols = [col for col in df.columns 
                       if col not in ['patient_id', 'disease', 'num_symptoms', 'symptoms']]
        
        return df, symptom_cols


# ==================== DATA PREPROCESSING ====================
def prepare_transactions(df, symptom_cols):
    """Convert dataset to transaction format for Apriori"""
    print("\n[*] Preparing transaction data...")
    
    # Convert to transaction format (list of lists)
    transactions = []
    for _, row in df.iterrows():
        # Get symptoms where value is 1
        patient_symptoms = [col for col in symptom_cols if row[col] == 1]
        if patient_symptoms:  # Only add non-empty transactions
            transactions.append(patient_symptoms)
    
    print(f"[OK] Prepared {len(transactions)} transactions")
    print(f"     Unique symptoms: {len(symptom_cols)}")
    print(f"     Avg symptoms per transaction: {sum(len(t) for t in transactions)/len(transactions):.2f}")
    
    return transactions


def create_binary_matrix(transactions, symptom_cols):
    """Create binary matrix for Apriori"""
    print("\n[*] Creating binary matrix...")
    
    # Use TransactionEncoder
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_binary = pd.DataFrame(te_ary, columns=te.columns_)
    
    print(f"[OK] Binary matrix created: {df_binary.shape}")
    
    return df_binary


# ==================== ASSOCIATION RULE MINING ====================
def mine_frequent_itemsets(df_binary, min_support=MIN_SUPPORT):
    """Apply Apriori algorithm to find frequent itemsets"""
    print(f"\n[*] Mining frequent itemsets (min_support={min_support})...")
    
    frequent_itemsets = apriori(df_binary, min_support=min_support, use_colnames=True)
    
    print(f"[OK] Found {len(frequent_itemsets)} frequent itemsets")
    
    # Show top itemsets
    if len(frequent_itemsets) > 0:
        top_itemsets = frequent_itemsets.nlargest(10, 'support')
        print("\n     Top 10 Frequent Itemsets:")
        for idx, row in top_itemsets.iterrows():
            items = ', '.join(list(row['itemsets']))
            print(f"     - {items} (support: {row['support']:.3f})")
    
    return frequent_itemsets


def generate_association_rules(frequent_itemsets, min_confidence=MIN_CONFIDENCE):
    """Generate association rules from frequent itemsets"""
    print(f"\n[*] Generating association rules (min_confidence={min_confidence})...")
    
    if len(frequent_itemsets) == 0:
        print("[!] No frequent itemsets found. Cannot generate rules.")
        return pd.DataFrame()
    
    rules = association_rules(frequent_itemsets, 
                              metric="confidence", 
                              min_threshold=min_confidence)
    
    # Calculate additional metrics
    if len(rules) > 0:
        # Filter by lift
        rules = rules[rules['lift'] >= MIN_LIFT]
        
        # Sort by lift
        rules = rules.sort_values('lift', ascending=False)
        
        print(f"[OK] Generated {len(rules)} association rules")
        
        # Show top rules
        print("\n     Top 10 Association Rules:")
        for idx, row in rules.head(10).iterrows():
            antecedents = ', '.join(list(row['antecedents']))
            consequents = ', '.join(list(row['consequents']))
            print(f"     - {antecedents} → {consequents}")
            print(f"       Support: {row['support']:.3f}, Confidence: {row['confidence']:.3f}, Lift: {row['lift']:.3f}")
    else:
        print("[!] No rules generated with current thresholds")
    
    return rules


# ==================== VISUALIZATION ====================
def plot_support_confidence_scatter(rules):
    """Scatter plot of support vs confidence"""
    if len(rules) == 0:
        return
    
    print("\n[*] Creating support-confidence scatter plot...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    scatter = ax.scatter(rules['support'], rules['confidence'], 
                        c=rules['lift'], s=rules['lift']*50, 
                        alpha=0.6, cmap='viridis', edgecolors='black', linewidth=0.5)
    
    ax.set_xlabel('Support', fontsize=12, fontweight='bold')
    ax.set_ylabel('Confidence', fontsize=12, fontweight='bold')
    ax.set_title('Association Rules: Support vs Confidence (sized by Lift)', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Lift', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('visualizations/support_confidence_scatter.png', dpi=300, bbox_inches='tight')
    print("     [OK] Saved: visualizations/support_confidence_scatter.png")
    plt.close()


def plot_top_rules_bar(rules, top_n=20):
    """Bar chart of top association rules"""
    if len(rules) == 0:
        return
    
    print("\n[*] Creating top rules bar chart...")
    
    top_rules = rules.nlargest(top_n, 'lift').copy()
    
    # Create rule labels
    top_rules['rule'] = top_rules.apply(
        lambda row: f"{', '.join(list(row['antecedents'])[:2])} → {', '.join(list(row['consequents'])[:2])}", 
        axis=1
    )
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    y_pos = np.arange(len(top_rules))
    ax.barh(y_pos, top_rules['lift'], color='steelblue', alpha=0.8)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_rules['rule'], fontsize=9)
    ax.set_xlabel('Lift', fontsize=12, fontweight='bold')
    ax.set_title(f'Top {top_n} Association Rules by Lift', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(top_rules['lift']):
        ax.text(v + 0.05, i, f'{v:.2f}', va='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('visualizations/top_rules_bar.png', dpi=300, bbox_inches='tight')
    print("     [OK] Saved: visualizations/top_rules_bar.png")
    plt.close()


def plot_symptom_network(rules, top_n=30):
    """Network graph of symptom associations"""
    if len(rules) == 0:
        return
    
    print("\n[*] Creating symptom network graph...")
    
    # Get top rules
    top_rules = rules.nlargest(top_n, 'lift')
    
    # Create graph
    G = nx.DiGraph()
    
    for _, row in top_rules.iterrows():
        antecedents = list(row['antecedents'])
        consequents = list(row['consequents'])
        
        for ant in antecedents[:2]:  # Limit to avoid clutter
            for cons in consequents[:2]:
                # Add edge with weight = lift
                if G.has_edge(ant, cons):
                    G[ant][cons]['weight'] += row['lift']
                else:
                    G.add_edge(ant, cons, weight=row['lift'])
    
    # Create layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Plot
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Draw nodes
    node_sizes = [G.degree(node) * 300 for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                          node_color='lightblue', alpha=0.9, 
                          edgecolors='darkblue', linewidths=2, ax=ax)
    
    # Draw edges
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    nx.draw_networkx_edges(G, pos, width=[w/max_weight*5 for w in weights],
                          alpha=0.5, edge_color='gray', 
                          arrows=True, arrowsize=20, ax=ax)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
    
    ax.set_title(f'Symptom Association Network (Top {top_n} Rules)', 
                fontsize=16, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('visualizations/symptom_network.png', dpi=300, bbox_inches='tight')
    print("     [OK] Saved: visualizations/symptom_network.png")
    plt.close()


def plot_symptom_heatmap(df_binary, top_n=20):
    """Heatmap of symptom co-occurrences"""
    print("\n[*] Creating symptom co-occurrence heatmap...")
    
    # Calculate co-occurrence matrix
    co_occurrence = df_binary.T.dot(df_binary)
    
    # Get top symptoms by frequency
    symptom_freq = df_binary.sum().sort_values(ascending=False)
    top_symptoms = symptom_freq.head(top_n).index
    
    # Filter matrix
    co_occurrence_top = co_occurrence.loc[top_symptoms, top_symptoms]
    
    # Plot
    fig, ax = plt.subplots(figsize=(14, 12))
    
    sns.heatmap(co_occurrence_top, annot=True, fmt='d', cmap='YlOrRd', 
                square=True, linewidths=0.5, cbar_kws={'label': 'Co-occurrence Count'},
                ax=ax)
    
    ax.set_title(f'Top {top_n} Symptom Co-occurrence Heatmap', 
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('visualizations/symptom_heatmap.png', dpi=300, bbox_inches='tight')
    print("     [OK] Saved: visualizations/symptom_heatmap.png")
    plt.close()


def create_interactive_network(rules, top_n=50):
    """Create interactive network visualization with Plotly"""
    if len(rules) == 0:
        return
    
    print("\n[*] Creating interactive network visualization...")
    
    # Get top rules
    top_rules = rules.nlargest(top_n, 'lift')
    
    # Create graph
    G = nx.DiGraph()
    
    for _, row in top_rules.iterrows():
        antecedents = list(row['antecedents'])
        consequents = list(row['consequents'])
        
        for ant in antecedents[:2]:
            for cons in consequents[:2]:
                G.add_edge(ant, cons, weight=row['lift'], 
                          confidence=row['confidence'], support=row['support'])
    
    # Create layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node}<br>Degree: {G.degree(node)}")
        node_size.append(G.degree(node) * 10 + 20)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="top center",
        hovertext=node_text,
        hoverinfo='text',
        marker=dict(
            size=node_size,
            color='lightblue',
            line=dict(width=2, color='darkblue')
        ))
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title=f'Interactive Symptom Association Network (Top {top_n} Rules)',
                       titlefont_size=16,
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=0, l=0, r=0, t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                   )
    
    fig.write_html('visualizations/interactive_network.html')
    print("     [OK] Saved: visualizations/interactive_network.html")


# ==================== MAIN EXECUTION ====================
def main():
    """Main execution function"""
    
    # Load data (real or synthetic)
    df, symptom_cols = load_data()
    
    # Prepare transactions
    transactions = prepare_transactions(df, symptom_cols)
    
    # Create binary matrix
    df_binary = create_binary_matrix(transactions, symptom_cols)
    
    # Mine frequent itemsets
    frequent_itemsets = mine_frequent_itemsets(df_binary)
    
    # Generate association rules
    rules = generate_association_rules(frequent_itemsets)
    
    if len(rules) > 0:
        # Create visualizations
        plot_support_confidence_scatter(rules)
        plot_top_rules_bar(rules, top_n=20)
        plot_symptom_network(rules, top_n=30)
        plot_symptom_heatmap(df_binary, top_n=20)
        create_interactive_network(rules, top_n=50)
        
        # Export model
        export_rules_to_json(rules, symptom_cols)
        
        # Save rules to CSV
        rules_export = rules.copy()
        rules_export['antecedents'] = rules_export['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules_export['consequents'] = rules_export['consequents'].apply(lambda x: ', '.join(list(x)))
        rules_export.to_csv('models/association_rules.csv', index=False)
        print(f"[OK] Saved rules to: models/association_rules.csv")
    
    print("\n" + "=" * 70)
    print("[SUCCESS] ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nOutput files:")
    print("   - models/association_rules.json")
    print("   - models/association_rules.csv")
    print("\nNext step: Use association_rules.json in Flutter mobile app!")
    print("=" * 70)


def export_rules_to_json(rules, symptom_cols, filepath='models/association_rules.json'):
    """Export association rules to JSON for mobile app"""
    print("\n[*] Exporting rules to JSON...")
    
    if len(rules) == 0:
        print("[!] No rules to export")
        return
    
    # Convert rules to JSON-serializable format
    rules_list = []
    for _, row in rules.iterrows():
        # Handle Infinity and NaN values
        conviction = row.get('conviction', None)
        if conviction is not None and (np.isinf(conviction) or np.isnan(conviction)):
            conviction = None
        
        rule = {
            'antecedents': list(row['antecedents']),
            'consequents': list(row['consequents']),
            'support': float(row['support']),
            'confidence': float(row['confidence']),
            'lift': float(row['lift']),
            'conviction': float(conviction) if conviction is not None else None
        }
        rules_list.append(rule)
    
    # Create export data
    export_data = {
        'metadata': {
            'total_rules': len(rules),
            'min_support': MIN_SUPPORT,
            'min_confidence': MIN_CONFIDENCE,
            'min_lift': MIN_LIFT,
            'total_symptoms': len(symptom_cols)
        },
        'symptoms': sorted(symptom_cols),
        'rules': rules_list
    }
    
    # Save to JSON
    with open(filepath, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"[OK] Exported {len(rules_list)} rules to: {filepath}")
    print(f"     File size: {os.path.getsize(filepath) / 1024:.2f} KB")


if __name__ == "__main__":
    main()
