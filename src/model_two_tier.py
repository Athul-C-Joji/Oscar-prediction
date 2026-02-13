"""
Two-Tier Prediction System
- Tier 1: Basic model for all films (nominations only)
- Tier 2: Enhanced model when precursor awards available
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os


def train_two_tier_system():
    """
    Train both basic and enhanced models
    """
    print("=" * 60)
    print("TWO-TIER PREDICTION SYSTEM")
    print("=" * 60)
    
    # --------------------------------------------------
    # Load Data
    # --------------------------------------------------
    print("\n📂 Loading master dataset...")
    df = pd.read_csv('data/processed/master_dataset.csv')
    
    # --------------------------------------------------
    # TIER 1: BASIC MODEL (All Historical Data)
    # --------------------------------------------------
    print("\n" + "=" * 60)
    print("TIER 1: BASIC MODEL (Nominations Only)")
    print("=" * 60)
    
    # Features available for ALL films
    basic_features = [
        'total_nominations',
        'nomination_share',
    ]
    
    # Add engineered features from earlier
    df['nom_ratio'] = df['total_nominations'] / df['year_total_nominations']
    df['is_top_nominated'] = (df.groupby('year_ceremony')['total_nominations']
                               .transform('max') == df['total_nominations']).astype(int)
    df['nom_rank'] = df.groupby('year_ceremony')['total_nominations'].rank(ascending=False, method='min')
    
    basic_features.extend(['nom_ratio', 'is_top_nominated', 'nom_rank'])
    
    df_basic = df[basic_features + ['winner', 'year_ceremony', 'film']].dropna()
    
    print(f"✅ Basic model dataset: {len(df_basic)} records")
    
    # Split
    train_basic = df_basic[df_basic['year_ceremony'] <= 2021]
    test_basic = df_basic[df_basic['year_ceremony'] >= 2022]
    
    X_train_basic = train_basic[basic_features]
    y_train_basic = train_basic['winner']
    X_test_basic = test_basic[basic_features]
    y_test_basic = test_basic['winner']
    
    print(f"Training: {len(X_train_basic)}, Testing: {len(X_test_basic)}")
    
    # Train
    model_basic = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        class_weight={0: 1, 1: 10},
        random_state=42
    )
    
    model_basic.fit(X_train_basic, y_train_basic)
    
    # Evaluate
    y_prob_basic = model_basic.predict_proba(X_test_basic)[:, 1]
    y_pred_basic = (y_prob_basic >= 0.15).astype(int)
    
    print("\n📊 Basic Model Performance:")
    print(classification_report(y_test_basic, y_pred_basic, zero_division=0))
    
    try:
        auc_basic = roc_auc_score(y_test_basic, y_prob_basic)
        print(f"ROC-AUC: {auc_basic:.4f}")
    except:
        pass
    
    # --------------------------------------------------
    # TIER 2: ENHANCED MODEL (With Precursor Awards)
    # --------------------------------------------------
    print("\n" + "=" * 60)
    print("TIER 2: ENHANCED MODEL (With Precursor Awards)")
    print("=" * 60)
    
        # Tier 2: Just add precursor awards (don't require ratings/sentiment)
    enhanced_features = basic_features + [
        'won_gg_drama',
        'won_gg_musical',
        'won_bafta',
        'won_sag_cast',
        'total_precursor_wins',
        'has_precursor_win',
        'precursor_sweep',
    ]

    print(f"Enhanced features: {enhanced_features}")
    
    df_enhanced = df[enhanced_features + ['winner', 'year_ceremony', 'film']].dropna()
    
    print(f"✅ Enhanced model dataset: {len(df_enhanced)} records")
    print(f"✅ Features: {len(enhanced_features)}")
    
    if len(df_enhanced) >= 10:  # Need minimum data
        # Split
        train_enh = df_enhanced[df_enhanced['year_ceremony'] <= 2021]
        test_enh = df_enhanced[df_enhanced['year_ceremony'] >= 2022]
        
        if len(train_enh) > 0:
            X_train_enh = train_enh[enhanced_features]
            y_train_enh = train_enh['winner']
            X_test_enh = test_enh[enhanced_features]
            y_test_enh = test_enh['winner']
            
            print(f"Training: {len(X_train_enh)}, Testing: {len(X_test_enh)}")
            
            # Train
            model_enhanced = RandomForestClassifier(
                n_estimators=300,
                max_depth=10,
                class_weight={0: 1, 1: 15},
                random_state=42
            )
            
            model_enhanced.fit(X_train_enh, y_train_enh)
            
            # Evaluate
            if len(X_test_enh) > 0:
                y_prob_enh = model_enhanced.predict_proba(X_test_enh)[:, 1]
                y_pred_enh = (y_prob_enh >= 0.15).astype(int)
                
                print("\n📊 Enhanced Model Performance:")
                print(classification_report(y_test_enh, y_pred_enh, zero_division=0))
                
                try:
                    auc_enh = roc_auc_score(y_test_enh, y_prob_enh)
                    print(f"ROC-AUC: {auc_enh:.4f}")
                except:
                    pass
        else:
            print("⚠️ Not enough training data for enhanced model")
            model_enhanced = None
    else:
        print("⚠️ Not enough data for enhanced model - using basic only")
        model_enhanced = None
    
    # --------------------------------------------------
    # Save Models
    # --------------------------------------------------
    os.makedirs('models', exist_ok=True)
    
    joblib.dump(model_basic, 'models/tier1_basic_model.pkl')
    print(f"\n💾 Tier 1 model saved")
    
    if model_enhanced:
        joblib.dump(model_enhanced, 'models/tier2_enhanced_model.pkl')
        print(f"💾 Tier 2 model saved")
    
    # Save feature lists
    with open('models/basic_features.txt', 'w') as f:
        for feat in basic_features:
            f.write(f"{feat}\n")
    
    if model_enhanced:
        with open('models/enhanced_features.txt', 'w') as f:
            for feat in enhanced_features:
                f.write(f"{feat}\n")
    
    print("\n✅ TWO-TIER SYSTEM COMPLETE!")
    
    return model_basic, model_enhanced


if __name__ == "__main__":
    train_two_tier_system()