"""
BAFTA Awards Scraper
Scrapes BAFTA Film Awards winners
"""

import pandas as pd
import os


def scrape_bafta():
    """
    Create BAFTA Best Film dataset
    """
    print("=" * 50)
    print("BAFTA AWARDS SCRAPER")
    print("=" * 50)
    
    print("\n📝 Creating BAFTA dataset...")
    
    # BAFTA Best Film winners (recent years)
    bafta_data = [
        {'year': 2024, 'film': 'Oppenheimer', 'won_bafta': 1},
        {'year': 2024, 'film': 'Poor Things', 'won_bafta': 0},
        {'year': 2024, 'film': 'Killers of the Flower Moon', 'won_bafta': 0},
        {'year': 2024, 'film': 'Anatomy of a Fall', 'won_bafta': 0},
        {'year': 2024, 'film': 'The Holdovers', 'won_bafta': 0},
        
        {'year': 2023, 'film': 'All Quiet on the Western Front', 'won_bafta': 1},
        {'year': 2023, 'film': 'Everything Everywhere All at Once', 'won_bafta': 0},
        {'year': 2023, 'film': 'The Banshees of Inisherin', 'won_bafta': 0},
        {'year': 2023, 'film': 'The Fabelmans', 'won_bafta': 0},
        
        {'year': 2022, 'film': 'The Power of the Dog', 'won_bafta': 1},
        {'year': 2022, 'film': 'Belfast', 'won_bafta': 0},
        {'year': 2022, 'film': 'Dune', 'won_bafta': 0},
        {'year': 2022, 'film': 'Don\'t Look Up', 'won_bafta': 0},
        
        {'year': 2021, 'film': 'Nomadland', 'won_bafta': 1},
        {'year': 2021, 'film': 'The Father', 'won_bafta': 0},
        {'year': 2021, 'film': 'Promising Young Woman', 'won_bafta': 0},
        
        {'year': 2020, 'film': '1917', 'won_bafta': 1},
        {'year': 2020, 'film': 'The Irishman', 'won_bafta': 0},
        {'year': 2020, 'film': 'Joker', 'won_bafta': 0},
        {'year': 2020, 'film': 'Once Upon a Time in Hollywood', 'won_bafta': 0},
    ]
    
    df = pd.DataFrame(bafta_data)
    
    # Save to data folder
    os.makedirs('data/external', exist_ok=True)
    output_path = 'data/external/bafta.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Saved {len(df)} records to {output_path}")
    print("\n📊 Sample data:")
    print(df.head(10))
    
    print("\n🏆 BAFTA winners by year:")
    winners = df[df['won_bafta'] == 1][['year', 'film']]
    print(winners.to_string(index=False))
    
    return df


if __name__ == "__main__":
    scrape_bafta()