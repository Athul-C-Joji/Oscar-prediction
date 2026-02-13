"""
Master Data Integration Script
Combines Oscar data with all external sources:
- Golden Globes
- BAFTA
- SAG Awards
- Movie Ratings (IMDb, RT, Metacritic)
- Sentiment Analysis
"""

import pandas as pd
import os


def integrate_all_data():
    """
    Merge all data sources into one master dataset
    """
    print("=" * 60)
    print("MASTER DATA INTEGRATION")
    print("=" * 60)
    
    # --------------------------------------------------
    # 1️⃣ Load Base Oscar Data
    # --------------------------------------------------
    print("\n📂 Loading base Oscar data...")
    oscar_df = pd.read_csv('data/processed/best_picture_clean.csv')
    print(f"✅ Loaded {len(oscar_df)} Oscar records")
    
    # --------------------------------------------------
    # 2️⃣ Load External Data Sources
    # --------------------------------------------------
    print("\n📂 Loading external data sources...")
    
    # Golden Globes
    if os.path.exists('data/external/golden_globes.csv'):
        gg_df = pd.read_csv('data/external/golden_globes.csv')
        print(f"✅ Golden Globes: {len(gg_df)} records")
    else:
        print("⚠️ Golden Globes data not found")
        gg_df = pd.DataFrame()
    
    # BAFTA
    if os.path.exists('data/external/bafta.csv'):
        bafta_df = pd.read_csv('data/external/bafta.csv')
        print(f"✅ BAFTA: {len(bafta_df)} records")
    else:
        print("⚠️ BAFTA data not found")
        bafta_df = pd.DataFrame()
    
    # SAG Awards
    if os.path.exists('data/external/sag_awards.csv'):
        sag_df = pd.read_csv('data/external/sag_awards.csv')
        print(f"✅ SAG Awards: {len(sag_df)} records")
    else:
        print("⚠️ SAG Awards data not found")
        sag_df = pd.DataFrame()
    
    # Movie Ratings
    if os.path.exists('data/external/movie_ratings.csv'):
        ratings_df = pd.read_csv('data/external/movie_ratings.csv')
        print(f"✅ Movie Ratings: {len(ratings_df)} records")
    else:
        print("⚠️ Movie Ratings data not found")
        ratings_df = pd.DataFrame()
    
    # Sentiment Analysis
    if os.path.exists('data/external/sentiment_scores.csv'):
        sentiment_df = pd.read_csv('data/external/sentiment_scores.csv')
        print(f"✅ Sentiment Scores: {len(sentiment_df)} records")
    else:
        print("⚠️ Sentiment data not found")
        sentiment_df = pd.DataFrame()
    
    # --------------------------------------------------
    # 3️⃣ Merge All Data
    # --------------------------------------------------
    print("\n🔗 Merging all data sources...")
    
    # Start with Oscar data
    master_df = oscar_df.copy()
    
    # Merge Golden Globes
    if not gg_df.empty:
        master_df = master_df.merge(
            gg_df, 
            left_on=['year_ceremony', 'film'], 
            right_on=['year', 'film'],
            how='left',
            suffixes=('', '_gg')
        )
        master_df = master_df.drop('year_gg', axis=1, errors='ignore')
        master_df['won_gg_drama'] = master_df['won_gg_drama'].fillna(0)
        master_df['won_gg_musical'] = master_df['won_gg_musical'].fillna(0)
        print("✅ Merged Golden Globes")
    
    # Merge BAFTA
    if not bafta_df.empty:
        master_df = master_df.merge(
            bafta_df,
            left_on=['year_ceremony', 'film'],
            right_on=['year', 'film'],
            how='left',
            suffixes=('', '_bafta')
        )
        master_df = master_df.drop('year_bafta', axis=1, errors='ignore')
        master_df['won_bafta'] = master_df['won_bafta'].fillna(0)
        print("✅ Merged BAFTA")
    
    # Merge SAG
    if not sag_df.empty:
        master_df = master_df.merge(
            sag_df,
            left_on=['year_ceremony', 'film'],
            right_on=['year', 'film'],
            how='left',
            suffixes=('', '_sag')
        )
        master_df = master_df.drop('year_sag', axis=1, errors='ignore')
        master_df['won_sag_cast'] = master_df['won_sag_cast'].fillna(0)
        print("✅ Merged SAG Awards")
    
    # Merge Ratings
    if not ratings_df.empty:
        master_df = master_df.merge(
            ratings_df,
            left_on=['year_ceremony', 'film'],
            right_on=['year', 'film'],
            how='left',
            suffixes=('', '_ratings')
        )
        master_df = master_df.drop('year_ratings', axis=1, errors='ignore')
        print("✅ Merged Movie Ratings")
    
    # Merge Sentiment
    if not sentiment_df.empty:
        master_df = master_df.merge(
            sentiment_df,
            left_on=['year_ceremony', 'film'],
            right_on=['year', 'film'],
            how='left',
            suffixes=('', '_sentiment')
        )
        master_df = master_df.drop('year_sentiment', axis=1, errors='ignore')
        print("✅ Merged Sentiment Scores")
    
    # --------------------------------------------------
    # 4️⃣ Create New Features
    # --------------------------------------------------
    print("\n🔧 Engineering new features...")
    
    # Total precursor awards won
    master_df['total_precursor_wins'] = (
        master_df.get('won_gg_drama', 0) + 
        master_df.get('won_gg_musical', 0) + 
        master_df.get('won_bafta', 0) + 
        master_df.get('won_sag_cast', 0)
    )
    
    # Has any precursor win
    master_df['has_precursor_win'] = (master_df['total_precursor_wins'] > 0).astype(int)
    
    # Sweep indicator (won all 3 major precursors: GG, BAFTA, SAG)
    if all(col in master_df.columns for col in ['won_bafta', 'won_sag_cast']):
        master_df['precursor_sweep'] = (
            ((master_df.get('won_gg_drama', 0) == 1) | (master_df.get('won_gg_musical', 0) == 1)) &
            (master_df['won_bafta'] == 1) &
            (master_df['won_sag_cast'] == 1)
        ).astype(int)
    
    print("✅ Created precursor award features")
    
    # --------------------------------------------------
    # 5️⃣ Save Master Dataset
    # --------------------------------------------------
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/master_dataset.csv'
    master_df.to_csv(output_path, index=False)
    
    print(f"\n💾 Saved master dataset to {output_path}")
    print(f"✅ Total records: {len(master_df)}")
    print(f"✅ Total features: {len(master_df.columns)}")
    
    # --------------------------------------------------
    # 6️⃣ Show Summary
    # --------------------------------------------------
    print("\n📊 DATASET SUMMARY")
    print("=" * 60)
    print(f"Total Films: {len(master_df)}")
    print(f"Total Winners: {master_df['winner'].sum()}")
    print(f"Year Range: {master_df['year_ceremony'].min()} - {master_df['year_ceremony'].max()}")
    print(f"\nFeatures: {len(master_df.columns)}")
    print("\nAll columns:")
    for col in master_df.columns:
        print(f"  - {col}")
    
    print("\n🏆 Films with precursor sweeps (won GG + BAFTA + SAG):")
    if 'precursor_sweep' in master_df.columns:
        sweeps = master_df[master_df['precursor_sweep'] == 1][['year_ceremony', 'film', 'winner']]
        if len(sweeps) > 0:
            print(sweeps.to_string(index=False))
        else:
            print("  None in dataset")
    
    print("\n🔍 Sample of integrated data:")
    sample_cols = ['year_ceremony', 'film', 'winner', 'total_precursor_wins', 
                   'imdb_rating', 'avg_vader_sentiment']
    available_cols = [col for col in sample_cols if col in master_df.columns]
    print(master_df[available_cols].head(10).to_string(index=False))
    
    print("\n✅ INTEGRATION COMPLETE!")
    
    return master_df


if __name__ == "__main__":
    integrate_all_data()