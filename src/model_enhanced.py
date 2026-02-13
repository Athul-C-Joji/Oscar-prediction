"""
Enhanced Model Training
Uses ALL features: nominations + precursor awards + ratings + sentiment
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib
import os


def train_enhanced_model():
    """
    Train model with all available features
    """
    print("=" * 60)
    print("ENHANCED MODEL TRAINING")
    print("=" * 60)
    
    # --------------------------------------------------
    # 1️⃣ Load Master Dataset
    # --------------------------------------------------
    print("\n📂 Loading master dataset...")
    df = pd.read_csv('data/processed/master_dataset.csv')
    print(f"✅ Loaded {len(df)} records with {len(df.columns)} features")
    
    # --------------------------------------------------
    # 2️⃣ Select Features
    # --------------------------------------------------
    print("\n🔧 Selecting features for training...")
    
    # Only use rows where we have complete data
    feature_columns = [
        # Nomination features
        'total_nominations',
        'nomination_share',
        
        # Precursor awards (most important!)
        'won_gg_drama',
        'won_gg_musical',
        'won_bafta',
        'won_sag_cast',
        'total_precursor_wins',
        'has_precursor_win',
        'precursor_sweep',
        
        # Ratings
        'imdb_rating',
        'rt_critics',
        'rt_audience',
        'metacritic',
        'combined_score',
        
        # Sentiment
        'avg_vader_sentiment',
        'avg_positive_score',
    ]
    
    # Check which features are available
    available_features = [col for col in feature_columns if col in df.columns]
    print(f"\n✅ Using {len(available_features)} features:")
    for feat in available_features:
        print(f"   - {feat}")
    
    # Filter to rows with complete data
    df_complete = df[available_features + ['winner', 'year_ceremony', 'film']].dropna()
    print(f"\n✅ Complete data: {len(df_complete)} records")
    
    X = df_complete[available_features]
    y = df_complete['winner']
    
    # --------------------------------------------------
    # 3️⃣ Time-Based Split
    # --------------------------------------------------
    print("\n🗓️ Performing time-based split...")
    
    train = df_complete[df_complete['year_ceremony'] <= 2021]
    test = df_complete[df_complete['year_ceremony'] >= 2022]
    
    X_train = train[available_features]
    y_train = train['winner']
    
    X_test = test[available_features]
    y_test = test['winner']
    
    print(f"✅ Training samples: {len(X_train)}")
    print(f"✅ Testing samples: {len(X_test)}")
    print(f"   Winners in train: {y_train.sum()}")
    print(f"   Winners in test: {y_test.sum()}")
    
    # --------------------------------------------------
    # 4️⃣ Train Enhanced Model
    # --------------------------------------------------
    print("\n🤖 Training Random Forest with enhanced features...")
    
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight={0: 1, 1: 15},  # Heavy weight on winners
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print("✅ Model trained!")
    
    # --------------------------------------------------
    # 5️⃣ Evaluate Model
    # --------------------------------------------------
    print("\n📊 Evaluating enhanced model...")
    
    # Training performance
    y_train_pred = model.predict(X_train)
    train_acc = (y_train_pred == y_train).mean()
    
    # Test performance
    y_test_prob = model.predict_proba(X_test)[:, 1]
    threshold = 0.15
    y_test_pred = (y_test_prob >= threshold).astype(int)
    
    print(f"\n🎯 Training Accuracy: {train_acc:.2%}")
    
    print("\n📋 Test Set Classification Report:")
    print(classification_report(y_test, y_test_pred, zero_division=0))
    
    try:
        auc_score = roc_auc_score(y_test, y_test_prob)
        print(f"\n🎯 ROC-AUC Score: {auc_score:.4f}")
    except:
        print("\n⚠️ Not enough data for ROC-AUC")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_test_pred)
    print("\n📊 Confusion Matrix:")
    print(cm)
    print("   [[True Neg  False Pos]")
    print("    [False Neg True Pos]]")
    
    # --------------------------------------------------
    # 6️⃣ Feature Importance
    # --------------------------------------------------
    print("\n🔍 Top 10 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': available_features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(feature_importance.head(10).to_string(index=False))
    
    # --------------------------------------------------
    # 7️⃣ Test Predictions
    # --------------------------------------------------
    print("\n🔮 Predictions on Test Set:")
    test_results = test[['year_ceremony', 'film', 'winner']].copy()
    test_results['predicted_prob'] = y_test_prob
    test_results['predicted'] = y_test_pred
    test_results = test_results.sort_values('predicted_prob', ascending=False)
    
    print(test_results.to_string(index=False))
    
    # Check accuracy
    correct = (test_results['winner'] == test_results['predicted']).sum()
    total = len(test_results)
    print(f"\n✅ Correctly classified: {correct}/{total} ({correct/total:.1%})")
    
    # Winners predicted correctly
    winners_predicted = test_results[test_results['winner'] == 1]['predicted'].sum()
    total_winners = test_results['winner'].sum()
    print(f"🏆 Winners correctly predicted: {winners_predicted}/{total_winners}")
    
    # --------------------------------------------------
    # 8️⃣ Save Model
    # --------------------------------------------------
    os.makedirs('models', exist_ok=True)
    model_path = 'models/enhanced_model.pkl'
    joblib.dump(model, model_path)
    
    # Save feature list
    feature_list_path = 'models/feature_list.txt'
    with open(feature_list_path, 'w') as f:
        for feat in available_features:
            f.write(f"{feat}\n")
    
    print(f"\n💾 Model saved to {model_path}")
    print(f"💾 Feature list saved to {feature_list_path}")
    
    print("\n✅ ENHANCED TRAINING COMPLETE!")
    
    return model, feature_importance


if __name__ == "__main__":
    train_enhanced_model()