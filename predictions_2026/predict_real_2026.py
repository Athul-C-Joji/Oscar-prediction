"""
2026 Oscar Predictions with REAL Nominations
Uses actual 98th Academy Awards nominees (announced Jan 2026)
"""

import pandas as pd
import joblib
import os


def predict_real_2026_oscars():
    """
    Predict 2026 Oscars using REAL nomination data
    """
    print("=" * 70)
    print("🎬 2026 OSCAR PREDICTIONS - 98TH ACADEMY AWARDS")
    print("   Using REAL Nomination Data!")
    print("=" * 70)
    
    # --------------------------------------------------
    # 1️⃣ REAL 2026 Oscar Nominees (from official announcement)
    # --------------------------------------------------
    print("\n📂 Loading REAL 2026 Oscar nominees...")
    
    real_nominees = [
        {'film': 'Sinners', 'total_nominations': 15},
        {'film': 'One Battle after Another', 'total_nominations': 13},
        {'film': 'Marty Supreme', 'total_nominations': 11},
        {'film': 'Frankenstein', 'total_nominations': 10},
        {'film': 'Hamnet', 'total_nominations': 9},
        {'film': 'Sentimental Value', 'total_nominations': 6},
        {'film': 'F1', 'total_nominations': 5},
        {'film': 'Bugonia', 'total_nominations': 4},
        {'film': 'Train Dreams', 'total_nominations': 3},
        {'film': 'The Secret Agent', 'total_nominations': 2},
    ]
    
    contenders = pd.DataFrame(real_nominees)
    print(f"✅ Loaded {len(contenders)} Best Picture nominees")
    
    # --------------------------------------------------
    # 2️⃣ Add Precursor Awards Data
    # --------------------------------------------------
    print("\n🏆 Adding precursor awards data...")
    
    # Golden Globes 2026 - ACTUAL WINNERS (83rd Golden Globe Awards - Jan 11, 2026)
    contenders['won_gg_drama'] = 0
    contenders['won_gg_musical'] = 0
    
    # Update with actual winners
    contenders.loc[contenders['film'] == 'Hamnet', 'won_gg_drama'] = 1
    contenders.loc[contenders['film'] == 'One Battle after Another', 'won_gg_musical'] = 1
    
    # BAFTA 2026 (update after Feb ceremony)
    contenders['won_bafta'] = 0
    
    # SAG 2026 (update after Feb ceremony)
    contenders['won_sag_cast'] = 0
    
    # Manually update known winners (if any)
    # Example: contenders.loc[contenders['film'] == 'Sinners', 'won_bafta'] = 1
    
    print("⚠️ Precursor awards data pending - will update as results come in")
    
    # --------------------------------------------------
    # 3️⃣ Calculate Features
    # --------------------------------------------------
    print("\n🔧 Calculating prediction features...")
    
    contenders['year_ceremony'] = 2026
    contenders['nomination_share'] = contenders['total_nominations'] / contenders['total_nominations'].sum()
    contenders['year_total_nominations'] = contenders['total_nominations'].sum()
    
    # Engineering features (same as training)
    contenders['nom_ratio'] = contenders['total_nominations'] / contenders['year_total_nominations']
    contenders['is_top_nominated'] = (contenders['total_nominations'] == contenders['total_nominations'].max()).astype(int)
    contenders['nom_rank'] = contenders['total_nominations'].rank(ascending=False, method='min')
    
    # Precursor wins
    contenders['total_precursor_wins'] = (
        contenders['won_gg_drama'] + 
        contenders['won_gg_musical'] + 
        contenders['won_bafta'] + 
        contenders['won_sag_cast']
    )
    contenders['has_precursor_win'] = (contenders['total_precursor_wins'] > 0).astype(int)
    contenders['precursor_sweep'] = 0  # Will update if any film wins all 3 major precursors
    
    # --------------------------------------------------
    # 4️⃣ Load Model
    # --------------------------------------------------
    print("\n🤖 Loading trained prediction model...")
    
    try:
        model = joblib.load('models/tier2_enhanced_model.pkl')
        print("✅ Loaded Tier 2 Enhanced Model")
        use_tier = 2
    except:
        model = joblib.load('models/tier1_basic_model.pkl')
        print("⚠️ Using Tier 1 Basic Model")
        use_tier = 1
    
    # --------------------------------------------------
    # 5️⃣ Prepare Features
    # --------------------------------------------------
    if use_tier == 2:
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
    else:
        features = [
            'total_nominations',
            'nomination_share',
            'nom_ratio',
            'is_top_nominated',
            'nom_rank',
        ]
    
    X = contenders[features]
    
    # --------------------------------------------------
    # 6️⃣ Generate Predictions
    # --------------------------------------------------
    print("\n🔮 Generating predictions...")
    
    probabilities = model.predict_proba(X)[:, 1]
    predictions = model.predict(X)
    
    contenders['win_probability'] = probabilities
    contenders['predicted_winner'] = predictions
    
    # --------------------------------------------------
    # 7️⃣ Display Results
    # --------------------------------------------------
    results = contenders[[
        'film', 
        'win_probability', 
        'total_nominations',
        'total_precursor_wins'
    ]].sort_values('win_probability', ascending=False)
    
    print("\n" + "=" * 70)
    print("🏆 2026 OSCAR BEST PICTURE PREDICTIONS")
    print("   Based on REAL nomination data from 98th Academy Awards")
    print("=" * 70)
    
    for idx, row in results.iterrows():
        film = row['film']
        prob = row['win_probability']
        noms = row['total_nominations']
        precursor = row['total_precursor_wins']
        
        print(f"\n{film}")
        print(f"  Win Probability: {prob:.1%}")
        print(f"  Total Nominations: {int(noms)}")
        print(f"  Precursor Awards Won: {int(precursor)}")
        
        if prob == results['win_probability'].max():
            print(f"  🎯 TOP PREDICTION ⭐")
    
    # Save predictions
    output_path = 'data/predictions_2026/final_oscar_predictions_2026.csv'
    results.to_csv(output_path, index=False)
    
    print("\n" + "=" * 70)
    print(f"💾 Predictions saved to {output_path}")
    
    # Top 3
    print("\n🥇 TOP 3 PREDICTIONS:")
    top3 = results.head(3)
    for i, (idx, row) in enumerate(top3.iterrows(), 1):
        medal = ["🥇", "🥈", "🥉"][i-1]
        print(f"{medal} {row['film']} - {row['win_probability']:.1%}")
    
    print("\n📌 NOTES:")
    print("   • Predictions based on REAL Oscar nominations")
    print("   • Update after Golden Globes results")
    print("   • Update after BAFTA (mid-Feb 2026)")
    print("   • Update after SAG (late-Feb 2026)")
    print("   • 98th Academy Awards: March 2027")
    
    print("\n💡 Most nominated film doesn't always win!")
    print(f"   {results.iloc[0]['film']} is the model's pick despite not having most noms")
    
    return results


if __name__ == "__main__":
    predict_real_2026_oscars()