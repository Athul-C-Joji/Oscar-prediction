"""
Model Training Script
Trains Best Picture prediction model using time-based split
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os


def train_model():

    print("=" * 50)
    print("MODEL TRAINING")
    print("=" * 50)

    # --------------------------------------------------
    # 1️⃣ Load Processed Data
    # --------------------------------------------------
    print("\n📂 Loading processed data...")
    df = pd.read_csv("data/processed/best_picture_clean.csv")

    # --------------------------------------------------
    # 2️⃣ Select Features (Basic Version)
    # --------------------------------------------------
    # For now we use year as simple feature
    # Later we will add nominations, metadata, etc.

    features = ['year_ceremony']
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

    # --------------------------------------------------
    # 4️⃣ Train Model
    # --------------------------------------------------
    print("\n🤖 Training Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train, y_train)

    # --------------------------------------------------
    # 5️⃣ Evaluate Model
    # --------------------------------------------------
    print("\n📊 Evaluating model...")

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("ROC-AUC Score:", roc_auc_score(y_test, y_prob))

    # --------------------------------------------------
    # 6️⃣ Save Model
    # --------------------------------------------------
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/best_picture_model.pkl")

    print("\n✅ Model saved to models/best_picture_model.pkl")


if __name__ == "__main__":
    train_model()
