"""
Smart Matching: Oscar Films with Golden Globes Dataset
CORRECTED version with proper year alignment
"""

import pandas as pd
import os


def smart_merge_golden_globes():
    """
    Intelligently merge Oscar and Golden Globes datasets
    """
    print("="*70)
    print("🔗 SMART MATCHING: OSCAR ↔ GOLDEN GLOBES")
    print("="*70)
    
    # Load datasets
    oscar_df = pd.read_csv('data/processed/best_picture_clean.csv')
    gg_df = pd.read_csv('data/external/golden_globes_1944_2024.csv')
    
    print(f"\n✅ Loaded {len(oscar_df)} Oscar films")
    print(f"✅ Loaded {len(gg_df)} Golden Globes films")
    
    # Normalize film names for matching
    oscar_df['film_normalized'] = oscar_df['film'].str.lower().str.strip()
    gg_df['film_normalized'] = gg_df['film'].str.lower().str.strip()
    
    # KEY FIX: GG year = Oscar ceremony year (SAME year, not +1!)
    gg_df['year_ceremony'] = gg_df['year']  # CORRECTED!
    
    print(f"\n🔍 Matching films by year and normalized title...")
    
    # Merge on year_ceremony and normalized film name
    merged = oscar_df.merge(
        gg_df[['year_ceremony', 'film_normalized', 'won_gg_drama', 'won_gg_musical']],
        on=['year_ceremony', 'film_normalized'],
        how='left'
    )
    
    # Fill NaN with 0 (films that weren't nominated for GG)
    merged['won_gg_drama'] = merged['won_gg_drama'].fillna(0).astype(int)
    merged['won_gg_musical'] = merged['won_gg_musical'].fillna(0).astype(int)
    
    # Count matches
    matched = merged[
        (merged['won_gg_drama'] > 0) | (merged['won_gg_musical'] > 0)
    ]
    
    # Drop the normalized column (don't need it anymore)
    merged = merged.drop(columns=['film_normalized'])
    
    print(f"✅ Matched {len(matched)} Oscar films with Golden Globes data")
    print(f"   Coverage: {len(matched)/len(oscar_df)*100:.1f}%")
    
    # Save
    output_path = 'data/processed/oscar_with_full_gg_matched.csv'
    merged.to_csv(output_path, index=False)
    
    print(f"\n💾 Saved to: {output_path}")
    
    # Statistics
    print(f"\n📊 MATCHING STATISTICS:")
    print(f"   Total Oscar films: {len(oscar_df)}")
    print(f"   Matched with GG: {len(matched)} ({len(matched)/len(oscar_df)*100:.1f}%)")
    print(f"   Has GG Drama win: {merged['won_gg_drama'].sum()}")
    print(f"   Has GG Musical win: {merged['won_gg_musical'].sum()}")
    
    # Show recent GG Drama winners
    print(f"\n📋 Recent GG Drama winners (2020-2024):")
    drama_winners = merged[
        (merged['year_ceremony'] >= 2020) & 
        (merged['won_gg_drama'] == 1)
    ][['year_ceremony', 'film', 'winner', 'won_gg_drama']]
    print(drama_winners.to_string(index=False))
    
    # Show recent GG Musical winners
    print(f"\n📋 Recent GG Musical/Comedy winners (2020-2024):")
    musical_winners = merged[
        (merged['year_ceremony'] >= 2020) & 
        (merged['won_gg_musical'] == 1)
    ][['year_ceremony', 'film', 'winner', 'won_gg_musical']]
    print(musical_winners.to_string(index=False))
    
    # Coverage by decade
    print(f"\n📈 Coverage by decade:")
    merged['decade'] = (merged['year_ceremony'] // 10) * 10
    decade_coverage = merged.groupby('decade').agg({
        'won_gg_drama': lambda x: (x > 0).sum(),
        'won_gg_musical': lambda x: (x > 0).sum(),
        'film': 'count'
    })
    decade_coverage.columns = ['GG Drama', 'GG Musical', 'Total Films']
    decade_coverage['Coverage %'] = ((decade_coverage['GG Drama'] + decade_coverage['GG Musical']) / decade_coverage['Total Films'] * 100).round(1)
    print(decade_coverage.tail(8))
    
    # Correlation analysis
    print(f"\n🎯 GG → OSCAR CORRELATION:")
    print(f"   GG Drama winners that won Oscar: {merged[(merged['won_gg_drama']==1) & (merged['winner']==1)].shape[0]}/{merged['won_gg_drama'].sum()}")
    print(f"   GG Musical winners that won Oscar: {merged[(merged['won_gg_musical']==1) & (merged['winner']==1)].shape[0]}/{merged['won_gg_musical'].sum()}")
    
    # Calculate win rates
    if merged['won_gg_drama'].sum() > 0:
        drama_win_rate = merged[(merged['won_gg_drama']==1) & (merged['winner']==1)].shape[0] / merged['won_gg_drama'].sum() * 100
        print(f"   📊 GG Drama → Oscar win rate: {drama_win_rate:.1f}%")
    
    if merged['won_gg_musical'].sum() > 0:
        musical_win_rate = merged[(merged['won_gg_musical']==1) & (merged['winner']==1)].shape[0] / merged['won_gg_musical'].sum() * 100
        print(f"   📊 GG Musical → Oscar win rate: {musical_win_rate:.1f}%")
    
    print(f"\n✅ SMART MATCHING COMPLETE!")
    print(f"\n💡 IMPACT:")
    print(f"   Before: {32} films with GG data (manual entry)")
    print(f"   After: {len(matched)} films with GG data (from full dataset)")
    print(f"   Increase: +{len(matched)-32} films! 🚀")
    
    return merged


if __name__ == "__main__":
    smart_merge_golden_globes()