"""
Data Preprocessing Script
Cleans and prepares Oscar data for machine learning
"""

import pandas as pd
import os

def preprocess_oscar_data():
    """
    Load and clean Oscar data
    Focus on Best Picture category
    """
    print("=" * 50)
    print("DATA PREPROCESSING")
    print("=" * 50)
    
    # Load raw data
    print("\n📂 Loading raw data...")
    df = pd.read_csv('data/raw/oscars.csv')
    print(f"✅ Loaded {len(df)} total records")
    print(f"📊 Columns: {list(df.columns)}")
    
    # Show first few rows to understand structure
    print("\n🔍 First 5 rows:")
    print(df.head())
    
    # Check for Best Picture category
    print("\n🎬 Categories in dataset:")
    print(df['category'].value_counts().head(10))
    
    # Filter for Best Picture only
    print("\n🎬 Filtering for Best Picture category...")
    df_bp = df[df['category'].str.contains('PICTURE', case=False, na=False)].copy()
    print(f"✅ Found {len(df_bp)} Best Picture nominations")
    
    # Check for missing values
    print("\n🔍 Checking for missing values...")
    missing = df_bp.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("✅ No missing values!")
    
    # Save processed data
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/best_picture_clean.csv'
    df_bp.to_csv(output_path, index=False)
    
    print(f"\n✅ Processed data saved to: {output_path}")
    print(f"✅ Final dataset: {len(df_bp)} records")
    
    # Show summary
    if 'winner' in df_bp.columns:
        print("\n📊 Summary:")
        print(f"   - Winners: {df_bp['winner'].sum()}")
        print(f"   - Non-winners: {len(df_bp) - df_bp['winner'].sum()}")
    
    print("\n✅ Preprocessing complete!")
    
    return df_bp

if __name__ == "__main__":
    preprocess_oscar_data()