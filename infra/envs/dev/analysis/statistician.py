#!/usr/bin/env python3
"""
Statistical Analysis Component
Computes descriptive statistics, correlations, and identifies patterns
"""
import json
import sys
import pandas as pd
import numpy as np
from pathlib import Path

def load_processed_data(data_path):
    """Load processed JSON data"""
    print(f"📈 Loading processed data from: {data_path}")
    
    if not Path(data_path).exists():
        raise FileNotFoundError(f"Processed data file not found: {data_path}")
    
    with open(data_path, 'r') as f:
        data_dict = json.load(f)
    
    df = pd.DataFrame(data_dict['data'])
    metadata = data_dict['metadata']
    
    print(f"   ✓ Loaded {len(df)} rows for analysis")
    return df, metadata

def compute_descriptive_stats(df, numeric_cols):
    """Compute descriptive statistics for numeric columns"""
    print("📊 Computing descriptive statistics...")
    
    stats = {}
    for col in numeric_cols:
        stats[col] = {
            'count': int(df[col].count()),
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'std': float(df[col].std()),
            'min': float(df[col].min()),
            'max': float(df[col].max()),
            'q25': float(df[col].quantile(0.25)),
            'q75': float(df[col].quantile(0.75))
        }
    
    print(f"   ✓ Computed statistics for {len(numeric_cols)} numeric columns")
    return stats

def compute_correlations(df, numeric_cols):
    """Compute correlation matrix"""
    print("🔗 Computing correlation matrix...")
    
    if len(numeric_cols) < 2:
        return {}
    
    corr_matrix = df[numeric_cols].corr()
    
    # Convert to nested dict for JSON serialization
    correlations = {}
    for col1 in numeric_cols:
        correlations[col1] = {}
        for col2 in numeric_cols:
            correlations[col1][col2] = float(corr_matrix.loc[col1, col2])
    
    # Find strongest correlations (excluding self-correlations)
    strong_correlations = []
    for col1 in numeric_cols:
        for col2 in numeric_cols:
            if col1 != col2:
                corr_value = correlations[col1][col2]
                if abs(corr_value) > 0.5:  # Strong correlation threshold
                    strong_correlations.append({
                        'variable1': col1,
                        'variable2': col2,
                        'correlation': corr_value,
                        'strength': 'strong' if abs(corr_value) > 0.7 else 'moderate'
                    })
    
    print(f"   ✓ Found {len(strong_correlations)} strong correlations")
    return {
        'matrix': correlations,
        'strong_correlations': strong_correlations
    }

def identify_patterns(df, metadata):
    """Identify interesting patterns in the data"""
    print("🔍 Identifying data patterns...")
    
    patterns = []
    numeric_cols = metadata['numeric_columns']
    categorical_cols = metadata['categorical_columns']
    
    # Pattern 1: Categorical distribution
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        patterns.append({
            'type': 'categorical_distribution',
            'column': col,
            'unique_values': int(df[col].nunique()),
            'most_common': str(value_counts.index[0]),
            'most_common_count': int(value_counts.iloc[0]),
            'distribution': value_counts.head().to_dict()
        })
    
    # Pattern 2: Numeric ranges and outliers
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        
        patterns.append({
            'type': 'numeric_analysis',
            'column': col,
            'outliers_count': len(outliers),
            'outliers_percentage': round(len(outliers) / len(df) * 100, 2),
            'normal_range': f"{lower_bound:.2f} to {upper_bound:.2f}"
        })
    
    # Pattern 3: Missing data analysis
    missing_analysis = []
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            missing_analysis.append({
                'column': col,
                'missing_count': int(missing_count),
                'missing_percentage': round(missing_count / len(df) * 100, 2)
            })
    
    if missing_analysis:
        patterns.append({
            'type': 'missing_data',
            'columns_with_missing': missing_analysis
        })
    
    print(f"   ✓ Identified {len(patterns)} patterns")
    return patterns

def save_statistical_analysis(stats, correlations, patterns, output_path):
    """Save statistical analysis results"""
    print(f"💾 Saving statistical analysis to: {output_path}")
    
    analysis_results = {
        'descriptive_statistics': stats,
        'correlations': correlations,
        'patterns': patterns,
        'summary': {
            'variables_analyzed': len(stats),
            'strong_correlations_found': len(correlations.get('strong_correlations', [])),
            'patterns_identified': len(patterns)
        }
    }
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"   ✓ Saved statistical analysis results")
    return analysis_results

def main():
    """Main statistical analysis function"""
    if len(sys.argv) != 3:
        print("Usage: python statistician.py <processed_json> <output_json>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        # Load processed data
        df, metadata = load_processed_data(input_path)
        
        # Compute descriptive statistics
        stats = compute_descriptive_stats(df, metadata['numeric_columns'])
        
        # Compute correlations
        correlations = compute_correlations(df, metadata['numeric_columns'])
        
        # Identify patterns
        patterns = identify_patterns(df, metadata)
        
        # Save results
        results = save_statistical_analysis(stats, correlations, patterns, output_path)
        
        print("✅ Statistical analysis completed successfully!")
        return results
        
    except Exception as e:
        print(f"❌ Statistical analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()