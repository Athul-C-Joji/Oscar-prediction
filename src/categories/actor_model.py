"""
Leading Actor Category Prediction Model
Using Manual Precursor Data
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score


def train_actor_model():
    print("=" * 50)
    print("LEADING ACTOR MODEL")
    print("=" * 50)

    # --------------------------------------------------
    # 1️⃣ Load Master Dataset
    # --------------------------------------------------
    df = pd.read_csv("data/processed/all_categories_master.csv")

    # Filter Leading Actor only
    df_actor = df[df["category"] == "Leading Actor"].copy()
    print(f"Leading Actor nominations: {len(df_actor)}")

    # --------------------------------------------------
    # Fix Name Format (Last, First → First Last)
    # --------------------------------------------------
    def fix_name_format(name):
        if isinstance(name, str) and "," in name:
            parts = name.split(",")
            return parts[1].strip() + " " + parts[0].strip()
        return name

    df_actor["nominee"] = df_actor["nominee"].apply(fix_name_format)

    # --------------------------------------------------
    # 2️⃣ Career History Feature
    # --------------------------------------------------
    df_actor = df_actor.sort_values(by=["year", "nominee"])
    df_actor["actor_prev_nominations"] = (
        df_actor.groupby("nominee").cumcount()
    )

    # --------------------------------------------------
    # 3️⃣ Best Picture Nominee Feature
    # --------------------------------------------------
    df_bp = df[df["category"] == "Best Picture"]
    bp_films = df_bp.groupby("year")["film"].apply(list).to_dict()

    def is_bp_nominee(row):
        if row["year"] in bp_films:
            return 1 if row["film"] in bp_films[row["year"]] else 0
        return 0

    df_actor["film_is_bp_nominee"] = df_actor.apply(is_bp_nominee, axis=1)

    # --------------------------------------------------
    # 4️⃣ Merge Manual Precursor Data
    # --------------------------------------------------
    precursors = pd.read_csv("data/external/acting_precursors.csv")

    precursors["nominee"] = precursors["nominee"].apply(fix_name_format)

    df_actor = df_actor.merge(
        precursors[["year", "nominee", "won_sag", "won_golden_globe", "won_bafta"]],
        on=["year", "nominee"],
        how="left"
    )

    df_actor[["won_sag", "won_golden_globe", "won_bafta"]] = (
        df_actor[["won_sag", "won_golden_globe", "won_bafta"]]
        .fillna(0)
    )

    # --------------------------------------------------
    # 5️⃣ Feature Selection
    # --------------------------------------------------
    df_actor["total_nominations"] = df_actor["total_nominations"].fillna(0)

    features = [
        "total_nominations",
        "film_is_bp_nominee",
        "actor_prev_nominations",
        "won_sag",
        "won_golden_globe",
        "won_bafta"
    ]

    # --------------------------------------------------
    # 6️⃣ Time-Based Split
    # --------------------------------------------------
    train = df_actor[df_actor["year"] <= 2021]
    test = df_actor[df_actor["year"] > 2021]

    X_train = train[features]
    y_train = train["won"]

    X_test = test[features]
    y_test = test["won"]

    # --------------------------------------------------
    # 7️⃣ Train Model
    # --------------------------------------------------
    model = LogisticRegression(
        class_weight="balanced",
        max_iter=1000
    )

    model.fit(X_train, y_train)

    # --------------------------------------------------
    # 8️⃣ Evaluate
    # --------------------------------------------------
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    auc = roc_auc_score(y_test, y_proba)
    print(f"ROC-AUC: {auc:.3f}")

    print("\nModel training completed.")
    return model


if __name__ == "__main__":
    train_actor_model()
