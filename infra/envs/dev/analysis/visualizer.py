#!/usr/bin/env python3
"""
Data Visualization Component
Creates comprehensive dashboards and charts
"""
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data_and_stats(processed_path, stats_path):
    """Load processed data and statistical analysis"""
    print(f"📊 Loading data and statistics...")
    
    # Load processed data
    with open(processed_path, 'r') as f:
        data_dict = json.load(f)
    df = pd.DataFrame(data_dict['data'])
    
    # Load statistical analysis
    with open(stats_path, 'r') as f:
        stats = json.load(f)
    
    print(f"   ✓ Loaded data ({len(df)} rows) and statistical analysis")
    return df, stats

def create_correlation_heatmap(df, stats, output_dir):
    """Create correlation matrix heatmap"""
    print("🔥 Creating correlation heatmap...")
    
    numeric_cols = [col for col in df.columns if col in stats['descriptive_statistics']]
    if len(numeric_cols) < 2:
        print("   ⚠️ Skipping correlation heatmap (need 2+ numeric columns)")
        return None
    
    plt.figure(figsize=(10, 8))
    corr_matrix = df[numeric_cols].corr()
    
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, 
                mask=mask,
                annot=True, 
                cmap='RdBu_r', 
                center=0,
                square=True,
                fmt='.2f',
                cbar_kws={"shrink": .8})
    
    plt.title('Correlation Matrix Heatmap', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    heatmap_path = output_dir / 'correlation_heatmap.png'
    plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Saved correlation heatmap: {heatmap_path}")
    return str(heatmap_path)

def create_distribution_plots(df, stats, output_dir):
    """Create distribution plots for numeric variables"""
    print("📈 Creating distribution plots...")
    
    numeric_cols = [col for col in df.columns if col in stats['descriptive_statistics']]
    if not numeric_cols:
        print("   ⚠️ No numeric columns for distribution plots")
        return []
    
    # Create subplots
    n_cols = min(3, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols):
        ax = axes[i] if len(numeric_cols) > 1 else axes
        
        # Create histogram with KDE overlay
        df[col].hist(ax=ax, bins=20, alpha=0.7, density=True)
        df[col].plot.kde(ax=ax, color='red', linewidth=2)
        
        ax.set_title(f'Distribution of {col}', fontweight='bold')
        ax.set_xlabel(col)
        ax.set_ylabel('Density')
        ax.grid(True, alpha=0.3)
    
    # Hide empty subplots
    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    
    dist_path = output_dir / 'distributions.png'
    plt.savefig(dist_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Saved distribution plots: {dist_path}")
    return [str(dist_path)]

def create_scatter_plots(df, stats, output_dir):
    """Create scatter plots for strong correlations"""
    print("⚡ Creating scatter plots for correlations...")
    
    strong_corrs = stats.get('correlations', {}).get('strong_correlations', [])
    if not strong_corrs:
        print("   ⚠️ No strong correlations found for scatter plots")
        return []
    
    plot_paths = []
    
    # Limit to top 4 strongest correlations to avoid too many plots
    top_corrs = sorted(strong_corrs, key=lambda x: abs(x['correlation']), reverse=True)[:4]
    
    for i, corr in enumerate(top_corrs):
        plt.figure(figsize=(8, 6))
        
        var1, var2 = corr['variable1'], corr['variable2']
        correlation = corr['correlation']
        
        plt.scatter(df[var1], df[var2], alpha=0.6, s=50)
        
        # Add trend line
        z = np.polyfit(df[var1], df[var2], 1)
        p = np.poly1d(z)
        plt.plot(df[var1], p(df[var1]), "r--", alpha=0.8, linewidth=2)
        
        plt.xlabel(var1, fontsize=12)
        plt.ylabel(var2, fontsize=12)
        plt.title(f'{var1} vs {var2}\nCorrelation: {correlation:.3f} ({corr["strength"]})', 
                 fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        scatter_path = output_dir / f'scatter_{var1}_vs_{var2}.png'
        plt.savefig(scatter_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        plot_paths.append(str(scatter_path))
        print(f"   ✓ Saved scatter plot: {scatter_path}")
    
    return plot_paths

def create_categorical_plots(df, output_dir):
    """Create plots for categorical variables"""
    print("📊 Creating categorical analysis plots...")
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) == 0:
        print("   ⚠️ No categorical columns found")
        return []
    
    plot_paths = []
    
    for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
        plt.figure(figsize=(10, 6))
        
        value_counts = df[col].value_counts().head(10)  # Top 10 categories
        
        # Create bar plot
        ax = value_counts.plot(kind='bar', color='steelblue', alpha=0.8)
        plt.title(f'Distribution of {col}', fontsize=14, fontweight='bold')
        plt.xlabel(col, fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, v in enumerate(value_counts.values):
            ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        cat_path = output_dir / f'categorical_{col}.png'
        plt.savefig(cat_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        plot_paths.append(str(cat_path))
        print(f"   ✓ Saved categorical plot: {cat_path}")
    
    return plot_paths

def create_summary_dashboard(stats, output_dir):
    """Create an executive summary dashboard"""
    print("📋 Creating summary dashboard...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Variables overview
    desc_stats = stats['descriptive_statistics']
    variables = list(desc_stats.keys())
    means = [desc_stats[var]['mean'] for var in variables]
    
    ax1.bar(variables, means, color='lightblue', alpha=0.8)
    ax1.set_title('Mean Values by Variable', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Mean Value')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Correlation strength distribution
    strong_corrs = stats.get('correlations', {}).get('strong_correlations', [])
    if strong_corrs:
        corr_values = [abs(corr['correlation']) for corr in strong_corrs]
        ax2.hist(corr_values, bins=10, color='coral', alpha=0.7)
        ax2.set_title('Distribution of Strong Correlations', fontweight='bold', fontsize=12)
        ax2.set_xlabel('Absolute Correlation Value')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'No strong correlations\nfound', ha='center', va='center', 
                transform=ax2.transAxes, fontsize=12, alpha=0.7)
        ax2.set_title('Correlation Analysis', fontweight='bold', fontsize=12)
    
    # 3. Data quality overview
    patterns = stats.get('patterns', [])
    missing_pattern = next((p for p in patterns if p['type'] == 'missing_data'), None)
    
    if missing_pattern:
        columns = [col['column'] for col in missing_pattern['columns_with_missing']]
        percentages = [col['missing_percentage'] for col in missing_pattern['columns_with_missing']]
        ax3.bar(columns, percentages, color='orange', alpha=0.8)
        ax3.set_title('Missing Data by Column', fontweight='bold', fontsize=12)
        ax3.set_ylabel('Missing Percentage (%)')
        ax3.tick_params(axis='x', rotation=45)
    else:
        ax3.text(0.5, 0.5, 'No missing data\ndetected', ha='center', va='center', 
                transform=ax3.transAxes, fontsize=12, alpha=0.7)
        ax3.set_title('Data Quality Check', fontweight='bold', fontsize=12)
    
    # 4. Summary statistics
    summary_text = f"""
Analysis Summary:
• Variables analyzed: {len(desc_stats)}
• Strong correlations: {len(strong_corrs)}
• Patterns identified: {len(patterns)}
    """
    
    ax4.text(0.1, 0.5, summary_text, transform=ax4.transAxes, fontsize=12, 
             verticalalignment='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))
    ax4.set_title('Analysis Overview', fontweight='bold', fontsize=12)
    ax4.axis('off')
    
    plt.tight_layout()
    
    dashboard_path = output_dir / 'executive_dashboard.png'
    plt.savefig(dashboard_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Saved executive dashboard: {dashboard_path}")
    return str(dashboard_path)

def save_visualization_catalog(visualizations, output_path):
    """Save catalog of created visualizations"""
    print(f"📚 Saving visualization catalog...")
    
    catalog = {
        'visualizations_created': len(visualizations),
        'files': visualizations,
        'description': 'Catalog of all visualizations generated during analysis'
    }
    
    with open(output_path, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"   ✓ Saved visualization catalog: {output_path}")
    return catalog

def main():
    """Main visualization function"""
    if len(sys.argv) != 4:
        print("Usage: python visualizer.py <processed_json> <stats_json> <output_dir>")
        sys.exit(1)
    
    processed_path = sys.argv[1]
    stats_path = sys.argv[2]
    output_dir = Path(sys.argv[3])
    
    try:
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load data and statistics
        df, stats = load_data_and_stats(processed_path, stats_path)
        
        # Create visualizations
        all_visualizations = []
        
        # Correlation heatmap
        heatmap_path = create_correlation_heatmap(df, stats, output_dir)
        if heatmap_path:
            all_visualizations.append(heatmap_path)
        
        # Distribution plots
        dist_paths = create_distribution_plots(df, stats, output_dir)
        all_visualizations.extend(dist_paths)
        
        # Scatter plots
        scatter_paths = create_scatter_plots(df, stats, output_dir)
        all_visualizations.extend(scatter_paths)
        
        # Categorical plots
        cat_paths = create_categorical_plots(df, output_dir)
        all_visualizations.extend(cat_paths)
        
        # Summary dashboard
        dashboard_path = create_summary_dashboard(stats, output_dir)
        all_visualizations.append(dashboard_path)
        
        # Save catalog
        catalog_path = output_dir / 'visualization_catalog.json'
        catalog = save_visualization_catalog(all_visualizations, catalog_path)
        
        print(f"✅ Data visualization completed! Created {len(all_visualizations)} visualizations")
        return catalog
        
    except Exception as e:
        print(f"❌ Visualization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()