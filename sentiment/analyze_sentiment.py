"""
Sentiment Analysis Script
Analyzes sentiment from movie reviews and social media
"""

import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os


def analyze_reviews_sentiment():
    """
    Analyze sentiment from sample movie reviews
    In production, you'd scrape from Twitter, Reddit, IMDb reviews
    """
    print("=" * 50)
    print("SENTIMENT ANALYSIS")
    print("=" * 50)
    
    print("\n📝 Creating sample reviews dataset...")
    
    # Sample reviews for 2024 Best Picture nominees
    reviews_data = [
        # Oppenheimer
        {'year': 2024, 'film': 'Oppenheimer', 'review': 'A masterpiece! Nolan delivers another brilliant film.'},
        {'year': 2024, 'film': 'Oppenheimer', 'review': 'Incredible performances and stunning cinematography.'},
        {'year': 2024, 'film': 'Oppenheimer', 'review': 'The best film of the year without question.'},
        {'year': 2024, 'film': 'Oppenheimer', 'review': 'Epic and thought-provoking. Absolutely phenomenal.'},
        
        # Poor Things
        {'year': 2024, 'film': 'Poor Things', 'review': 'Bizarre but beautifully made. Emma Stone is amazing.'},
        {'year': 2024, 'film': 'Poor Things', 'review': 'Visually stunning and wildly original.'},
        {'year': 2024, 'film': 'Poor Things', 'review': 'Not for everyone, but incredibly creative.'},
        
        # Barbie
        {'year': 2024, 'film': 'Barbie', 'review': 'Fun and surprisingly deep! Great entertainment.'},
        {'year': 2024, 'film': 'Barbie', 'review': 'Loved it! Funny, colorful, and meaningful.'},
        {'year': 2024, 'film': 'Barbie', 'review': 'A cultural phenomenon. Margot Robbie shines.'},
        
        # Killers of the Flower Moon
        {'year': 2024, 'film': 'Killers of the Flower Moon', 'review': 'Powerful storytelling by Scorsese.'},
        {'year': 2024, 'film': 'Killers of the Flower Moon', 'review': 'A bit long but worth watching.'},
        {'year': 2024, 'film': 'Killers of the Flower Moon', 'review': 'Important story that needed to be told.'},
        
        # The Holdovers
        {'year': 2024, 'film': 'The Holdovers', 'review': 'Heartwarming and beautifully acted.'},
        {'year': 2024, 'film': 'The Holdovers', 'review': 'A charming film with great characters.'},
        
        # Past Lives
        {'year': 2024, 'film': 'Past Lives', 'review': 'Emotionally devastating in the best way.'},
        {'year': 2024, 'film': 'Past Lives', 'review': 'Subtle, beautiful, and heartbreaking.'},
        
        # American Fiction
        {'year': 2024, 'film': 'American Fiction', 'review': 'Sharp, witty, and timely satire.'},
        {'year': 2024, 'film': 'American Fiction', 'review': 'Jeffrey Wright delivers an outstanding performance.'},
    ]
    
    df = pd.DataFrame(reviews_data)
    
    print(f"\n✅ Created {len(df)} sample reviews")
    
    # Initialize sentiment analyzers
    print("\n🤖 Analyzing sentiment with TextBlob and VADER...")
    vader = SentimentIntensityAnalyzer()
    
    # Analyze with TextBlob
    df['textblob_polarity'] = df['review'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['textblob_subjectivity'] = df['review'].apply(lambda x: TextBlob(x).sentiment.subjectivity)
    
    # Analyze with VADER
    df['vader_compound'] = df['review'].apply(lambda x: vader.polarity_scores(x)['compound'])
    df['vader_positive'] = df['review'].apply(lambda x: vader.polarity_scores(x)['pos'])
    df['vader_negative'] = df['review'].apply(lambda x: vader.polarity_scores(x)['neg'])
    
    # Classify sentiment
    df['sentiment_label'] = df['vader_compound'].apply(
        lambda x: 'Positive' if x > 0.05 else ('Negative' if x < -0.05 else 'Neutral')
    )
    
    # Aggregate by film
    print("\n📊 Aggregating sentiment by film...")
    film_sentiment = df.groupby(['year', 'film']).agg({
        'textblob_polarity': 'mean',
        'vader_compound': 'mean',
        'vader_positive': 'mean',
        'vader_negative': 'mean',
    }).reset_index()
    
    film_sentiment.columns = ['year', 'film', 'avg_textblob_sentiment', 
                              'avg_vader_sentiment', 'avg_positive_score', 'avg_negative_score']
    
    # Add sentiment category
    film_sentiment['sentiment_category'] = film_sentiment['avg_vader_sentiment'].apply(
        lambda x: 'Very Positive' if x > 0.5 else ('Positive' if x > 0.2 else ('Neutral' if x > -0.2 else 'Negative'))
    )
    
    # Save results
    os.makedirs('data/external', exist_ok=True)
    output_path = 'data/external/sentiment_scores.csv'
    film_sentiment.to_csv(output_path, index=False)
    
    print(f"\n✅ Saved sentiment analysis to {output_path}")
    
    # Display results
    print("\n📊 Sentiment Analysis Results:")
    print(film_sentiment.sort_values('avg_vader_sentiment', ascending=False).to_string(index=False))
    
    print("\n🎯 Top 3 most positively reviewed films:")
    top3 = film_sentiment.nlargest(3, 'avg_vader_sentiment')[['film', 'avg_vader_sentiment', 'sentiment_category']]
    print(top3.to_string(index=False))
    
    print("\n💡 Sentiment scores range from -1 (very negative) to +1 (very positive)")
    
    return film_sentiment


if __name__ == "__main__":
    analyze_reviews_sentiment()