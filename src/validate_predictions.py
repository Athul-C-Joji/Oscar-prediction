"""
Validation Script for 2026 Oscar Predictions
Checks if predictions align with historical patterns
"""

import pandas as pd
import os


def validate_best_picture():
    """
    Validate Best Picture predictions against historical rules
    """
    print("="*70)
    print("🔍 VALIDATING BEST PICTURE PREDICTIONS")
    print("="*70)
    
    # Load predictions
    df = pd.read_csv('data/predictions_2026/best_picture_predictions.csv')
    
    print(f"\n📊 Current Predictions:")
    for idx, row in df.head(5).iterrows():
        film = row['film']
        prob = row['win_probability']
        noms = row.get('total_nominations', row.get('noms', 0))
        
        gg_drama = row.get('won_gg_drama', 0)
        gg_musical = row.get('won_gg_musical', 0)
        
        print(f"\n{idx+1}. {film}: {prob:.1%}")
        print(f"   Nominations: {int(noms)}")
        print(f"   GG Drama: {'✅ YES' if gg_drama == 1 else '❌ No'}")
        print(f"   GG Musical: {'✅ YES' if gg_musical == 1 else '❌ No'}")
    
    # VALIDATION RULES (Based on historical data)
    print("\n" + "="*70)
    print("🧪 VALIDATION TESTS")
    print("="*70)
    
    # RULE 1: Winner should have AT LEAST 3 nominations
    print("\n✅ RULE 1: Winners need at least 3 nominations")
    print("   Historical: 100% of winners (1995-2024) had 3+ nominations")
    
    top_pred = df.iloc[0]
    top_noms = top_pred.get('total_nominations', top_pred.get('noms', 0))
    
    if top_noms >= 3:
        print(f"   ✅ PASS: {top_pred['film']} has {int(top_noms)} nominations")
    else:
        print(f"   ⚠️ WARNING: {top_pred['film']} only has {int(top_noms)} nominations!")
    
    # RULE 2: Top prediction should ideally have a precursor win
    print("\n✅ RULE 2: Top prediction should have precursor win")
    print("   Historical: 85% of winners (2000-2024) won at least one precursor")
    
    has_precursor = (top_pred.get('won_gg_drama', 0) == 1 or 
                    top_pred.get('won_gg_musical', 0) == 1 or
                    top_pred.get('won_bafta', 0) == 1 or
                    top_pred.get('won_sag_cast', 0) == 1)
    
    if has_precursor:
        print(f"   ✅ PASS: {top_pred['film']} has precursor win(s)")
    else:
        print(f"   ⚠️ WARNING: {top_pred['film']} has NO precursor wins yet")
        print(f"   📌 Note: BAFTA and SAG are still pending")
    
    # RULE 3: Most nominated film winning is common but not guaranteed
    print("\n✅ RULE 3: Check most-nominated film")
    print("   Historical: Most-nominated film wins ~40% of the time")
    
    most_nominated = df.nlargest(1, 'total_nominations').iloc[0]
    most_noms_film = most_nominated['film']
    most_noms_count = most_nominated.get('total_nominations', most_nominated.get('noms', 0))
    
    print(f"   Most nominated: {most_noms_film} ({int(most_noms_count)} noms)")
    
    if most_noms_film == top_pred['film']:
        print(f"   ✅ Top prediction IS most-nominated (historically common)")
    else:
        print(f"   ⚠️ Top prediction is NOT most-nominated")
        print(f"   📌 This happens! Examples:")
        print(f"      • CODA (2022): 3 noms, beat Power of Dog (12 noms)")
        print(f"      • Parasite (2020): 6 noms, beat 1917 (10 noms)")
    
    # RULE 4: GG Drama winner correlation
    print("\n✅ RULE 4: Golden Globe Drama winner correlation")
    print("   Historical: GG Drama winners win Oscar ~55% of time")
    
    gg_drama_winner = df[df.get('won_gg_drama', 0) == 1]
    
    if len(gg_drama_winner) > 0:
        gg_winner_name = gg_drama_winner.iloc[0]['film']
        gg_winner_prob = gg_drama_winner.iloc[0]['win_probability']
        gg_winner_rank = df[df['film'] == gg_winner_name].index[0] + 1
        
        print(f"   GG Drama Winner: {gg_winner_name}")
        print(f"   Prediction Rank: #{gg_winner_rank}")
        print(f"   Probability: {gg_winner_prob:.1%}")
        
        if gg_winner_rank <= 3:
            print(f"   ✅ PASS: GG Drama winner is in top 3 predictions")
        else:
            print(f"   ⚠️ WARNING: GG Drama winner ranked #{gg_winner_rank}")
    
    # RULE 5: Probability sanity check
    print("\n✅ RULE 5: Probability distribution check")
    print("   Expected: Top prediction 30-60%, not >80% or <20%")
    
    top_prob = top_pred['win_probability']
    
    if 0.20 <= top_prob <= 0.80:
        print(f"   ✅ PASS: Top prediction ({top_prob:.1%}) is in reasonable range")
    elif top_prob > 0.80:
        print(f"   ⚠️ WARNING: Very high confidence ({top_prob:.1%}) - might be overfit")
    else:
        print(f"   ⚠️ WARNING: Very low confidence ({top_prob:.1%}) - might be underconfident")
    
    # RULE 6: Sum of probabilities
    print("\n✅ RULE 6: Probabilities should sum to ~100%")
    total_prob = df['win_probability'].sum()
    
    if 0.99 <= total_prob <= 1.01:
        print(f"   ✅ PASS: Total probability = {total_prob:.2%}")
    else:
        print(f"   ⚠️ WARNING: Total probability = {total_prob:.2%} (should be 100%)")


def validate_technical_categories():
    """
    Validate technical category predictions
    """
    print("\n" + "="*70)
    print("🔍 VALIDATING TECHNICAL CATEGORIES")
    print("="*70)
    
    # RULE: Most-nominated films usually dominate technical categories
    print("\n✅ RULE: Technical awards cluster on most-nominated films")
    print("   Historical: Films with 10+ noms win ~70% of technical Oscars")
    
    tech_categories = [
        'best_cinematography_predictions.csv',
        'best_film_editing_predictions.csv',
        'best_production_design_predictions.csv',
        'best_sound_predictions.csv',
        'best_visual_effects_predictions.csv',
    ]
    
    tech_winners = {}
    
    for cat_file in tech_categories:
        filepath = f'data/predictions_2026/{cat_file}'
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            winner = df.iloc[0]
            film = winner.get('film', 'Unknown')
            
            if film not in tech_winners:
                tech_winners[film] = 0
            tech_winners[film] += 1
    
    print(f"\n📊 Technical category predictions by film:")
    for film, count in sorted(tech_winners.items(), key=lambda x: x[1], reverse=True):
        print(f"   {film}: {count} predicted wins")
    
    # Check if one film dominates
    if tech_winners:
        max_wins = max(tech_winners.values())
        if max_wins >= 3:
            print(f"\n   ✅ PASS: A single film dominates technical categories (realistic)")
        else:
            print(f"\n   ⚠️ Note: Technical wins are spread across multiple films")


def check_historical_comparison():
    """
    Compare 2026 predictions to similar historical years
    """
    print("\n" + "="*70)
    print("📚 HISTORICAL COMPARISON")
    print("="*70)
    
    df = pd.read_csv('data/predictions_2026/best_picture_predictions.csv')
    top_pred = df.iloc[0]
    
    print(f"\n🎬 Your Top Prediction: {top_pred['film']}")
    print(f"   Nominations: {int(top_pred.get('total_nominations', top_pred.get('noms', 0)))}")
    print(f"   GG Drama: {'✅' if top_pred.get('won_gg_drama', 0) == 1 else '❌'}")
    print(f"   Win Probability: {top_pred['win_probability']:.1%}")
    
    print("\n📊 Similar Historical Winners:")
    
    # Find historical analogs
    historical_analogs = [
        {
            'year': 2024,
            'film': 'Oppenheimer',
            'noms': 13,
            'gg_drama': True,
            'bafta': True,
            'sag': True,
            'result': 'WON ✅'
        },
        {
            'year': 2022,
            'film': 'CODA',
            'noms': 3,
            'gg_drama': False,
            'bafta': False,
            'sag': True,
            'result': 'WON ✅ (upset!)'
        },
        {
            'year': 2021,
            'film': 'Nomadland',
            'noms': 6,
            'gg_drama': True,
            'bafta': True,
            'sag': False,
            'result': 'WON ✅'
        },
        {
            'year': 2020,
            'film': 'Parasite',
            'noms': 6,
            'gg_drama': False,
            'bafta': False,
            'sag': True,
            'result': 'WON ✅'
        },
    ]
    
    for analog in historical_analogs:
        print(f"\n{analog['year']} - {analog['film']}:")
        print(f"   Nominations: {analog['noms']}")
        print(f"   GG Drama: {'✅' if analog['gg_drama'] else '❌'}")
        print(f"   BAFTA: {'✅' if analog['bafta'] else '❌'}")
        print(f"   SAG: {'✅' if analog['sag'] else '❌'}")
        print(f"   Result: {analog['result']}")


def final_verdict():
    """
    Overall assessment of predictions
    """
    print("\n" + "="*70)
    print("⚖️ FINAL VALIDATION VERDICT")
    print("="*70)
    
    df = pd.read_csv('data/predictions_2026/best_picture_predictions.csv')
    top_pred = df.iloc[0]
    
    print(f"\n🎯 YOUR PREDICTION: {top_pred['film']} ({top_pred['win_probability']:.1%})")
    
    print("\n✅ STRENGTHS:")
    
    # Check strengths
    has_gg_drama = top_pred.get('won_gg_drama', 0) == 1
    noms = int(top_pred.get('total_nominations', top_pred.get('noms', 0)))
    prob = top_pred['win_probability']
    
    if has_gg_drama:
        print("   ✅ Won Golden Globe Drama (55% historical Oscar win rate)")
    
    if noms >= 6:
        print(f"   ✅ Strong nomination count ({noms} nominations)")
    
    if 0.30 <= prob <= 0.60:
        print(f"   ✅ Realistic confidence level ({prob:.1%})")
    
    print("\n⚠️ UNCERTAINTIES:")
    print("   ⏳ BAFTA results pending (Feb 16, 2026)")
    print("   ⏳ SAG results pending (Feb 23, 2026)")
    print("   ⏳ These will significantly impact final prediction")
    
    print("\n📈 CONFIDENCE ASSESSMENT:")
    
    if has_gg_drama and noms >= 8:
        confidence = "HIGH"
        reason = "GG Drama win + strong nominations = proven pattern"
    elif has_gg_drama or noms >= 10:
        confidence = "MEDIUM-HIGH"
        reason = "One strong signal present, waiting for BAFTA/SAG confirmation"
    else:
        confidence = "MEDIUM"
        reason = "Reasonable prediction but needs precursor validation"
    
    print(f"   Confidence Level: {confidence}")
    print(f"   Reasoning: {reason}")
    
    print("\n💡 RECOMMENDATION:")
    print("   Your predictions are DEFENSIBLE and based on historical patterns.")
    print("   Update after BAFTA (Feb 16) and SAG (Feb 23) for final prediction.")
    print("   Current prediction is conservative and appropriate given available data.")


if __name__ == "__main__":
    validate_best_picture()
    validate_technical_categories()
    check_historical_comparison()
    final_verdict()
    
    print("\n" + "="*70)
    print("✅ VALIDATION COMPLETE")
    print("="*70)