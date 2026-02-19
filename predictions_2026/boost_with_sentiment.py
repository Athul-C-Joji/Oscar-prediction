"""
Boost ALL Category Predictions with Sentiment Analysis
Applies sentiment boosts to technical categories
"""

import pandas as pd
import os


def normalize_probabilities(probs):
    """Normalize probabilities to sum to 1.0"""
    total = sum(probs)
    return [p / total for p in probs]


def boost_category_with_sentiment(category_file, sentiment_category, match_field='nominee'):
    """
    Boost a category's predictions using sentiment scores
    """
    pred_path = f'data/predictions_2026/{category_file}'
    
    if not os.path.exists(pred_path):
        return None
    
    # Load predictions
    df = pd.read_csv(pred_path)
    
    # Load sentiment
    sentiment_df = pd.read_csv('data/predictions_2026/sentiment_all_categories_2026.csv')
    
    # Filter sentiment for this category
    cat_sentiment = sentiment_df[sentiment_df['category'] == sentiment_category]
    
    if len(cat_sentiment) == 0:
        print(f"   ⚠️ No sentiment data for {sentiment_category}")
        return None
    
    print(f"\n📂 Updating {category_file}...")
    print(f"   Using sentiment from '{sentiment_category}' category")
    
    # Apply sentiment boost
    for idx, row in df.iterrows():
        film = row.get('film', '')
        
        # Find sentiment for this film
        film_sentiment = cat_sentiment[cat_sentiment['film'] == film]
        
        if len(film_sentiment) > 0:
            vader_score = film_sentiment.iloc[0]['avg_vader']
            
            # Calculate boost based on sentiment
            # Very Positive (>0.5) = 1.3x boost
            # Positive (0.2-0.5) = 1.15x boost
            # Neutral = 1.0x (no change)
            if vader_score > 0.5:
                boost = 1.3
            elif vader_score > 0.2:
                boost = 1.15
            else:
                boost = 1.0
            
            df.loc[idx, 'win_probability'] = df.loc[idx, 'win_probability'] * boost
            
            if boost > 1.0:
                print(f"   ✅ Boosted {film}: sentiment {vader_score:.3f} → {boost}x")
    
    # Normalize
    df['win_probability'] = normalize_probabilities(df['win_probability'].tolist())
    
    # Re-sort
    df = df.sort_values('win_probability', ascending=False)
    
    # Show top 3
    print(f"   📊 Updated top 3:")
    for i, row in df.head(3).iterrows():
        name = row.get(match_field, row.get('film', 'Unknown'))
        prob = row['win_probability']
        print(f"      {name}: {prob:.1%}")
    
    # Save
    df.to_csv(pred_path, index=False)
    
    return df


def boost_all_with_sentiment():
    """
    Apply sentiment boosts to ALL categories
    """
    print("="*70)
    print("🎬 BOOSTING ALL PREDICTIONS WITH SENTIMENT ANALYSIS")
    print("="*70)
    
    # Check if sentiment file exists
    if not os.path.exists('data/predictions_2026/sentiment_all_categories_2026.csv'):
        print("❌ Sentiment file not found! Run analyze_all_categories_2026.py first")
        return
    
    # Mapping: prediction file → sentiment category
    category_mappings = {
        # Main categories use 'general' sentiment
        'best_picture_predictions.csv': ('general', 'film'),
        'best_director_predictions.csv': ('general', 'nominee'),
        
        # Technical categories
        'best_cinematography_predictions.csv': ('cinematography', 'nominee'),
        'best_film_editing_predictions.csv': ('editing', 'nominee'),
        'best_production_design_predictions.csv': ('production_design', 'nominee'),
        'best_costume_design_predictions.csv': ('costume_design', 'nominee'),
        'best_makeup_and_hairstyling_predictions.csv': ('makeup', 'nominee'),
        'best_visual_effects_predictions.csv': ('vfx', 'nominee'),
        'best_sound_predictions.csv': ('sound', 'nominee'),
        'best_original_score_predictions.csv': ('score', 'nominee'),
    }
    
    updated_count = 0
    
    for pred_file, (sentiment_cat, match_field) in category_mappings.items():
        result = boost_category_with_sentiment(pred_file, sentiment_cat, match_field)
        if result is not None:
            updated_count += 1
    
    print(f"\n{'='*70}")
    print(f"✅ Updated {updated_count} categories with sentiment boosts!")
    print("="*70)
    
    # Create updated summary
    print("\n📊 FINAL PREDICTIONS WITH SENTIMENT:")
    
    summary = []
    
    for pred_file in category_mappings.keys():
        pred_path = f'data/predictions_2026/{pred_file}'
        if os.path.exists(pred_path):
            df = pd.read_csv(pred_path)
            if len(df) > 0:
                winner = df.iloc[0]
                cat_name = pred_file.replace('_predictions.csv', '').replace('_', ' ').title()
                winner_name = winner.get('nominee', winner.get('film', 'Unknown'))
                prob = winner['win_probability']
                
                summary.append({
                    'Category': cat_name,
                    'Winner': winner_name,
                    'Probability': f"{prob:.1%}"
                })
                
                print(f"\n🏆 {cat_name}")
                print(f"   → {winner_name} ({prob:.1%})")
    
    # Save summary
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv('data/predictions_2026/PREDICTIONS_WITH_SENTIMENT.csv', index=False)
    
    print(f"\n💾 Summary saved to: PREDICTIONS_WITH_SENTIMENT.csv")
    
    print("\n✅ COMPLETE!")
    print("\n💡 NEXT STEPS:")
    print("   1. Your predictions now include sentiment boosts!")
    print("   2. Wait for BAFTA (Feb 16) for even more accuracy")
    print("   3. Wait for SAG (Feb 23) for final predictions")
    print("   4. Optional: Add IMDb/RT ratings for additional boost")


if __name__ == "__main__":
    boost_all_with_sentiment()
    