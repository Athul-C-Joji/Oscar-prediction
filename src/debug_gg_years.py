"""
Debug: Check year alignment between Oscar and Golden Globes
"""

import pandas as pd


def debug_years():
    """
    Check what years we have in each dataset
    """
    print("="*70)
    print("🔍 DEBUGGING YEAR ALIGNMENT")
    print("="*70)
    
    # Load datasets
    oscar_df = pd.read_csv('data/processed/best_picture_clean.csv')
    gg_df = pd.read_csv('data/external/golden_globes_1944_2024.csv')
    
    print("\n📊 OSCAR DATASET:")
    print(f"   Year range: {oscar_df['year_ceremony'].min()} - {oscar_df['year_ceremony'].max()}")
    print(f"   Column names: {list(oscar_df.columns)}")
    
    print("\n   Sample Oscar data (recent):")
    print(oscar_df[oscar_df['year_ceremony'] >= 2022][['year_ceremony', 'year_film', 'film', 'winner']].head(10).to_string(index=False))
    
    print("\n📊 GOLDEN GLOBES DATASET:")
    print(f"   Year range: {gg_df['year'].min()} - {gg_df['year'].max()}")
    print(f"   Column names: {list(gg_df.columns)}")
    
    print("\n   Sample GG data (recent):")
    print(gg_df[gg_df['year'] >= 2022][['year', 'film', 'category', 'winner']].head(10).to_string(index=False))
    
    # Check year alignment
    print("\n🔍 YEAR ALIGNMENT CHECK:")
    print("\n   How it SHOULD work:")
    print("   • Golden Globes 2024 (January 2024) → predicts Oscars 2024 (March 2024)")
    print("   • GG honors 2023 films → Oscars honor 2023 films")
    print("   • So: GG year = Oscar ceremony year (SAME year)")
    
    print("\n   Let's check a specific example:")
    print("   2024 Oscars (March 2024) - Winner should be Oppenheimer")
    
    oscar_2024 = oscar_df[oscar_df['year_ceremony'] == 2024]
    print(f"\n   Oscar 2024 nominees:")
    print(oscar_2024[['year_ceremony', 'film', 'winner']].to_string(index=False))
    
    gg_2024 = gg_df[gg_df['year'] == 2024]
    print(f"\n   Golden Globes 2024 nominees:")
    print(gg_2024[['year', 'film', 'category', 'winner']].head(10).to_string(index=False))
    
    # Try direct matching
    print("\n🔧 TRYING DIRECT MATCH (year_ceremony = gg_year):")
    
    oscar_films_2024 = set(oscar_2024['film'].str.lower().str.strip())
    gg_films_2024 = set(gg_2024['film'].str.lower().str.strip())
    
    print(f"\n   Oscar 2024 films: {oscar_films_2024}")
    print(f"\n   GG 2024 films: {gg_films_2024}")
    
    common = oscar_films_2024.intersection(gg_films_2024)
    print(f"\n   ✅ Common films: {common}")
    
    if len(common) == 0:
        print(f"\n   ❌ No exact matches! Titles are different.")
        print(f"\n   Let's check individual film names:")
        
        for oscar_film in list(oscar_films_2024)[:3]:
            print(f"\n   Oscar: '{oscar_film}'")
            for gg_film in list(gg_films_2024)[:5]:
                print(f"      vs GG: '{gg_film}'")


if __name__ == "__main__":
    debug_years()