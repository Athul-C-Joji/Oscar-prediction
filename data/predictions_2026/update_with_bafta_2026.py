"""
Update Predictions with BAFTA 2026 Winners
Apply BAFTA boost to all categories
"""

import pandas as pd
import os


# BAFTA 2026 Winners (February 16, 2026)
BAFTA_2026_WINNERS = {
    # Main Categories
    'Best Film': 'One Battle after Another',
    'Best Director': 'Paul Thomas Anderson',
    'Best Actor': 'Robert Aramayo',  # Not Oscar nominated (I Swear)
    'Best Actress': 'Jessie Buckley',
    'Best Supporting Actor': 'Sean Penn',
    'Best Supporting Actress': 'Wunmi Mosaku',
    
    # Screenplays
    'Best Original Screenplay': 'Sinners',
    'Best Adapted Screenplay': 'One Battle after Another',
    
    # Technical
    'Best Cinematography': 'One Battle after Another',
    'Best Editing': 'One Battle after Another',
    'Best Production Design': 'Frankenstein',
    'Best Costume Design': 'Frankenstein',
    'Best Makeup & Hair': 'Frankenstein',
    'Best Sound': 'F1',
    'Best Visual Effects': 'Avatar: Fire and Ash',
    'Best Original Score': 'Sinners',
}


def normalize_probabilities(probs):
    """Normalize probabilities to sum to 1.0"""
    total = sum(probs)
    return [p / total for p in probs]


def update_with_bafta():
    """
    Update ALL category predictions with BAFTA 2026 winners
    """
    print("="*70)
    print("🏆 UPDATING PREDICTIONS WITH BAFTA 2026 WINNERS")
    print("="*70)
    
    print("\n📋 BAFTA 2026 Winners:")
    print(f"   Best Film: One Battle after Another")
    print(f"   Best Director: Paul Thomas Anderson")
    print(f"   Best Actress: Jessie Buckley (Hamnet)")
    print(f"   Best Supporting Actress: Wunmi Mosaku (Sinners)")
    print(f"   + {len(BAFTA_2026_WINNERS)-4} more technical categories")
    
    # Category mappings: file → BAFTA category → match field
    category_updates = {
        'best_picture_predictions.csv': {
            'bafta_winner': 'One Battle after Another',
            'match_field': 'film',
            'boost': 2.5  # BAFTA Best Film is VERY predictive
        },
        'best_director_predictions.csv': {
            'bafta_winner': 'Paul Thomas Anderson',
            'match_field': 'nominee',
            'boost': 2.2
        },
        'best_actress_in_a_leading_role_predictions.csv': {
            'bafta_winner': 'Jessie Buckley',
            'match_field': 'nominee',
            'boost': 2.0
        },
        'best_actress_in_a_supporting_role_predictions.csv': {
            'bafta_winner': 'Wunmi Mosaku',
            'match_field': 'nominee',
            'boost': 1.8
        },
        'best_actor_in_a_supporting_role_predictions.csv': {
            'bafta_winner': 'Sean Penn',
            'match_field': 'nominee',
            'boost': 1.8
        },
        'best_original_screenplay_predictions.csv': {
            'bafta_winner': 'Sinners',
            'match_field': 'nominee',
            'boost': 2.0
        },
        'best_adapted_screenplay_predictions.csv': {
            'bafta_winner': 'One Battle after Another',
            'match_field': 'nominee',
            'boost': 2.0
        },
        'best_cinematography_predictions.csv': {
            'bafta_winner': 'One Battle after Another',
            'match_field': 'film',
            'boost': 2.0
        },
        'best_film_editing_predictions.csv': {
            'bafta_winner': 'One Battle after Another',
            'match_field': 'film',
            'boost': 2.0
        },
        'best_production_design_predictions.csv': {
            'bafta_winner': 'Frankenstein',
            'match_field': 'film',
            'boost': 2.0
        },
        'best_costume_design_predictions.csv': {
            'bafta_winner': 'Frankenstein',
            'match_field': 'film',
            'boost': 2.0
        },
        'best_makeup_and_hairstyling_predictions.csv': {
            'bafta_winner': 'Frankenstein',
            'match_field': 'film',
            'boost': 2.0
        },
        'best_sound_predictions.csv': {
            'bafta_winner': 'F1',
            'match_field': 'film',
            'boost': 1.8
        },
        'best_original_score_predictions.csv': {
            'bafta_winner': 'Sinners',
            'match_field': 'film',
            'boost': 2.0
        },
    }
    
    updated_count = 0
    results_summary = []
    
    for pred_file, config in category_updates.items():
        filepath = f'data/predictions_2026/{pred_file}'
        
        if not os.path.exists(filepath):
            continue
        
        cat_name = pred_file.replace('_predictions.csv', '').replace('_', ' ').title()
        
        print(f"\n📂 Updating: {cat_name}")
        
        df = pd.read_csv(filepath)
        
        bafta_winner = config['bafta_winner']
        match_field = config['match_field']
        boost = config['boost']
        
        # Find and boost BAFTA winner
        mask = df[match_field].str.contains(bafta_winner, case=False, na=False, regex=False)
        
        if mask.any():
            df.loc[mask, 'win_probability'] = df.loc[mask, 'win_probability'] * boost
            print(f"   ✅ Boosted '{bafta_winner}' by {boost}x")
        else:
            print(f"   ⚠️ BAFTA winner '{bafta_winner}' not found in nominees")
        
        # Normalize
        df['win_probability'] = normalize_probabilities(df['win_probability'].tolist())
        
        # Re-sort
        df = df.sort_values('win_probability', ascending=False)
        
        # Show top 3
        print(f"   📊 Updated top 3:")
        for i, row in df.head(3).iterrows():
            name = row.get(match_field, 'Unknown')
            prob = row['win_probability']
            is_bafta = bafta_winner.lower() in name.lower()
            status = "🏆 BAFTA" if is_bafta else ""
            print(f"      {name}: {prob:.1%} {status}")
        
        # Save
        df.to_csv(filepath, index=False)
        
        # Track results
        winner = df.iloc[0]
        results_summary.append({
            'Category': cat_name,
            'Winner': winner.get(match_field, 'Unknown'),
            'Probability': f"{winner['win_probability']:.1%}",
            'BAFTA Boost': 'Yes' if mask.any() else 'No'
        })
        
        updated_count += 1
    
    print(f"\n{'='*70}")
    print(f"✅ Updated {updated_count} categories with BAFTA boost!")
    print("="*70)
    
    # Final predictions summary
    print(f"\n🏆 FINAL PREDICTIONS WITH GG + BAFTA:")
    print("="*70)
    
    for result in results_summary[:10]:  # Show first 10
        print(f"\n{result['Category']}")
        print(f"   → {result['Winner']} ({result['Probability']})")
    
    # Save summary
    summary_df = pd.DataFrame(results_summary)
    summary_df.to_csv('data/predictions_2026/PREDICTIONS_WITH_GG_AND_BAFTA.csv', index=False)
    
    print(f"\n💾 Summary saved to: PREDICTIONS_WITH_GG_AND_BAFTA.csv")
    
    # Key insights
    print(f"\n📊 KEY INSIGHTS:")
    print(f"   🎬 Best Picture: MAJOR CHANGE!")
    print(f"      • One Battle after Another won BOTH GG Musical/Comedy AND BAFTA Best Film")
    print(f"      • This is a VERY strong signal (rare to win both)")
    print(f"      • Hamnet only won GG Drama (no BAFTA)")
    
    print(f"\n   🎯 PREDICTIONS NOW:")
    print(f"      Before BAFTA: Hamnet led with 39.6%")
    print(f"      After BAFTA: Check the updated predictions!")
    
    print(f"\n⏳ NEXT UPDATE:")
    print(f"   • SAG Awards (late February 2026)")
    print(f"   • SAG Cast winner will be the FINAL major indicator")
    
    return results_summary


if __name__ == "__main__":
    update_with_bafta()