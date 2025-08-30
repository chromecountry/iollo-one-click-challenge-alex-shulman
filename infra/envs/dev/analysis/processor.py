#!/usr/bin/env python3
"""
Data Processing Component
Loads, validates, and cleans data for analysis pipeline
"""
import pandas as pd
import json
import sys
from pathlib import Path

def load_and_validate_data(data_path):
    """Load CSV data and perform basic validation"""
    print(f"📊 Loading data from: {data_path}")
    
    if not Path(data_path).exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"   ✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Validate we have at least 2 numeric columns for meaningful analysis
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) < 2:
        raise ValueError(f"Need at least 2 numeric columns for analysis, found: {len(numeric_cols)}")
    
    print(f"   ✓ Found {len(numeric_cols)} numeric columns: {list(numeric_cols)}")
    return df

def clean_data(df):
    """Basic data cleaning operations"""
    print("🧹 Cleaning data...")
    
    initial_rows = len(df)
    
    # Remove rows with all NaN values
    df = df.dropna(how='all')
    
    # Basic outlier detection using IQR for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
        if outliers.sum() > 0:
            print(f"   ✓ Found {outliers.sum()} outliers in {col} (keeping for analysis)")
    
    print(f"   ✓ Cleaned data: {len(df)} rows (removed {initial_rows - len(df)} empty rows)")
    return df

def save_processed_data(df, output_path):
    """Save processed data as JSON"""
    print(f"💾 Saving processed data to: {output_path}")
    
    # Convert to JSON-serializable format
    data_dict = {
        'metadata': {
            'rows': len(df),
            'columns': len(df.columns),
            'numeric_columns': list(df.select_dtypes(include=['number']).columns),
            'categorical_columns': list(df.select_dtypes(include=['object']).columns)
        },
        'data': df.to_dict('records')
    }
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(data_dict, f, indent=2, default=str)
    
    print(f"   ✓ Saved {len(df)} records to JSON")
    return data_dict

def main():
    """Main processing function"""
    if len(sys.argv) != 3:
        print("Usage: python processor.py <input_csv> <output_json>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        # Load and validate data
        df = load_and_validate_data(input_path)
        
        # Clean data
        df_clean = clean_data(df)
        
        # Save processed data
        processed_data = save_processed_data(df_clean, output_path)
        
        print("✅ Data processing completed successfully!")
        return processed_data
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()