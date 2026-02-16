"""
Update All Category Predictions with Golden Globes 2026 Winners
Adds GG win data to boost prediction accuracy
"""

import pandas as pd
import joblib
import os


# Golden Globes 2026 Winners (83rd Awards - January 11, 2026)
GOLDEN_GLOBES_WINNERS = {
    # ========== FILM ==========
    'Hamnet': {'category': 'Best Picture - Drama', 'type': 'drama'},
    'One Battle After Another': {'category': 'Best Picture - Musical/Comedy', 'type': 'musical'},
    
    # ========== DIRECTOR ==========
    'Paul Thomas Anderson': {'category': 'Best Director', 'film': 'One Battle After Another'},
    
    # ========== ACTING - DRAMA ==========
    'Wagner Moura': {'category': 'Best Actor - Drama', 'film': 'The Secret Agent'},
    'Jessie Buckley': {'category': 'Best Actress - Drama', 'film': 'Hamnet'},
    
    # ========== ACTING - MUSICAL/COMEDY ==========
    'Timothée Chalamet': {'category': 'Best Actor - Musical/Comedy', 'film': 'Marty Supreme'},
    'Rose Byrne': {'category': 'Best Actress - Musical/Comedy', 'film': 'If I Had Legs I\'d Kick You'},
    
    # ========== SUPPORTING ==========
    'Stellan Skarsgård': {'category': 'Best Supporting Actor', 'film': 'Sentimental Value'},
    'Teyana Taylor': {'category': 'Best Supporting Actress', 'film': 'One Battle After Another'},
    
    # ========== SCREENPLAY ==========
    'Paul Thomas Anderson_screenplay': {'category': 'Best Screenplay', 'film': 'One Battle After Another'},
    
    # ========== MUSIC ==========
    'Ludwig Göransson': {'category': 'Best Original Score', 'film': 'Sinners'},
    'Golden': {'category': 'Best Original Song', 'film': 'KPop Demon Hunters'},
    
    # ========== ANIMATED ==========
    'KPop Demon Hunters': {'category': 'Best Animated Feature', 'film': 'KPop Demon Hunters'},
}


def update_predictions_with_gg():
    """
    Re-run predictions with Golden Globes data added
    """
    print("="*70)
    print("🏆 UPDATING PREDICTIONS WITH GOLDEN GLOBES 2026 WINNERS")
    print("="*70)
    
    # Load model
    print("\n🤖 Loading model...")
    try:
        model = joblib.load('models/tier2_enhanced_model.pkl')
        print("✅ Model loaded")
    except:
        print("❌ Model not found!")
        return
    
    features = [
        'total_nominations',
        'nomination_share',
        'nom_ratio',
        'is_top_nominated',
        'nom_rank',
        'won_gg_drama',
        'won_gg_musical',
        'won_bafta',
        'won_sag_cast',
        'total_precursor_wins',
        'has_precursor_win',
        'precursor_sweep',
    ]
    
    # Categories to update
    categories_to_update = {
        'best_actor_in_a_leading_role_predictions.csv': {
            'gg_winners': ['Wagner Moura', 'Timothée Chalamet'],
            'match_field': 'nominee'
        },
        'best_actress_in_a_leading_role_predictions.csv': {
            'gg_winners': ['Jessie Buckley'],  # Add Musical/Comedy winner here
            'match_field': 'nominee'
        },
        'best_actor_in_a_supporting_role_predictions.csv': {
            'gg_winners': ['Stellan Skarsgård'],
            'match_field': 'nominee'
        },
        'best_actress_in_a_supporting_role_predictions.csv': {
            'gg_winners': ['Teyana Taylor'],
            'match_field': 'nominee'
        },
        'best_picture_predictions.csv': {
            'gg_winners': ['Hamnet', 'One Battle After Another'],
            'match_field': 'film'
        },
    }
    
    updated_count = 0
    
    for filename, config in categories_to_update.items():
        filepath = f'data/predictions_2026/{filename}'
        
        if not os.path.exists(filepath):
            print(f"⚠️ {filename} not found, skipping...")
            continue
        
        print(f"\n📂 Updating {filename}...")
        
        # Load predictions
        df = pd.read_csv(filepath)
        
        # Mark GG winners
        match_field = config['match_field']
        gg_winners = config['gg_winners']
        
        # Reset GG flags
        df['won_gg'] = 0
        
        # Mark winners
        for winner in gg_winners:
            mask = df[match_field].str.contains(winner, case=False, na=False)
            df.loc[mask, 'won_gg'] = 1
            if mask.any():
                print(f"   ✅ Marked {winner} as GG winner")
        
        # Update precursor features
        df['won_gg_drama'] = 0
        df['won_gg_musical'] = 0
        
        # Assign to drama or musical based on winner
        for winner in gg_winners:
            mask = df[match_field].str.contains(winner, case=False, na=False)
            if winner in ['Wagner Moura', 'Jessie Buckley', 'Hamnet']:
                df.loc[mask, 'won_gg_drama'] = 1
            elif winner in ['Timothée Chalamet', 'One Battle After Another']:
                df.loc[mask, 'won_gg_musical'] = 1
        
        # Recalculate total precursor wins
        df['total_precursor_wins'] = (
            df['won_gg_drama'] + 
            df['won_gg_musical'] + 
            df.get('won_bafta', 0) + 
            df.get('won_sag_cast', 0)
        )
        df['has_precursor_win'] = (df['total_precursor_wins'] > 0).astype(int)
        
        # Re-predict with updated features
        X = df[features]
        
        try:
            probabilities = model.predict_proba(X)[:, 1]
            df['win_probability'] = probabilities
        except Exception as e:
            print(f"   ⚠️ Prediction failed: {e}")
            continue
        
        # Sort by new probabilities
        df = df.sort_values('win_probability', ascending=False)
        
        # Save updated predictions
        df.to_csv(filepath, index=False)
        
        # Show top 3
        print(f"   📊 Updated predictions:")
        for idx, row in df.head(3).iterrows():
            name = row.get('nominee', row.get('film', 'Unknown'))
            prob = row['win_probability']
            gg_status = "🏆 GG WINNER" if row.get('won_gg', 0) == 1 else ""
            print(f"      {name}: {prob:.1%} {gg_status}")
        
        updated_count += 1
    
    print(f"\n✅ Updated {updated_count} category predictions with Golden Globes data!")
    
    # Create updated summary
    print("\n📊 Creating updated summary...")
    
    summary = []
    
    # Main categories
    main_cats = [
        ('Best Picture', 'best_picture_predictions.csv', 'film'),
        ('Best Director', 'best_director_predictions.csv', 'nominee'),
        ('Best Actor', 'best_actor_in_a_leading_role_predictions.csv', 'nominee'),
        ('Best Actress', 'best_actress_in_a_leading_role_predictions.csv', 'nominee'),
        ('Best Supporting Actor', 'best_actor_in_a_supporting_role_predictions.csv', 'nominee'),
        ('Best Supporting Actress', 'best_actress_in_a_supporting_role_predictions.csv', 'nominee'),
    ]
    
    print("\n🏆 UPDATED PREDICTIONS WITH GOLDEN GLOBES:")
    
    for cat_name, filename, field in main_cats:
        filepath = f'data/predictions_2026/{filename}'
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            winner = df.iloc[0]
            winner_name = winner[field]
            prob = winner['win_probability']
            
            print(f"\n{cat_name}:")
            print(f"   🥇 {winner_name} - {prob:.1%}")
            
            summary.append({
                'Category': cat_name,
                'Winner': winner_name,
                'Probability': f"{prob:.1%}",
                'Updated': 'Yes'
            })
    
    # Save summary
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv('data/predictions_2026/UPDATED_WITH_GG_SUMMARY.csv', index=False)
    
    print(f"\n💾 Summary saved to: UPDATED_WITH_GG_SUMMARY.csv")
    print("\n✅ ALL PREDICTIONS UPDATED WITH GOLDEN GLOBES DATA!")


if __name__ == "__main__":
    update_predictions_with_gg()