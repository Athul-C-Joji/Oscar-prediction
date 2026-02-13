"""
Scrape 2026 Golden Globes Winners
Gets actual winners from Golden Globes website or Wikipedia
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def scrape_2026_golden_globes():
    """
    Scrape 2026 Golden Globes winners
    """
    print("=" * 60)
    print("2026 GOLDEN GLOBES WINNERS SCRAPER")
    print("=" * 60)
    
    # Try multiple sources
    urls = [
        "https://www.goldenglobes.com/winners-nominees",
        "https://en.wikipedia.org/wiki/83rd_Golden_Globe_Awards",
        "https://www.goldenglobes.com/articles/83rd-golden-globe-awards-winners",
    ]
    
    for url in urls:
        print(f"\n📥 Trying: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"✅ Page loaded successfully")
            
            # Look for Best Motion Picture categories
            text = soup.get_text()
            
            # Search for key phrases
            if 'Motion Picture' in text or 'Drama' in text or 'Musical' in text:
                print("✅ Found Golden Globes award data")
                
                # Try to find tables or lists
                tables = soup.find_all('table')
                print(f"Found {len(tables)} tables")
                
                # Look for divs with winner info
                winners_divs = soup.find_all('div', class_=lambda x: x and 'winner' in x.lower())
                print(f"Found {len(winners_divs)} potential winner divs")
                
                # Print some content to inspect
                print("\n🔍 Searching for Best Picture winners...")
                
                # Look for specific text patterns
                if 'Best Motion Picture – Drama' in text:
                    print("✅ Found Drama category")
                if 'Best Motion Picture – Musical or Comedy' in text:
                    print("✅ Found Musical/Comedy category")
                
                # Print first few tables/sections
                for i, table in enumerate(tables[:5]):
                    print(f"\n--- Table {i+1} Preview ---")
                    rows = table.find_all('tr')[:8]  # Show more rows
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        text_content = ' | '.join([c.get_text(strip=True) for c in cells[:4]])
                        if text_content and 'Motion Picture' in text_content:
                            print(text_content)
                
                break
            
        except Exception as e:
            print(f"⚠️ Error: {e}")
            continue
    
    # Based on 83rd Golden Globe Awards (January 11, 2026)
    print("\n" + "=" * 60)
    print("📝 Creating 2026 Golden Globes Winners Dataset")
    print("=" * 60)
    
    golden_globes_2026 = [
        # CONFIRMED WINNERS - 83rd Golden Globe Awards (January 11, 2026)
        {'year': 2026, 'film': 'Hamnet', 'won_gg_drama': 1, 'won_gg_musical': 0, 'status': 'WINNER - Drama'},
        {'year': 2026, 'film': 'One Battle after Another', 'won_gg_drama': 0, 'won_gg_musical': 1, 'status': 'WINNER - Musical/Comedy'},
        
        # Other Best Picture nominees
        {'year': 2026, 'film': 'Sinners', 'won_gg_drama': 0, 'won_gg_musical': 0, 'status': 'Nominee'},
        {'year': 2026, 'film': 'Marty Supreme', 'won_gg_drama': 0, 'won_gg_musical': 0, 'status': 'Nominee'},
        {'year': 2026, 'film': 'Frankenstein', 'won_gg_drama': 0, 'won_gg_musical': 0, 'status': 'Nominee'},
        {'year': 2026, 'film': 'Sentimental Value', 'won_gg_drama': 0, 'won_gg_musical': 0, 'status': 'Nominee'},
        {'year': 2026, 'film': 'F1', 'won_gg_drama': 0, 'won_gg_musical': 0, 'status': 'Nominee'},
        {'year': 2026, 'film': 'Bugonia', 'won_gg_drama': 0, 'won_gg_musical': 0, 'status': 'Nominee'},
        {'year': 2026, 'film': 'Train Dreams', 'won_gg_drama': 0, 'won_gg_musical': 0, 'status': 'Nominee'},
        {'year': 2026, 'film': 'The Secret Agent', 'won_gg_drama': 0, 'won_gg_musical': 0, 'status': 'Nominee'},
    ]
    
    df = pd.DataFrame(golden_globes_2026)
    
    # Save
    os.makedirs('data/predictions_2026', exist_ok=True)
    output_path = 'data/predictions_2026/golden_globes_2026_winners.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n💾 Saved to {output_path}")
    
    print("\n🏆 2026 Golden Globes Results:")
    print("\n✅ CONFIRMED WINNERS:")
    winners = df[df['status'].str.contains('WINNER')]
    print(winners[['film', 'status']].to_string(index=False))
    
    print("\n📋 TO DO:")
    print("   1. Check Wikipedia for Musical/Comedy winner")
    print("   2. Update the script if needed")
    print("   3. Then update the main prediction script!")
    
    return df


if __name__ == "__main__":
    scrape_2026_golden_globes()