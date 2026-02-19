"""
Multi-Category Sentiment Analysis for 2026 Oscars
Analyzes sentiment for ALL categories including technical
"""

import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os


# Sample reviews mentioning technical aspects
# In production, you'd scrape these from reviews, Twitter, Reddit
TECHNICAL_REVIEWS = {
    'Sinners': {
        'general': [
            'Ryan Coogler delivers a genre-defying masterpiece',
            'A bold and visually stunning achievement',
            'One of the year\'s most ambitious films',
        ],
        'cinematography': [
            'Autumn Durald Arkapaw\'s cinematography is breathtaking',
            'Every frame is meticulously composed',
            'The visual language is stunning and innovative',
        ],
        'editing': [
            'The editing keeps the tension at a fever pitch',
            'Michael Shawver\'s cutting is razor sharp',
            'Perfectly paced and tightly edited',
        ],
        'production_design': [
            'Hannah Beachler creates an immersive world',
            'The production design is extraordinary',
            'Every set feels lived-in and authentic',
        ],
        'sound': [
            'The sound design is immersive and powerful',
            'Audio work that puts you inside the story',
            'Exceptional sound mixing throughout',
        ],
        'score': [
            'Ludwig Göransson delivers another masterful score',
            'The music elevates every scene',
            'A haunting and memorable soundtrack',
        ],
        'vfx': [
            'Visual effects that blend seamlessly',
            'Stunning VFX work that serves the story',
            'Groundbreaking visual effects',
        ],
    },
    
    'Hamnet': {
        'general': [
            'Chloé Zhao crafts an intimate epic',
            'A powerful and moving adaptation',
            'Jessie Buckley gives the performance of the year',
        ],
        'cinematography': [
            'Gorgeous cinematography that captures emotion',
            'Visually poetic and stunning',
        ],
        'production_design': [
            'Period detail is impeccable',
            'Fiona Crombie\'s production design is masterful',
        ],
        'costume_design': [
            'The costumes are period-perfect and beautiful',
            'Exquisite costume work',
        ],
    },
    
    'Frankenstein': {
        'general': [
            'Guillermo del Toro\'s dark vision is stunning',
            'A gothic masterpiece',
        ],
        'cinematography': [
            'Dan Laustsen creates a moody, atmospheric world',
            'Dark and gorgeous cinematography',
        ],
        'production_design': [
            'Production design is hauntingly beautiful',
            'Gothic sets are extraordinary',
        ],
        'makeup': [
            'The creature makeup is phenomenal',
            'Prosthetics and makeup are Oscar-worthy',
        ],
    },
    
    'One Battle after Another': {
        'general': [
            'Paul Thomas Anderson at his most ambitious',
            'Epic filmmaking at its finest',
        ],
        'cinematography': [
            'Michael Bauman\'s work is stunning',
            'Beautifully shot and composed',
        ],
        'score': [
            'Jonny Greenwood delivers another brilliant score',
            'The music is haunting and powerful',
        ],
    },
    
    'Marty Supreme': {
        'general': [
            'Safdie brothers deliver another anxiety-inducing thriller',
            'Timothée Chalamet disappears into the role',
        ],
        'cinematography': [
            'Darius Khondji\'s cinematography is electric',
            'Visually dynamic and innovative',
        ],
        'editing': [
            'Frenetic editing that keeps you on edge',
            'Perfectly paced and propulsive',
        ],
    },
}


def analyze_category_sentiment(film, category, reviews):
    """
    Analyze sentiment for a specific category
    """
    if not reviews:
        return None
    
    vader = SentimentIntensityAnalyzer()
    
    sentiments = []
    
    for review in reviews:
        # TextBlob
        blob = TextBlob(review)
        tb_polarity = blob.sentiment.polarity
        
        # VADER
        vader_scores = vader.polarity_scores(review)
        vader_compound = vader_scores['compound']
        
        sentiments.append({
            'textblob': tb_polarity,
            'vader': vader_compound
        })
    
    # Calculate averages
    avg_textblob = sum(s['textblob'] for s in sentiments) / len(sentiments)
    avg_vader = sum(s['vader'] for s in sentiments) / len(sentiments)
    
    sentiment_label = 'Very Positive' if avg_vader > 0.5 else (
        'Positive' if avg_vader > 0.2 else (
            'Neutral' if avg_vader > -0.2 else 'Negative'
        )
    )
    
    return {
        'film': film,
        'category': category,
        'avg_textblob': avg_textblob,
        'avg_vader': avg_vader,
        'sentiment_label': sentiment_label,
        'num_reviews': len(reviews)
    }


def analyze_all_categories():
    """
    Perform sentiment analysis for all categories
    """
    print("="*70)
    print("🎬 COMPREHENSIVE SENTIMENT ANALYSIS - ALL CATEGORIES")
    print("="*70)
    
    all_results = []
    
    # Categories to analyze
    categories = [
        'general',
        'cinematography',
        'editing',
        'production_design',
        'costume_design',
        'makeup',
        'vfx',
        'sound',
        'score',
    ]
    
    for film, film_reviews in TECHNICAL_REVIEWS.items():
        print(f"\n{'='*70}")
        print(f"🎬 {film}")
        print('='*70)
        
        for category in categories:
            if category in film_reviews:
                result = analyze_category_sentiment(
                    film, 
                    category, 
                    film_reviews[category]
                )
                
                if result:
                    all_results.append(result)
                    print(f"\n📊 {category.replace('_', ' ').title()}")
                    print(f"   Sentiment: {result['avg_vader']:.3f} ({result['sentiment_label']})")
                    print(f"   Reviews: {result['num_reviews']}")
    
    # Create DataFrame
    df = pd.DataFrame(all_results)
    
    # Save
    os.makedirs('data/predictions_2026', exist_ok=True)
    output_path = 'data/predictions_2026/sentiment_all_categories_2026.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n{'='*70}")
    print(f"💾 Sentiment analysis saved to: {output_path}")
    
    # Summary by category
    print(f"\n{'='*70}")
    print("📊 SENTIMENT SUMMARY BY CATEGORY")
    print('='*70)
    
    for category in categories:
        cat_data = df[df['category'] == category]
        if len(cat_data) > 0:
            print(f"\n🎨 {category.replace('_', ' ').title()}:")
            top_films = cat_data.nlargest(3, 'avg_vader')
            for idx, row in top_films.iterrows():
                print(f"   {row['film']}: {row['avg_vader']:.3f} ({row['sentiment_label']})")
    
    print("\n💡 HOW TO IMPROVE THIS:")
    print("   1. Scrape professional reviews (IndieWire, Variety, THR)")
    print("   2. Search Twitter for '#FilmName cinematography'")
    print("   3. Analyze Reddit r/TrueFilm discussions")
    print("   4. Use YouTube video essay comments")
    print("   5. Scrape film Twitter accounts for technical praise")
    
    return df


if __name__ == "__main__":
    analyze_all_categories()