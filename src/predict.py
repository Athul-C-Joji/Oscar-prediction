"""
Prediction Script
Uses trained model to predict Oscar winners for new nominees
"""

import pandas as pd
import joblib
import os


def engineer_features(df):
    """
    Create the same features used during training
    """
    # Nomination ratio
    df['nom_ratio'] = df['total_nominations'] / df['year_total_nominations']
    
    # Is it the most nominated film that year?
    df['is_top_nominated'] = (df.groupby('year_ceremony')['total_nominations']
                               .transform('max') == df['total_nominations']).astype(int)
    
    # Nomination rank within year
    df['nom_rank'] = df.groupby('year_ceremony')['total_nominations'].rank(ascending=False, method='min')
    
    return df


def predict_winners(year=None):
    """
    Predict Oscar winners for a specific year
    """
    print("=" * 50)
    print("OSCAR WINNER PREDICTION")
    print("=" * 50)
    
    # Load model
    print("\n📂 Loading trained model...")
    if not os.path.exists("models/best_picture_model.pkl"):
        print("❌ Model not found! Please train the model first.")
        return
    
    model = joblib.load("models/best_picture_model.pkl")
    print("✅ Model loaded successfully!")
    
    # Load data
    print("\n📂 Loading nominee data...")
    df = pd.read_csv("data/processed/best_picture_clean.csv")
    
    # Filter by year if specified
    if year:
        df = df[df['year_ceremony'] == year]
        print(f"✅ Filtered for {year} ceremony")
    else:
        # Use most recent year
        year = df['year_ceremony'].max()
        df = df[df['year_ceremony'] == year]
        print(f"✅ Using most recent year: {year}")
    
    if len(df) == 0:
        print(f"❌ No nominees found for year {year}")
        return
    
    # Engineer features
    df = engineer_features(df)
    
    # Prepare features
    features = [
        'total_nominations',
        'nomination_share',
        'nom_ratio',
        'is_top_nominated',
        'nom_rank'
    ]
    
    X = df[features]
    
    # Make predictions
    print(f"\n🔮 Predicting winners for {year} ceremony...")
    probabilities = model.predict_proba(X)[:, 1]
    predictions = model.predict(X)
    
    # Create results dataframe
    results = df[['film', 'total_nominations', 'winner']].copy()
    results['win_probability'] = probabilities
    results['predicted_winner'] = predictions
    
    # Sort by probability
    results = results.sort_values('win_probability', ascending=False)
    
    # Display results
    print("\n" + "=" * 80)
    print(f"🎬 BEST PICTURE PREDICTIONS - {year} OSCARS")
    print("=" * 80)
    
    for idx, row in results.iterrows():
        film = row['film']
        prob = row['win_probability']
        noms = row['total_nominations']
        actual = "🏆 WINNER" if row['winner'] == 1 else ""
        predicted = "⭐ PREDICTED" if row['predicted_winner'] == 1 else ""
        
        print(f"\n{film}")
        print(f"  Win Probability: {prob:.1%}")
        print(f"  Total Nominations: {int(noms)}")
        if actual:
            print(f"  {actual}")
        if predicted:
            print(f"  {predicted}")
    
    print("\n" + "=" * 80)
    
    # Show top prediction
    top_film = results.iloc[0]['film']
    top_prob = results.iloc[0]['win_probability']
    actual_winner = results[results['winner'] == 1]['film'].values
    
    print(f"\n🎯 TOP PREDICTION: {top_film} ({top_prob:.1%} probability)")
    if len(actual_winner) > 0:
        print(f"🏆 ACTUAL WINNER: {actual_winner[0]}")
        if top_film == actual_winner[0]:
            print("✅ CORRECT PREDICTION!")
        else:
            print("❌ INCORRECT PREDICTION")
    
    return results


if __name__ == "__main__":
    # Predict for most recent year
    predict_winners()
    
    # Or predict for specific year:
    # predict_winners(year=2024)