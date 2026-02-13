"""
Movie Ratings Scraper
Gets IMDb ratings and Rotten Tomatoes scores
"""

import pandas as pd
import os


def scrape_ratings():
    """
    Create movie ratings dataset (IMDb and Rotten Tomatoes)
    Note: In production, you'd use APIs like OMDb or scrape directly
    For now, we'll create sample data
    """
    print("=" * 50)
    print("MOVIE RATINGS SCRAPER")
    print("=" * 50)
    
    print("\n📝 Creating ratings dataset...")
    
    # Sample ratings data for recent Best Picture nominees
    ratings_data = [
        # 2024 nominees
        {'year': 2024, 'film': 'Oppenheimer', 'imdb_rating': 8.3, 'rt_critics': 93, 'rt_audience': 90, 'metacritic': 90},
        {'year': 2024, 'film': 'Poor Things', 'imdb_rating': 7.8, 'rt_critics': 92, 'rt_audience': 73, 'metacritic': 88},
        {'year': 2024, 'film': 'Killers of the Flower Moon', 'imdb_rating': 7.6, 'rt_critics': 93, 'rt_audience': 84, 'metacritic': 89},
        {'year': 2024, 'film': 'Barbie', 'imdb_rating': 6.8, 'rt_critics': 88, 'rt_audience': 83, 'metacritic': 80},
        {'year': 2024, 'film': 'Maestro', 'imdb_rating': 6.5, 'rt_critics': 81, 'rt_audience': 68, 'metacritic': 78},
        {'year': 2024, 'film': 'American Fiction', 'imdb_rating': 7.5, 'rt_critics': 93, 'rt_audience': 94, 'metacritic': 81},
        {'year': 2024, 'film': 'Anatomy of a Fall', 'imdb_rating': 7.7, 'rt_critics': 96, 'rt_audience': 90, 'metacritic': 87},
        {'year': 2024, 'film': 'The Holdovers', 'imdb_rating': 7.9, 'rt_critics': 97, 'rt_audience': 94, 'metacritic': 83},
        {'year': 2024, 'film': 'Past Lives', 'imdb_rating': 7.8, 'rt_critics': 95, 'rt_audience': 94, 'metacritic': 94},
        {'year': 2024, 'film': 'The Zone of Interest', 'imdb_rating': 7.4, 'rt_critics': 93, 'rt_audience': 78, 'metacritic': 89},
        
        # 2023 nominees
        {'year': 2023, 'film': 'Everything Everywhere All at Once', 'imdb_rating': 7.8, 'rt_critics': 95, 'rt_audience': 90, 'metacritic': 81},
        {'year': 2023, 'film': 'The Banshees of Inisherin', 'imdb_rating': 7.7, 'rt_critics': 96, 'rt_audience': 82, 'metacritic': 87},
        {'year': 2023, 'film': 'The Fabelmans', 'imdb_rating': 7.5, 'rt_critics': 92, 'rt_audience': 75, 'metacritic': 85},
        {'year': 2023, 'film': 'Tár', 'imdb_rating': 7.4, 'rt_critics': 91, 'rt_audience': 71, 'metacritic': 92},
        {'year': 2023, 'film': 'Top Gun: Maverick', 'imdb_rating': 8.2, 'rt_critics': 96, 'rt_audience': 99, 'metacritic': 78},
        {'year': 2023, 'film': 'All Quiet on the Western Front', 'imdb_rating': 7.7, 'rt_critics': 90, 'rt_audience': 90, 'metacritic': 76},
        
        # 2022 nominees
        {'year': 2022, 'film': 'CODA', 'imdb_rating': 8.0, 'rt_critics': 94, 'rt_audience': 91, 'metacritic': 72},
        {'year': 2022, 'film': 'Belfast', 'imdb_rating': 7.2, 'rt_critics': 85, 'rt_audience': 83, 'metacritic': 75},
        {'year': 2022, 'film': 'The Power of the Dog', 'imdb_rating': 6.8, 'rt_critics': 94, 'rt_audience': 55, 'metacritic': 88},
        {'year': 2022, 'film': 'Dune', 'imdb_rating': 8.0, 'rt_critics': 83, 'rt_audience': 90, 'metacritic': 74},
        {'year': 2022, 'film': 'Don\'t Look Up', 'imdb_rating': 7.2, 'rt_critics': 55, 'rt_audience': 77, 'metacritic': 55},
    ]
    
    df = pd.DataFrame(ratings_data)
    
    # Create combined score
    df['combined_score'] = (
        df['imdb_rating'] * 10 * 0.3 +  # Weight IMDb 30%
        df['rt_critics'] * 0.4 +         # Weight RT Critics 40%
        df['rt_audience'] * 0.2 +        # Weight RT Audience 20%
        df['metacritic'] * 0.1           # Weight Metacritic 10%
    )
    
    # Save to data folder
    os.makedirs('data/external', exist_ok=True)
    output_path = 'data/external/movie_ratings.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Saved {len(df)} records to {output_path}")
    print("\n📊 Top rated films:")
    top_rated = df.nlargest(10, 'combined_score')[['year', 'film', 'imdb_rating', 'rt_critics', 'combined_score']]
    print(top_rated.to_string(index=False))
    
    print("\n💡 Combined score = weighted average of all ratings")
    
    return df


if __name__ == "__main__":
    scrape_ratings()