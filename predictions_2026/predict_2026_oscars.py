"""
2026 Oscar Predictions
Predicts Best Picture winner for 96th Academy Awards (2026)
Using live 2025 awards season data
"""

import pandas as pd
import joblib
import os


def predict_2026_oscars():
    """
    Generate predictions for 2026 Oscars
    """
    print("=" * 70)
    print("🎬 2026 OSCAR PREDICTIONS (96th ACADEMY AWARDS)")
    print("=" * 70)
    
    # --------------------------------------------------
    # 1️⃣ Load Current Contenders
    # --------------------------------------------------
    print("\n📂 Loading 2025 awards season data...")
    
    # Golden Globes
    gg_df = pd.read_csv('data/predictions_2026/golden_globes_2025.csv')
    print(f"✅ Loaded {len(gg_df)} Golden Globes contenders")
    
    # Oscar buzz
    buzz_df = pd.read_csv('data/predictions_2026/oscar_buzz_2025.csv')
    print(f"✅ Loaded {len(buzz_df)} Oscar buzz rankings")
    
    # Merge
    contenders = gg_df.merge(buzz_df[['film', 'buzz_score']], on='film', how='left')
    contenders['buzz_score'] = contenders['buzz_score'].fillna(70)  # Default for films not in buzz list
    
    print(f"\n🎬 {len(contenders)} films in consideration")
    
    # --------------------------------------------------
    # 2️⃣ Simulate Oscar Nomination Data
    # --------------------------------------------------
    print("\n🔧 Estimating Oscar nominations...")
    
    # Estimate nominations based on Golden Globes wins + buzz
    # In reality, wait for actual Oscar noms on Jan 17, 2025
    
    nomination_estimates = []
    for idx, row in contenders.iterrows():
        # More realistic nomination estimates
        base = 6  # Base nominations for serious contenders
        
        if row['won_gg_drama'] == 1 or row['won_gg_musical'] == 1:
            base = 10  # GG winners typically get ~10 noms
        
        if row['buzz_score'] >= 90:
            base = min(base + 2, 11)
        elif row['buzz_score'] >= 85:
            base = min(base + 1, 10)
        elif row['buzz_score'] < 80:
            base = max(base - 1, 5)
        
        nomination_estimates.append(base)
    
    contenders['estimated_nominations'] = nomination_estimates
    
    # Simulate other required features
    contenders['year_ceremony'] = 2026
    contenders['nomination_share'] = contenders['estimated_nominations'] / contenders['estimated_nominations'].sum()
    contenders['year_total_nominations'] = contenders['estimated_nominations'].sum()
    
    # Rename estimated to match training features
    contenders['total_nominations'] = contenders['estimated_nominations']
    
    # Engineering features (same as training)
    contenders['nom_ratio'] = contenders['total_nominations'] / contenders['year_total_nominations']
    contenders['is_top_nominated'] = (contenders['total_nominations'] == contenders['total_nominations'].max()).astype(int)
    contenders['nom_rank'] = contenders['total_nominations'].rank(ascending=False, method='min')
    
    # Precursor wins
    contenders['total_precursor_wins'] = (
        contenders['won_gg_drama'] + 
        contenders['won_gg_musical']
        # Add BAFTA + SAG when available
    )
    contenders['has_precursor_win'] = (contenders['total_precursor_wins'] > 0).astype(int)
    
    # BAFTA and SAG (placeholder - update after Feb 2025)
    contenders['won_bafta'] = 0  # Will update after Feb 16
    contenders['won_sag_cast'] = 0  # Will update after Feb 23
    
    # Update for likely winners based on current predictions
    # These will be updated with actual results
    contenders.loc[contenders['film'] == 'Emilia Pérez', 'won_bafta'] = 0  # TBD
    contenders.loc[contenders['film'] == 'The Brutalist', 'won_bafta'] = 0  # TBD
    
    contenders['precursor_sweep'] = 0  # Will calculate after all awards
    
    # --------------------------------------------------
    # 3️⃣ Load Trained Models
    # --------------------------------------------------
    print("\n🤖 Loading prediction models...")
    
    try:
        model_tier2 = joblib.load('models/tier2_enhanced_model.pkl')
        print("✅ Loaded Tier 2 Enhanced Model (with precursor awards)")
        use_tier = 2
    except:
        model_tier2 = joblib.load('models/tier1_basic_model.pkl')
        print("⚠️ Using Tier 1 Basic Model")
        use_tier = 1
    
    # --------------------------------------------------
    # 4️⃣ Prepare Features
    # --------------------------------------------------
    print("\n🔧 Preparing features for prediction...")
    
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
    # 5️⃣ Generate Predictions
    # --------------------------------------------------
    print("\n🔮 Generating predictions...")
    
    probabilities = model_tier2.predict_proba(X)[:, 1]
    predictions = model_tier2.predict(X)
    
    contenders['win_probability'] = probabilities
    contenders['predicted_winner'] = predictions
    
    # --------------------------------------------------
    # 6️⃣ Display Results
    # --------------------------------------------------
    results = contenders[[
        'film', 
        'win_probability', 
        'estimated_nominations',
        'won_gg_drama',
        'won_gg_musical',
        'buzz_score'
    ]].sort_values('win_probability', ascending=False)
    
    print("\n" + "=" * 70)
    print("🏆 2026 OSCAR BEST PICTURE PREDICTIONS")
    print("=" * 70)
    
    for idx, row in results.iterrows():
        film = row['film']
        prob = row['win_probability']
        noms = row['estimated_nominations']
        gg_drama = "✅ GG Drama Winner" if row['won_gg_drama'] == 1 else ""
        gg_musical = "✅ GG Musical Winner" if row['won_gg_musical'] == 1 else ""
        
        print(f"\n{film}")
        print(f"  Win Probability: {prob:.1%}")
        print(f"  Estimated Nominations: {int(noms)}")
        print(f"  Buzz Score: {row['buzz_score']}")
        if gg_drama:
            print(f"  {gg_drama}")
        if gg_musical:
            print(f"  {gg_musical}")
        if prob == results['win_probability'].max():
            print(f"  🎯 TOP PREDICTION")
    
    # Save predictions
    output_path = 'data/predictions_2026/oscar_predictions_2026.csv'
    results.to_csv(output_path, index=False)
    
    print("\n" + "=" * 70)
    print(f"💾 Predictions saved to {output_path}")
    
    print("\n📌 IMPORTANT NOTES:")
    print("   • These predictions are PRELIMINARY")
    print("   • Oscar nominations announced: January 17, 2025")
    print("   • BAFTA Awards: February 16, 2025")
    print("   • SAG Awards: February 23, 2025")
    print("   • 96th Academy Awards: March 2, 2025")
    print("\n💡 Update this script with actual data as awards happen!")
    
    return results


if __name__ == "__main__":
    predict_2026_oscars()