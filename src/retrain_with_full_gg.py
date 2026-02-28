"""
Retrain Model with Full Golden Globes Dataset (1944-2024)
Compare performance before vs after
"""

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import os


def retrain_with_full_gg():
    """
    Retrain the model with expanded Golden Globes data
    """
    print("="*70)
    print("🔄 RETRAINING MODEL WITH FULL GOLDEN GLOBES DATA")
    print("="*70)
    
    # Load the expanded dataset
    df = pd.read_csv('data/processed/oscar_with_full_gg_matched.csv')
    
    print(f"\n✅ Loaded {len(df)} records")
    print(f"   Years: {df['year_ceremony'].min()} - {df['year_ceremony'].max()}")
    print(f"   Films with GG data: {((df['won_gg_drama'] > 0) | (df['won_gg_musical'] > 0)).sum()}")
    
    # Prepare features
    print(f"\n🔧 Preparing features...")
    
    # Basic features
    df['nomination_share'] = df['total_nominations'] / df['year_total_nominations']
    df['nom_ratio'] = df['total_nominations'] / df.groupby('year_ceremony')['total_nominations'].transform('mean')
    df['is_top_nominated'] = (df['total_nominations'] == df.groupby('year_ceremony')['total_nominations'].transform('max')).astype(int)
    df['nom_rank'] = df.groupby('year_ceremony')['total_nominations'].rank(ascending=False, method='min')
    
    # Precursor features
    df['total_precursor_wins'] = df['won_gg_drama'] + df['won_gg_musical']
    df['has_precursor_win'] = (df['total_precursor_wins'] > 0).astype(int)
    df['precursor_sweep'] = 0  # Will be 1 when film wins GG+BAFTA+SAG
    
    # Add placeholder for BAFTA/SAG
    if 'won_bafta' not in df.columns:
        df['won_bafta'] = 0
    if 'won_sag_cast' not in df.columns:
        df['won_sag_cast'] = 0
    
    # Features list
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
    
    # Prepare data
    X = df[features]
    y = df['winner']
    
    # Time-based split (very important!)
    print(f"\n📊 Splitting data (time-based)...")
    train_mask = df['year_ceremony'] <= 2021
    test_mask = df['year_ceremony'] >= 2022
    
    X_train = X[train_mask]
    y_train = y[train_mask]
    X_test = X[test_mask]
    y_test = y[test_mask]
    
    print(f"   Training: {len(X_train)} films (up to 2021)")
    print(f"   Testing: {len(X_test)} films (2022-2024)")
    
    # Train model
    print(f"\n🤖 Training Random Forest...")
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_split=3,
        min_samples_leaf=2,
        class_weight={0: 1, 1: 10},
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    print(f"✅ Model trained!")
    
    # Evaluate
    print(f"\n📊 MODEL PERFORMANCE:")
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    print(classification_report(y_test, y_pred, zero_division=0))
    
    roc_auc = roc_auc_score(y_test, y_proba)
    print(f"ROC-AUC: {roc_auc:.4f}")
    
    # Feature importance
    print(f"\n📈 FEATURE IMPORTANCE:")
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.iterrows():
        print(f"   {row['feature']}: {row['importance']:.4f}")
    
    # Compare with old model
    print(f"\n📊 COMPARISON WITH PREVIOUS MODEL:")
    print(f"   Previous ROC-AUC: 0.78")
    print(f"   New ROC-AUC: {roc_auc:.4f}")
    
    if roc_auc > 0.78:
        improvement = ((roc_auc - 0.78) / 0.78) * 100
        print(f"   📈 Improvement: +{improvement:.1f}% 🎉")
    elif roc_auc < 0.78:
        decline = ((0.78 - roc_auc) / 0.78) * 100
        print(f"   📉 Slight decline: -{decline:.1f}%")
    else:
        print(f"   ➡️ Same performance")
    
    # Save new model
    os.makedirs('models', exist_ok=True)
    model_path = 'models/tier2_enhanced_model_full_gg.pkl'
    joblib.dump(model, model_path)
    
    print(f"\n💾 New model saved to: {model_path}")
    
    # Test on recent films
    print(f"\n🔮 TESTING ON 2024 FILMS:")
    test_2024 = df[df['year_ceremony'] == 2024].copy()
    
    if len(test_2024) > 0:
        X_2024 = test_2024[features]
        proba_2024 = model.predict_proba(X_2024)[:, 1]
        test_2024['predicted_prob'] = proba_2024
        
        test_2024_sorted = test_2024.sort_values('predicted_prob', ascending=False)
        
        print(f"\n   2024 Predictions:")
        for idx, row in test_2024_sorted.head(5).iterrows():
            film = row['film']
            prob = row['predicted_prob']
            actual = "✅ WON" if row['winner'] == 1 else "❌ Lost"
            gg_drama = "🏆 GG Drama" if row['won_gg_drama'] == 1 else ""
            
            print(f"   {film}: {prob:.1%} {actual} {gg_drama}")
    
    print(f"\n✅ RETRAINING COMPLETE!")
    
    return model, feature_importance


if __name__ == "__main__":
    retrain_with_full_gg()