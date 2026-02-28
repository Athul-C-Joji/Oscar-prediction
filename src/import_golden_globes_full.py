"""
Import and Process Golden Globes Dataset (1944-2024)
Extracts Best Picture winners to enhance Oscar predictions
"""

import pandas as pd
import os


def import_golden_globes_full():
    """
    Import full Golden Globes dataset and extract relevant data
    """
    print("="*70)
    print("📥 IMPORTING GOLDEN GLOBES DATASET (1944-2024)")
    print("="*70)
    
    # Load the dataset
    filepath = 'data/raw/Golden_Globes_Awards_Dataset.csv'
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        print("Please copy Golden_Globes_Awards_Dataset.csv to data/raw/ folder")
        return None
    
    print(f"\n📂 Loading {filepath}...")
    df = pd.read_csv(filepath)
    
    print(f"✅ Loaded {len(df)} total records")
    print(f"   Years covered: {df['year'].min()} - {df['year'].max()}")
    
    # Show structure
    print(f"\n📊 Dataset structure:")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Nominee types: {df['nominee_type'].unique()}")
    
    # Filter for FILM Best Picture categories only
    print(f"\n🎬 Filtering for Best Picture awards...")
    
    # Best Picture - Drama and Musical/Comedy
    best_picture_awards = [
        'Best Motion Picture - Drama',
        'Best Motion Picture - Musical or Comedy',
        'Best Motion Picture â€" Drama',  # Handle encoding issues
        'Best Motion Picture â€" Musical or Comedy',
    ]
    
    # Filter
    bp_df = df[
        (df['nominee_type'] == 'film') & 
        (df['award'].isin(best_picture_awards))
    ].copy()
    
    print(f"✅ Found {len(bp_df)} Best Picture nominations (1944-2024)")
    
    # Standardize award names
    bp_df['award_clean'] = bp_df['award'].replace({
        'Best Motion Picture â€" Drama': 'Best Motion Picture - Drama',
        'Best Motion Picture â€" Musical or Comedy': 'Best Motion Picture - Musical or Comedy',
    })
    
    # Create separate columns for Drama vs Musical/Comedy
    bp_df['won_gg_drama'] = ((bp_df['award_clean'] == 'Best Motion Picture - Drama') & 
                              (bp_df['winner'] == True)).astype(int)
    
    bp_df['won_gg_musical'] = ((bp_df['award_clean'] == 'Best Motion Picture - Musical or Comedy') & 
                                (bp_df['winner'] == True)).astype(int)
    
    # Keep only relevant columns
    gg_processed = bp_df[[
        'year', 
        'title', 
        'award_clean', 
        'winner',
        'won_gg_drama',
        'won_gg_musical'
    ]].copy()
    
    gg_processed.columns = ['year', 'film', 'category', 'winner', 'won_gg_drama', 'won_gg_musical']
    
    # Show summary
    print(f"\n📊 Processed Golden Globes Data:")
    print(f"   Total films: {len(gg_processed)}")
    print(f"   Years: {gg_processed['year'].min()} - {gg_processed['year'].max()}")
    print(f"   Drama winners: {gg_processed['won_gg_drama'].sum()}")
    print(f"   Musical/Comedy winners: {gg_processed['won_gg_musical'].sum()}")
    
    # Save processed data
    output_path = 'data/external/golden_globes_1944_2024.csv'
    gg_processed.to_csv(output_path, index=False)
    
    print(f"\n💾 Saved to: {output_path}")
    
    # Show sample
    print(f"\n📋 Sample data (recent years):")
    print(gg_processed[gg_processed['year'] >= 2020].head(10).to_string(index=False))
    
    # Statistics by decade
    print(f"\n📈 Winners by decade:")
    gg_processed['decade'] = (gg_processed['year'] // 10) * 10
    decade_stats = gg_processed.groupby('decade').agg({
        'won_gg_drama': 'sum',
        'won_gg_musical': 'sum',
        'film': 'count'
    })
    decade_stats.columns = ['Drama Winners', 'Musical Winners', 'Total Films']
    print(decade_stats.tail(10))
    
    return gg_processed


def merge_with_oscar_data():
    """
    Merge Golden Globes data with Oscar dataset
    """
    print("\n" + "="*70)
    print("🔗 MERGING WITH OSCAR DATA")
    print("="*70)
    
    # Load Oscar data
    oscar_df = pd.read_csv('data/processed/best_picture_clean.csv')
    print(f"\n✅ Loaded {len(oscar_df)} Oscar records")
    
    # Load GG data
    gg_df = pd.read_csv('data/external/golden_globes_1944_2024.csv')
    print(f"✅ Loaded {len(gg_df)} Golden Globes records")
    
    # Merge on year and film title
    # Note: Film titles might not match exactly, need fuzzy matching
    
    print(f"\n🔧 Matching films by year and title...")
    
    # Create year_ceremony column in GG data (GG happens year before Oscars)
    gg_df['year_ceremony'] = gg_df['year'] + 1  # GG 2024 → Oscars 2025
    
    # Merge
    merged = oscar_df.merge(
        gg_df[['year_ceremony', 'film', 'won_gg_drama', 'won_gg_musical']],
        on=['year_ceremony', 'film'],
        how='left',
        suffixes=('', '_gg')
    )
    
    # Fill NaN with 0 (films that weren't nominated for GG)
    merged['won_gg_drama'] = merged['won_gg_drama'].fillna(0).astype(int)
    merged['won_gg_musical'] = merged['won_gg_musical'].fillna(0).astype(int)
    
    # Count matches
    matched = merged[
        (merged['won_gg_drama'] > 0) | (merged['won_gg_musical'] > 0)
    ]
    
    print(f"✅ Matched {len(matched)} Oscar films with Golden Globes data")
    print(f"   Coverage: {len(matched)/len(oscar_df)*100:.1f}%")
    
    # Show some matches
    print(f"\n📋 Recent matches:")
    recent_matches = matched[matched['year_ceremony'] >= 2020][[
        'year_ceremony', 'film', 'winner', 'won_gg_drama', 'won_gg_musical'
    ]]
    print(recent_matches.to_string(index=False))
    
    # Save
    output_path = 'data/processed/oscar_with_full_gg.csv'
    merged.to_csv(output_path, index=False)
    
    print(f"\n💾 Saved merged dataset to: {output_path}")
    
    print("\n📊 IMPACT ANALYSIS:")
    print(f"   Before: GG data for ~{32} films (2018-2024)")
    print(f"   After: GG data for ~{len(matched)} films (1944-2024)")
    print(f"   Increase: +{len(matched)-32} films with precursor data!")
    
    return merged


if __name__ == "__main__":
    # Import and process GG data
    gg_data = import_golden_globes_full()
    
    if gg_data is not None:
        # Merge with Oscar data
        merged_data = merge_with_oscar_data()
        
        print("\n" + "="*70)
        print("✅ IMPORT COMPLETE!")
        print("="*70)
        print("\n💡 NEXT STEPS:")
        print("   1. Re-run data integration with full GG data")
        print("   2. Retrain model with expanded dataset")
        print("   3. Compare old vs new predictions")