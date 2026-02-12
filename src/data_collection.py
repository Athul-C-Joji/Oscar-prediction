"""
Oscar Data Collection Script
Downloads historical Oscar data for analysis
"""

import pandas as pd
import os

def download_oscar_data():
    """
    Download Oscar nominees and winners data
    """
    print("=" * 50)
    print("OSCAR DATA COLLECTION")
    print("=" * 50)
    
    # Create data directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    
    print("\n📥 Downloading Oscar data...")
    
    # Try multiple sources
    urls = [
        "https://raw.githubusercontent.com/toddwschneider/oscars/master/data/nominees.csv",
        "https://github.com/chadwickbureau/boxball/raw/master/data/oscars.csv"
    ]
    
    df = None
    for url in urls:
        try:
            print(f"Trying: {url}")
            df = pd.read_csv(url)
            print("✅ Success!")
            break
        except:
            print("❌ Failed, trying next source...")
            continue
    
    if df is None:
        print("\n⚠️ Could not download from online sources.")
        print("Creating sample dataset instead...")
        
        # Create a sample dataset manually
        sample_data = {
            'year': [2024, 2024, 2024, 2023, 2023, 2023, 2022, 2022, 2022],
            'category': ['Best Picture', 'Best Picture', 'Best Picture', 
                        'Best Picture', 'Best Picture', 'Best Picture',
                        'Best Picture', 'Best Picture', 'Best Picture'],
            'film': ['Oppenheimer', 'Poor Things', 'Killers of the Flower Moon',
                    'Everything Everywhere All at Once', 'The Fabelmans', 'Tár',
                    'CODA', 'Belfast', 'The Power of the Dog'],
            'winner': [True, False, False, True, False, False, True, False, False]
        }
        df = pd.DataFrame(sample_data)
    
    # Save to our data folder
    output_path = 'data/raw/oscars.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Data saved to: {output_path}")
    print(f"✅ Total records: {len(df)}")
    print(f"\n📊 Columns: {list(df.columns)}")
    
    print("\n🔍 First 10 rows:")
    print(df.head(10))
    
    print("\n✅ Data collection complete!")
    return df

if __name__ == "__main__":
    download_oscar_data()