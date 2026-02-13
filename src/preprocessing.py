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
    # Create Total Nominations Per Film Feature
    # --------------------------------------------------
    print("\n🏆 Calculating total nominations per film...")

    # Count nominations per film per year
    nom_counts = (
        df.groupby(['year_ceremony', 'film'])
        .size()
        .reset_index(name='total_nominations')
    )

    # Merge nomination counts back to full dataset
    df = df.merge(
        nom_counts,
        on=['year_ceremony', 'film'],
        how='left'
    )

    print("✅ Total nominations feature added")


    # --------------------------------------------------
    # 3️⃣ Filter Best Picture Category
    # --------------------------------------------------
    print("\n🎬 Filtering for Best Picture category...")

    df_bp = df[df['category'].str.contains(
        'BEST PICTURE', case=False, na=False)].copy()

    print(f"✅ Found {len(df_bp)} Best Picture nominations")


    # --------------------------------------------------
    # Create Nomination Share Feature
    # --------------------------------------------------
    print("\n📊 Calculating nomination share per year...")

    # Total nominations among Best Picture nominees per year
    year_totals = (
        df_bp.groupby('year_ceremony')['total_nominations']
        .sum()
        .reset_index(name='year_total_nominations')
    )

    # Merge back
    df_bp = df_bp.merge(
        year_totals,
        on='year_ceremony',
        how='left'
    )

    # Calculate share
    df_bp['nomination_share'] = (
        df_bp['total_nominations'] /
        df_bp['year_total_nominations']
    )

    print("✅ Nomination share feature created")

    # --------------------------------------------------
    # Convert Winner Column to Numeric
    # --------------------------------------------------
    print("\n🎯 Converting winner column to numeric (1 = Winner, 0 = Non-Winner)...")
    df_bp['winner'] = df_bp['winner'].astype(int)

    print("\n📊 Winner value counts:")
    print(df_bp['winner'].value_counts())

    # --------------------------------------------------
    # Add Nomination Order Feature
    # --------------------------------------------------
    print("\n🔢 Creating nomination order feature...")

    # Sort properly first
    df_bp = df_bp.sort_values(by=['year_ceremony'])

    # Create nomination number within each year
    df_bp['nomination_number'] = (
        df_bp.groupby('year_ceremony')
            .cumcount() + 1
    )

    print("✅ Nomination order feature created")
    print(df_bp[['year_ceremony', 'nomination_number']].head())


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
