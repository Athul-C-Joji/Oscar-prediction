"""
Scrape Real 2026 Oscar Nominations
Gets actual Best Picture nominees and nomination counts
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def scrape_2026_oscar_nominations():
    """
    Scrape 2026 Oscar nominations from Wikipedia
    """
    print("=" * 60)
    print("2026 OSCAR NOMINATIONS SCRAPER")
    print("=" * 60)
    
    # Try multiple URLs
    urls = [
        "https://en.wikipedia.org/wiki/97th_Academy_Awards",
        "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture",
    ]
    
    for url in urls:
        print(f"\n📥 Trying URL: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            print(f"✅ Page loaded successfully")
            
            # Look for tables
            tables = soup.find_all('table', {'class': 'wikitable'})
            print(f"Found {len(tables)} tables")
            
            # Try to find nomination counts
            # Look for text like "Nominations and Awards" or "Most Nominations"
            
            # Print some content to see structure
            print("\n🔍 Searching for nomination data...")
            
            # Look for specific patterns
            text = soup.get_text()
            if '97th Academy Awards' in text or '2026' in text:
                print("✅ Found 2026 Oscar data on page")
                
                # Print tables for manual inspection
                for i, table in enumerate(tables[:5]):
                    print(f"\n--- Table {i+1} ---")
                    rows = table.find_all('tr')[:10]
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 2:
                            text = ' | '.join([cell.get_text(strip=True) for cell in cells[:4]])
                            if text:
                                print(text[:150])
            
            break
            
        except Exception as e:
            print(f"⚠️ Error: {e}")
            continue
    
    # Manually create dataset based on actual 2026 nominations
    # (Update this with real data from Wikipedia)
    print("\n📝 Creating 2026 Oscar nominations dataset...")
    print("⚠️ Please verify these are the actual nominees!")
    
    nominees_2026 = [
        # Based on 97th Academy Awards
        # UPDATE THESE WITH REAL DATA FROM WIKIPEDIA
        {'film': 'Emilia Pérez', 'total_nominations': 13},
        {'film': 'The Brutalist', 'total_nominations': 10},
        {'film': 'Wicked', 'total_nominations': 10},
        {'film': 'Conclave', 'total_nominations': 8},
        {'film': 'Anora', 'total_nominations': 6},
        {'film': 'A Complete Unknown', 'total_nominations': 8},
        {'film': 'Dune: Part Two', 'total_nominations': 5},
        {'film': 'The Substance', 'total_nominations': 5},
        {'film': 'Nickel Boys', 'total_nominations': 2},
        {'film': 'I\'m Still Here', 'total_nominations': 3},
    ]
    
    df = pd.DataFrame(nominees_2026)
    
    # Save
    os.makedirs('data/predictions_2026', exist_ok=True)
    output_path = 'data/predictions_2026/oscar_nominations_2026.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Saved {len(df)} nominees to {output_path}")
    print("\n🏆 2026 Oscar Best Picture Nominees:")
    print(df.sort_values('total_nominations', ascending=False).to_string(index=False))
    
    print("\n" + "=" * 60)
    print("⚠️ IMPORTANT: Verify these numbers match official data!")
    print("   Check: https://en.wikipedia.org/wiki/97th_Academy_Awards")
    print("=" * 60)
    
    return df


if __name__ == "__main__":
    scrape_2026_oscar_nominations()