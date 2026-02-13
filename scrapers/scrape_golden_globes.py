"""
Golden Globes Scraper
Scrapes Golden Globe winners from Wikipedia
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os


def scrape_golden_globes(start_year=2000, end_year=2024):
    """
    Scrape Golden Globe Best Motion Picture Drama winners
    """
    print("=" * 50)
    print("GOLDEN GLOBES SCRAPER")
    print("=" * 50)
    
    all_data = []
    
    for year in range(start_year, end_year + 1):
        print(f"\n📥 Scraping {year} Golden Globes...")
        
        # Golden Globes Wikipedia URL pattern
        url = f"https://en.wikipedia.org/wiki/{year}_Golden_Globe_Awards"
        
        try:
            # Add headers to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for tables with awards info
            tables = soup.find_all('table', {'class': 'wikitable'})
            
            # For now, collect basic info
            # We'll manually create a dataset based on known winners
            print(f"✅ Successfully accessed {year} page")
            
            time.sleep(1)  # Be polite, don't overwhelm the server
            
        except Exception as e:
            print(f"⚠️ Error scraping {year}: {e}")
            continue
    
    # For now, let's create a sample Golden Globes dataset manually
    # Later you can enhance the scraper to extract from tables
    
    print("\n📝 Creating Golden Globes dataset...")
    
    golden_globes_data = [
        # Format: year, film, won_gg_drama, won_gg_musical
        {'year': 2024, 'film': 'Oppenheimer', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2024, 'film': 'Poor Things', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2023, 'film': 'The Fabelmans', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2023, 'film': 'The Banshees of Inisherin', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2022, 'film': 'The Power of the Dog', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2022, 'film': 'West Side Story', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2021, 'film': 'Nomadland', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2021, 'film': 'Borat Subsequent Moviefilm', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2020, 'film': '1917', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2020, 'film': 'Once Upon a Time in Hollywood', 'won_gg_drama': 0, 'won_gg_musical': 1},
    ]
    
    df = pd.DataFrame(golden_globes_data)
    
    # Save to data folder
    os.makedirs('data/external', exist_ok=True)
    output_path = 'data/external/golden_globes.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Saved {len(df)} records to {output_path}")
    print("\n📊 Sample data:")
    print(df.head(10))
    
    print("\n💡 Note: This is a starter dataset.")
    print("   You can expand it by adding more years and categories.")
    
    return df


if __name__ == "__main__":
    scrape_golden_globes()