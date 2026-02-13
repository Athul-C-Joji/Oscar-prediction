"""
Debug script to check data coverage
"""

import pandas as pd

print("=" * 60)
print("DATA COVERAGE ANALYSIS")
print("=" * 60)

# Load master dataset
df = pd.read_csv('data/processed/master_dataset.csv')

print(f"\nTotal films: {len(df)}")

# Check precursor awards coverage
print("\n📊 PRECURSOR AWARDS COVERAGE:")
print(f"Films with GG Drama win: {df['won_gg_drama'].sum()}")
print(f"Films with GG Musical win: {df['won_gg_musical'].sum()}")
print(f"Films with BAFTA win: {df['won_bafta'].sum()}")
print(f"Films with SAG win: {df['won_sag_cast'].sum()}")
print(f"Films with ANY precursor data: {(df[['won_gg_drama', 'won_bafta', 'won_sag_cast']].notna().any(axis=1)).sum()}")

# Check by year
print("\n📅 COVERAGE BY YEAR:")
year_coverage = df.groupby('year_ceremony').agg({
    'won_bafta': lambda x: x.notna().sum(),
    'won_sag_cast': lambda x: x.notna().sum(),
    'imdb_rating': lambda x: x.notna().sum(),
    'film': 'count'
}).tail(10)
year_coverage.columns = ['Has BAFTA', 'Has SAG', 'Has Ratings', 'Total Films']
print(year_coverage)

# Films with complete precursor data
print("\n🎬 FILMS WITH COMPLETE PRECURSOR DATA:")
complete_precursor = df[
    df['won_bafta'].notna() & 
    df['won_sag_cast'].notna() &
    (df['won_gg_drama'].notna() | df['won_gg_musical'].notna())
][['year_ceremony', 'film', 'winner', 'won_bafta', 'won_sag_cast']]

print(f"Total: {len(complete_precursor)}")
print(complete_precursor.tail(20))

# Check what's missing
print("\n❓ MISSING DATA CHECK (2018-2024):")
recent = df[df['year_ceremony'] >= 2018][['year_ceremony', 'film', 'won_bafta', 'won_sag_cast', 'imdb_rating']]
print(recent.head(30))