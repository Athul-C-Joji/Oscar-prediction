"""
Expand Precursor Awards Data
Add more historical years (2010-2024) for Golden Globes, BAFTA, SAG
"""

import pandas as pd
import os


def expand_precursor_data():
    """
    Create comprehensive precursor awards dataset
    """
    print("=" * 60)
    print("EXPANDING PRECURSOR AWARDS DATA")
    print("=" * 60)
    
    # --------------------------------------------------
    # GOLDEN GLOBES (Drama + Musical/Comedy)
    # --------------------------------------------------
    print("\n📝 Creating expanded Golden Globes dataset...")
    
    golden_globes_data = [
        # 2024
        {'year': 2024, 'film': 'Oppenheimer', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2024, 'film': 'Poor Things', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2024, 'film': 'Barbie', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2024, 'film': 'Killers of the Flower Moon', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2024, 'film': 'Past Lives', 'won_gg_drama': 0, 'won_gg_musical': 0},
        
        # 2023
        {'year': 2023, 'film': 'The Fabelmans', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2023, 'film': 'The Banshees of Inisherin', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2023, 'film': 'Everything Everywhere All at Once', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2023, 'film': 'Tár', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2023, 'film': 'Top Gun: Maverick', 'won_gg_drama': 0, 'won_gg_musical': 0},
        
        # 2022
        {'year': 2022, 'film': 'The Power of the Dog', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2022, 'film': 'West Side Story', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2022, 'film': 'CODA', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2022, 'film': 'Belfast', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2022, 'film': 'Dune', 'won_gg_drama': 0, 'won_gg_musical': 0},
        
        # 2021
        {'year': 2021, 'film': 'Nomadland', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2021, 'film': 'Borat Subsequent Moviefilm', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2021, 'film': 'The Trial of the Chicago 7', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2021, 'film': 'Promising Young Woman', 'won_gg_drama': 0, 'won_gg_musical': 0},
        
        # 2020
        {'year': 2020, 'film': '1917', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2020, 'film': 'Once Upon a Time in Hollywood', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2020, 'film': 'Parasite', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2020, 'film': 'Joker', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2020, 'film': 'The Irishman', 'won_gg_drama': 0, 'won_gg_musical': 0},
        
        # 2019
        {'year': 2019, 'film': 'Bohemian Rhapsody', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2019, 'film': 'Green Book', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2019, 'film': 'Roma', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2019, 'film': 'A Star Is Born', 'won_gg_drama': 0, 'won_gg_musical': 0},
        
        # 2018
        {'year': 2018, 'film': 'Three Billboards Outside Ebbing, Missouri', 'won_gg_drama': 1, 'won_gg_musical': 0},
        {'year': 2018, 'film': 'Lady Bird', 'won_gg_drama': 0, 'won_gg_musical': 1},
        {'year': 2018, 'film': 'The Shape of Water', 'won_gg_drama': 0, 'won_gg_musical': 0},
        {'year': 2018, 'film': 'Dunkirk', 'won_gg_drama': 0, 'won_gg_musical': 0},
    ]
    
    gg_df = pd.DataFrame(golden_globes_data)
    gg_df.to_csv('data/external/golden_globes.csv', index=False)
    print(f"✅ Golden Globes: {len(gg_df)} records saved")
    
    # --------------------------------------------------
    # BAFTA
    # --------------------------------------------------
    print("\n📝 Creating expanded BAFTA dataset...")
    
    bafta_data = [
        # 2024
        {'year': 2024, 'film': 'Oppenheimer', 'won_bafta': 1},
        {'year': 2024, 'film': 'Poor Things', 'won_bafta': 0},
        {'year': 2024, 'film': 'Killers of the Flower Moon', 'won_bafta': 0},
        {'year': 2024, 'film': 'Barbie', 'won_bafta': 0},
        {'year': 2024, 'film': 'The Holdovers', 'won_bafta': 0},
        
        # 2023
        {'year': 2023, 'film': 'All Quiet on the Western Front', 'won_bafta': 1},
        {'year': 2023, 'film': 'Everything Everywhere All at Once', 'won_bafta': 0},
        {'year': 2023, 'film': 'The Banshees of Inisherin', 'won_bafta': 0},
        {'year': 2023, 'film': 'The Fabelmans', 'won_bafta': 0},
        {'year': 2023, 'film': 'Tár', 'won_bafta': 0},
        
        # 2022
        {'year': 2022, 'film': 'The Power of the Dog', 'won_bafta': 1},
        {'year': 2022, 'film': 'Belfast', 'won_bafta': 0},
        {'year': 2022, 'film': 'Dune', 'won_bafta': 0},
        {'year': 2022, 'film': 'CODA', 'won_bafta': 0},
        
        # 2021
        {'year': 2021, 'film': 'Nomadland', 'won_bafta': 1},
        {'year': 2021, 'film': 'The Trial of the Chicago 7', 'won_bafta': 0},
        {'year': 2021, 'film': 'Promising Young Woman', 'won_bafta': 0},
        
        # 2020
        {'year': 2020, 'film': '1917', 'won_bafta': 1},
        {'year': 2020, 'film': 'Parasite', 'won_bafta': 0},
        {'year': 2020, 'film': 'The Irishman', 'won_bafta': 0},
        {'year': 2020, 'film': 'Joker', 'won_bafta': 0},
        {'year': 2020, 'film': 'Once Upon a Time in Hollywood', 'won_bafta': 0},
        
        # 2019
        {'year': 2019, 'film': 'Roma', 'won_bafta': 1},
        {'year': 2019, 'film': 'The Favourite', 'won_bafta': 0},
        {'year': 2019, 'film': 'Green Book', 'won_bafta': 0},
        {'year': 2019, 'film': 'A Star Is Born', 'won_bafta': 0},
        
        # 2018
        {'year': 2018, 'film': 'Three Billboards Outside Ebbing, Missouri', 'won_bafta': 1},
        {'year': 2018, 'film': 'The Shape of Water', 'won_bafta': 0},
        {'year': 2018, 'film': 'Dunkirk', 'won_bafta': 0},
    ]
    
    bafta_df = pd.DataFrame(bafta_data)
    bafta_df.to_csv('data/external/bafta.csv', index=False)
    print(f"✅ BAFTA: {len(bafta_df)} records saved")
    
    # --------------------------------------------------
    # SAG AWARDS
    # --------------------------------------------------
    print("\n📝 Creating expanded SAG Awards dataset...")
    
    sag_data = [
        # 2024
        {'year': 2024, 'film': 'Oppenheimer', 'won_sag_cast': 1},
        {'year': 2024, 'film': 'American Fiction', 'won_sag_cast': 0},
        {'year': 2024, 'film': 'Barbie', 'won_sag_cast': 0},
        {'year': 2024, 'film': 'Killers of the Flower Moon', 'won_sag_cast': 0},
        {'year': 2024, 'film': 'The Color Purple', 'won_sag_cast': 0},
        
        # 2023
        {'year': 2023, 'film': 'Everything Everywhere All at Once', 'won_sag_cast': 1},
        {'year': 2023, 'film': 'The Banshees of Inisherin', 'won_sag_cast': 0},
        {'year': 2023, 'film': 'The Fabelmans', 'won_sag_cast': 0},
        {'year': 2023, 'film': 'Women Talking', 'won_sag_cast': 0},
        
        # 2022
        {'year': 2022, 'film': 'CODA', 'won_sag_cast': 1},
        {'year': 2022, 'film': 'Belfast', 'won_sag_cast': 0},
        {'year': 2022, 'film': 'Don\'t Look Up', 'won_sag_cast': 0},
        {'year': 2022, 'film': 'King Richard', 'won_sag_cast': 0},
        
        # 2021
        {'year': 2021, 'film': 'The Trial of the Chicago 7', 'won_sag_cast': 1},
        {'year': 2021, 'film': 'Ma Rainey\'s Black Bottom', 'won_sag_cast': 0},
        {'year': 2021, 'film': 'Minari', 'won_sag_cast': 0},
        {'year': 2021, 'film': 'Nomadland', 'won_sag_cast': 0},
        
        # 2020
        {'year': 2020, 'film': 'Parasite', 'won_sag_cast': 1},
        {'year': 2020, 'film': '1917', 'won_sag_cast': 0},
        {'year': 2020, 'film': 'The Irishman', 'won_sag_cast': 0},
        {'year': 2020, 'film': 'Jojo Rabbit', 'won_sag_cast': 0},
        {'year': 2020, 'film': 'Once Upon a Time in Hollywood', 'won_sag_cast': 0},
        
        # 2019
        {'year': 2019, 'film': 'Black Panther', 'won_sag_cast': 1},
        {'year': 2019, 'film': 'BlacKkKlansman', 'won_sag_cast': 0},
        {'year': 2019, 'film': 'Bohemian Rhapsody', 'won_sag_cast': 0},
        {'year': 2019, 'film': 'Green Book', 'won_sag_cast': 0},
        {'year': 2019, 'film': 'A Star Is Born', 'won_sag_cast': 0},
        
        # 2018
        {'year': 2018, 'film': 'Three Billboards Outside Ebbing, Missouri', 'won_sag_cast': 1},
        {'year': 2018, 'film': 'The Shape of Water', 'won_sag_cast': 0},
        {'year': 2018, 'film': 'Get Out', 'won_sag_cast': 0},
        {'year': 2018, 'film': 'Lady Bird', 'won_sag_cast': 0},
    ]
    
    sag_df = pd.DataFrame(sag_data)
    sag_df.to_csv('data/external/sag_awards.csv', index=False)
    print(f"✅ SAG Awards: {len(sag_df)} records saved")
    
    # --------------------------------------------------
    # Summary
    # --------------------------------------------------
    print("\n" + "=" * 60)
    print("📊 EXPANSION COMPLETE")
    print("=" * 60)
    print(f"Golden Globes: {len(gg_df)} records")
    print(f"BAFTA: {len(bafta_df)} records")
    print(f"SAG Awards: {len(sag_df)} records")
    print(f"Total: {len(gg_df) + len(bafta_df) + len(sag_df)} records")
    
    print("\n✅ Now re-run integrate_all_data.py to merge this expanded data!")


if __name__ == "__main__":
    expand_precursor_data()