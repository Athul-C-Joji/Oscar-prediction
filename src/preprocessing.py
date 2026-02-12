"""
Data Preprocessing Script
Cleans and prepares Oscar data for machine learning
"""

import pandas as pd
import os


def preprocess_oscar_data():
    """
    Load and clean Oscar data
    Focus on Best Picture category (1995–2024)
    """

    print("=" * 50)
    print("DATA PREPROCESSING")
    print("=" * 50)

    # --------------------------------------------------
    # 1️⃣ Load Raw Data
    # --------------------------------------------------
    print("\n📂 Loading raw data...")
    df = pd.read_csv('data/raw/oscars.csv')

    print(f"✅ Loaded {len(df)} total records")
    print(f"📊 Columns: {list(df.columns)}")

    # --------------------------------------------------
    # 2️⃣ Filter Modern Era (1995–2024)
    # --------------------------------------------------
    print("\n🗓️ Filtering data for modern era (1995–2024)...")

    df = df[(df['year_ceremony'] >= 1995) &
            (df['year_ceremony'] <= 2024)]

    print(f"✅ Records after year filtering: {len(df)}")

    # --------------------------------------------------
    # 3️⃣ Filter Best Picture Category
    # --------------------------------------------------
    print("\n🎬 Filtering for Best Picture category...")

    df_bp = df[df['category'].str.contains(
        'BEST PICTURE', case=False, na=False)].copy()

    print(f"✅ Found {len(df_bp)} Best Picture nominations")

    # --------------------------------------------------
    # 4️⃣ Convert Winner Column to Numeric
    # --------------------------------------------------
    print("\n🎯 Converting winner column to numeric (1 = Winner, 0 = Non-Winner)...")

    df_bp['winner'] = df_bp['winner'].astype(int)

    print("\n📊 Winner value counts:")
    print(df_bp['winner'].value_counts())

    # --------------------------------------------------
    # 5️⃣ Validate: One Winner Per Year
    # --------------------------------------------------
    print("\n📊 Winners per year check:")
    winners_per_year = df_bp.groupby('year_ceremony')['winner'].sum()
    print(winners_per_year.head())

    if all(winners_per_year == 1):
        print("✅ Validation passed: Exactly 1 winner per year")
    else:
        print("⚠️ Warning: Some years do not have exactly 1 winner")

    # --------------------------------------------------
    # 6️⃣ Save Processed Data
    # --------------------------------------------------
    os.makedirs('data/processed', exist_ok=True)

    output_path = 'data/processed/best_picture_clean.csv'
    df_bp.to_csv(output_path, index=False)

    print(f"\n✅ Processed data saved to: {output_path}")
    print(f"✅ Final dataset size: {len(df_bp)} records")

    print("\n✅ Preprocessing complete!")

    return df_bp


if __name__ == "__main__":
    preprocess_oscar_data()
