"""
Model Training Script - IMPROVED VERSION
Trains Best Picture prediction model with engineered features
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os


def engineer_features(df):
    """
    Create additional features to improve predictions
    """
    print("\n🔧 Engineering features...")
    
    # Nomination ratio (how many noms compared to that year's average)
    df['nom_ratio'] = df['total_nominations'] / df['year_total_nominations']
    
    # Is it the most nominated film that year?
    df['is_top_nominated'] = (df.groupby('year_ceremony')['total_nominations']
                               .transform('max') == df['total_nominations']).astype(int)
    
    # Nomination rank within year
    df['nom_rank'] = df.groupby('year_ceremony')['total_nominations'].rank(ascending=False, method='min')
    
    print(f"✅ Created new features: nom_ratio, is_top_nominated, nom_rank")
    
    return df


def train_model():

    print("=" * 50)
    print("MODEL TRAINING - IMPROVED")
    print("=" * 50)

    # --------------------------------------------------
    # 1️⃣ Load Processed Data
    # --------------------------------------------------
    print("\n📂 Loading processed data...")
    df = pd.read_csv("data/processed/best_picture_clean.csv")
    
    # Engineer features
    df = engineer_features(df)

    # --------------------------------------------------
    # 2️⃣ Select Features
    # --------------------------------------------------
    features = [
        'total_nominations',
        'nomination_share',
        'nom_ratio',
        'is_top_nominated',
        'nom_rank'
    ]

    target = 'winner'

    X = df[features]
    y = df[target]

    # --------------------------------------------------
    # 3️⃣ Time-Based Split
    # --------------------------------------------------
    print("\n🗓️ Performing time-based split...")

    train = df[df['year_ceremony'] <= 2021]
    test = df[df['year_ceremony'] >= 2022]

    X_train = train[features]
    y_train = train[target]

    X_test = test[features]
    y_test = test[target]

    print(f"✅ Training samples: {len(X_train)}")
    print(f"✅ Testing samples: {len(X_test)}")
    print(f"   Winners in train: {y_train.sum()}")
    print(f"   Winners in test: {y_test.sum()}")

    # --------------------------------------------------
    # 4️⃣ Train Model
    # --------------------------------------------------
    print("\n🤖 Training Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_split=3,
        min_samples_leaf=2,
        class_weight={0: 1, 1: 10},  # Give more weight to winners
        random_state=42
    )

    model.fit(X_train, y_train)

    # --------------------------------------------------
    # 5️⃣ Evaluate Model
    # --------------------------------------------------
    print("\n📊 Evaluating model...")

    y_prob = model.predict_proba(X_test)[:, 1]

    # Lower threshold
    threshold = 0.15
    y_pred = (y_prob >= threshold).astype(int)

    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    try:
        auc_score = roc_auc_score(y_test, y_prob)
        print(f"\n🎯 ROC-AUC Score: {auc_score:.4f}")
    except:
        print("\n⚠️ Not enough data for ROC-AUC")

    # Show predictions with probabilities
    print("\n🔍 Test Set Predictions:")
    test_results = test[['year_ceremony', 'film', 'winner']].copy()
    test_results['predicted_prob'] = y_prob
    test_results['predicted'] = y_pred
    test_results = test_results.sort_values('predicted_prob', ascending=False)
    print(test_results.to_string(index=False))
    
    # Feature importance
    print("\n🔍 Feature Importance:")
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.to_string(index=False))

    # --------------------------------------------------
    # 6️⃣ Save Model
    # --------------------------------------------------
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/best_picture_model.pkl")

    print("\n💾 Model saved to models/best_picture_model.pkl")
    print("\n✅ Training complete!")


if __name__ == "__main__":
    train_model()