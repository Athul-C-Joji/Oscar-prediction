"""
SAG Awards Scraper
Scrapes Screen Actors Guild Awards - Outstanding Performance by a Cast
"""

import pandas as pd
import os


def scrape_sag():
    """
    Create SAG Awards Best Cast dataset
    """
    print("=" * 50)
    print("SAG AWARDS SCRAPER")
    print("=" * 50)
    
    print("\n📝 Creating SAG Awards dataset...")
    
    # SAG Outstanding Performance by a Cast winners
    sag_data = [
        {'year': 2024, 'film': 'Oppenheimer', 'won_sag_cast': 1},
        {'year': 2024, 'film': 'American Fiction', 'won_sag_cast': 0},
        {'year': 2024, 'film': 'Barbie', 'won_sag_cast': 0},
        {'year': 2024, 'film': 'Killers of the Flower Moon', 'won_sag_cast': 0},
        {'year': 2024, 'film': 'The Color Purple', 'won_sag_cast': 0},
        
        {'year': 2023, 'film': 'Everything Everywhere All at Once', 'won_sag_cast': 1},
        {'year': 2023, 'film': 'The Banshees of Inisherin', 'won_sag_cast': 0},
        {'year': 2023, 'film': 'The Fabelmans', 'won_sag_cast': 0},
        {'year': 2023, 'film': 'Women Talking', 'won_sag_cast': 0},
        
        {'year': 2022, 'film': 'CODA', 'won_sag_cast': 1},
        {'year': 2022, 'film': 'Belfast', 'won_sag_cast': 0},
        {'year': 2022, 'film': 'Don\'t Look Up', 'won_sag_cast': 0},
        {'year': 2022, 'film': 'House of Gucci', 'won_sag_cast': 0},
        {'year': 2022, 'film': 'King Richard', 'won_sag_cast': 0},
        
        {'year': 2021, 'film': 'The Trial of the Chicago 7', 'won_sag_cast': 1},
        {'year': 2021, 'film': 'Ma Rainey\'s Black Bottom', 'won_sag_cast': 0},
        {'year': 2021, 'film': 'Minari', 'won_sag_cast': 0},
        {'year': 2021, 'film': 'One Night in Miami', 'won_sag_cast': 0},
        
        {'year': 2020, 'film': 'Parasite', 'won_sag_cast': 1},
        {'year': 2020, 'film': 'Bombshell', 'won_sag_cast': 0},
        {'year': 2020, 'film': 'The Irishman', 'won_sag_cast': 0},
        {'year': 2020, 'film': 'Jojo Rabbit', 'won_sag_cast': 0},
        {'year': 2020, 'film': 'Once Upon a Time in Hollywood', 'won_sag_cast': 0},
    ]
    
    df = pd.DataFrame(sag_data)
    
    # Save to data folder
    os.makedirs('data/external', exist_ok=True)
    output_path = 'data/external/sag_awards.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Saved {len(df)} records to {output_path}")
    print("\n📊 Sample data:")
    print(df.head(10))
    
    print("\n🎭 SAG Cast winners by year:")
    winners = df[df['won_sag_cast'] == 1][['year', 'film']]
    print(winners.to_string(index=False))
    
    print("\n💡 Fun fact: SAG Cast winner has strong correlation with Best Picture!")
    
    return df


if __name__ == "__main__":
    scrape_sag()