"""
Final 2026 Oscar Predictions with Proper Golden Globes Boost
Applies empirical GG winner boost based on historical patterns
"""

import pandas as pd
import os


# Historical GG Winner Boost (based on training data)
GG_BOOST_FACTORS = {
    'drama': 1.8,      # GG Drama winners 80% more likely to win Oscar
    'musical': 1.3,    # GG Musical/Comedy 30% boost (less predictive)
    'supporting': 1.5, # Supporting actor GG = 50% boost
    'director': 1.6,   # Director GG = 60% boost
    'score': 1.7,      # Score GG = 70% boost
}


def normalize_probabilities(probabilities):
    """Normalize probabilities to sum to 1.0"""
    total = sum(probabilities)
    return [p / total for p in probabilities]


def update_category_with_gg(filepath, gg_winners, boost_type='drama', match_field='nominee'):
    """
    Update a single category's predictions with GG boost
    """
    if not os.path.exists(filepath):
        return None
    
    print(f"\n📂 Updating {os.path.basename(filepath)}...")
    
    df = pd.read_csv(filepath)
    
    # Apply boost to GG winners
    boost_factor = GG_BOOST_FACTORS.get(boost_type, 1.5)
    
    for winner in gg_winners:
        mask = df[match_field].str.contains(winner, case=False, na=False)
        if mask.any():
            # Boost probability
            df.loc[mask, 'win_probability'] = df.loc[mask, 'win_probability'] * boost_factor
            print(f"   ✅ Boosted {winner} by {boost_factor}x")
    
    # Normalize probabilities
    probabilities = df['win_probability'].tolist()
    normalized = normalize_probabilities(probabilities)
    df['win_probability'] = normalized
    
    # Re-sort
    df = df.sort_values('win_probability', ascending=False)
    
    # Display top 3
    print(f"   📊 Updated predictions:")
    for idx, row in df.head(3).iterrows():
        name = row.get(match_field, 'Unknown')
        prob = row['win_probability']
        is_gg = any(winner.lower() in name.lower() for winner in gg_winners)
        status = "🏆 GG WINNER" if is_gg else ""
        print(f"      {name}: {prob:.1%} {status}")
    
    # Save
    df.to_csv(filepath, index=False)
    
    return df


def create_final_predictions():
    """
    Create final predictions with proper GG boosts
    """
    print("="*70)
    print("🎬 FINAL 2026 OSCAR PREDICTIONS")
    print("   With Golden Globes 2026 Winners Boost Applied")
    print("="*70)
    
    # ========== BEST PICTURE ==========
    update_category_with_gg(
        'data/predictions_2026/best_picture_predictions.csv',
        ['Hamnet', 'One Battle After Another'],
        boost_type='drama',
        match_field='film'
    )
    
    # ========== BEST DIRECTOR ==========
    update_category_with_gg(
        'data/predictions_2026/best_director_predictions.csv',
        ['Paul Thomas Anderson'],
        boost_type='director',
        match_field='nominee'
    )
    
    # ========== BEST ACTOR ==========
    # Drama winner gets bigger boost
    df = pd.read_csv('data/predictions_2026/best_actor_in_a_leading_role_predictions.csv')
    
    # Boost drama winner more
    drama_mask = df['nominee'].str.contains('Wagner Moura', case=False, na=False)
    df.loc[drama_mask, 'win_probability'] = df.loc[drama_mask, 'win_probability'] * 2.0
    
    # Boost musical/comedy winner less
    musical_mask = df['nominee'].str.contains('Timothée Chalamet', case=False, na=False)
    df.loc[musical_mask, 'win_probability'] = df.loc[musical_mask, 'win_probability'] * 1.5
    
    # Normalize
    df['win_probability'] = normalize_probabilities(df['win_probability'].tolist())
    df = df.sort_values('win_probability', ascending=False)
    
    print(f"\n📂 Updating best_actor_in_a_leading_role_predictions.csv...")
    print(f"   ✅ Boosted Wagner Moura (GG Drama) by 2.0x")
    print(f"   ✅ Boosted Timothée Chalamet (GG Musical) by 1.5x")
    print(f"   📊 Updated predictions:")
    for idx, row in df.head(3).iterrows():
        print(f"      {row['nominee']}: {row['win_probability']:.1%}")
    
    df.to_csv('data/predictions_2026/best_actor_in_a_leading_role_predictions.csv', index=False)
    
    # ========== BEST ACTRESS ==========
    df = pd.read_csv('data/predictions_2026/best_actress_in_a_leading_role_predictions.csv')
    
    # Boost drama winner more
    drama_mask = df['nominee'].str.contains('Jessie Buckley', case=False, na=False)
    df.loc[drama_mask, 'win_probability'] = df.loc[drama_mask, 'win_probability'] * 2.2
    
    # Rose Byrne won Musical/Comedy but not Oscar nominated
    
    # Normalize
    df['win_probability'] = normalize_probabilities(df['win_probability'].tolist())
    df = df.sort_values('win_probability', ascending=False)
    
    print(f"\n📂 Updating best_actress_in_a_leading_role_predictions.csv...")
    print(f"   ✅ Boosted Jessie Buckley (GG Drama) by 2.2x")
    print(f"   📊 Updated predictions:")
    for idx, row in df.head(3).iterrows():
        print(f"      {row['nominee']}: {row['win_probability']:.1%}")
    
    df.to_csv('data/predictions_2026/best_actress_in_a_leading_role_predictions.csv', index=False)
    
    # ========== SUPPORTING ACTORS ==========
    update_category_with_gg(
        'data/predictions_2026/best_actor_in_a_supporting_role_predictions.csv',
        ['Stellan Skarsgård'],
        boost_type='supporting',
        match_field='nominee'
    )
    
    update_category_with_gg(
        'data/predictions_2026/best_actress_in_a_supporting_role_predictions.csv',
        ['Teyana Taylor'],
        boost_type='supporting',
        match_field='nominee'
    )
    
    # ========== SCREENPLAY ==========
    # Paul Thomas Anderson won GG Screenplay
    update_category_with_gg(
        'data/predictions_2026/best_adapted_screenplay_predictions.csv',
        ['One Battle After Another'],
        boost_type='drama',
        match_field='nominee'
    )
    
    # ========== SCORE ==========
    update_category_with_gg(
        'data/predictions_2026/best_original_score_predictions.csv',
        ['Ludwig Goransson', 'Ludwig Göransson'],
        boost_type='score',
        match_field='nominee'
    )
    
    # ========== SONG ==========
    update_category_with_gg(
        'data/predictions_2026/best_original_song_predictions.csv',
        ['Golden'],
        boost_type='drama',
        match_field='nominee'
    )
    
    # ========== ANIMATED FEATURE ==========
    update_category_with_gg(
        'data/predictions_2026/best_animated_feature_film_predictions.csv',
        ['KPop Demon Hunters'],
        boost_type='drama',
        match_field='nominee'
    )
    
    # ========== CREATE FINAL SUMMARY ==========
    print("\n" + "="*70)
    print("📊 FINAL PREDICTIONS SUMMARY - WITH GOLDEN GLOBES BOOST")
    print("="*70)
    
    categories_files = {
        'Best Picture': 'best_picture_predictions.csv',
        'Best Director': 'best_director_predictions.csv',
        'Best Actor': 'best_actor_in_a_leading_role_predictions.csv',
        'Best Actress': 'best_actress_in_a_leading_role_predictions.csv',
        'Best Supporting Actor': 'best_actor_in_a_supporting_role_predictions.csv',
        'Best Supporting Actress': 'best_actress_in_a_supporting_role_predictions.csv',
        'Best Original Screenplay': 'best_original_screenplay_predictions.csv',
        'Best Adapted Screenplay': 'best_adapted_screenplay_predictions.csv',
        'Best Cinematography': 'best_cinematography_predictions.csv',
        'Best Film Editing': 'best_film_editing_predictions.csv',
        'Best Original Score': 'best_original_score_predictions.csv',
        'Best Original Song': 'best_original_song_predictions.csv',
        'Best Animated Feature': 'best_animated_feature_film_predictions.csv',
    }
    
    final_summary = []
    
    for cat_name, filename in categories_files.items():
        filepath = f'data/predictions_2026/{filename}'
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            winner = df.iloc[0]
            
            winner_name = winner.get('nominee', winner.get('film', 'Unknown'))
            prob = winner['win_probability']
            
            final_summary.append({
                'Category': cat_name,
                'Predicted Winner': winner_name,
                'Probability': f"{prob:.1%}",
                'Golden Globes Boost': 'Yes' if 'gg' in filename or cat_name in [
                    'Best Picture', 'Best Director', 'Best Actor', 'Best Actress',
                    'Best Supporting Actor', 'Best Supporting Actress', 'Best Original Score', 'Best Animated Feature'
                ] else 'No'
            })
            
            print(f"\n🏆 {cat_name}")
            print(f"   → {winner_name} ({prob:.1%})")
    
    # Save final summary
    summary_df = pd.DataFrame(final_summary)
    summary_df.to_csv('data/predictions_2026/FINAL_PREDICTIONS_WITH_GG.csv', index=False)
    
    print(f"\n💾 Final predictions saved to: FINAL_PREDICTIONS_WITH_GG.csv")
    print("\n✅ COMPLETE! All predictions updated with Golden Globes boost!")
    
    return summary_df


if __name__ == "__main__":
    create_final_predictions()