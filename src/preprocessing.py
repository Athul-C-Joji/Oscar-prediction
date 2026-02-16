"""
Data Preprocessing Script
Cleans and prepares Oscar data for machine learning
"""

import pandas as pd
import os


def preprocess_oscar_data():
    print("=" * 50)
    print("DATA PREPROCESSING")
    print("=" * 50)

    # --------------------------------------------------
    # 1️⃣ Load Raw Data
    # --------------------------------------------------
    print("\n📂 Loading raw data...")
    df = pd.read_csv("data/raw/oscars.csv")

    print(f"✅ Loaded {len(df)} total records")
    print(f"📊 Columns: {list(df.columns)}")

    # --------------------------------------------------
    # 2️⃣ Filter Modern Era (1995–2024)
    # --------------------------------------------------
    print("\n🗓️ Filtering data for modern era (1995–2024)...")

    df = df[
        (df["year_ceremony"] >= 1995) &
        (df["year_ceremony"] <= 2024)
    ]

    print(f"✅ Records after year filtering: {len(df)}")

    # --------------------------------------------------
    # 3️⃣ Create Total Nominations Per Film Feature
    # --------------------------------------------------
    print("\n🏆 Calculating total nominations per film...")

    nom_counts = (
        df.groupby(["year_ceremony", "film"])
        .size()
        .reset_index(name="total_nominations")
    )

    df = df.merge(
        nom_counts,
        on=["year_ceremony", "film"],
        how="left"
    )

    print("✅ Total nominations feature added")

    # --------------------------------------------------
    # 4️⃣ Filter Best Picture Category (for legacy model)
    # --------------------------------------------------
    print("\n🎬 Filtering for Best Picture category...")

    df_bp = df[
        df["category"].str.contains("BEST PICTURE", case=False, na=False)
    ].copy()

    print(f"✅ Found {len(df_bp)} Best Picture nominations")

    # Nomination share feature
    year_totals = (
        df_bp.groupby("year_ceremony")["total_nominations"]
        .sum()
        .reset_index(name="year_total_nominations")
    )

    df_bp = df_bp.merge(
        year_totals,
        on="year_ceremony",
        how="left"
    )

    df_bp["nomination_share"] = (
        df_bp["total_nominations"] /
        df_bp["year_total_nominations"]
    )

    df_bp["winner"] = df_bp["winner"].astype(int)

    df_bp = df_bp.sort_values(by=["year_ceremony"])
    df_bp["nomination_number"] = (
        df_bp.groupby("year_ceremony").cumcount() + 1
    )

    # Validate
    winners_per_year = df_bp.groupby("year_ceremony")["winner"].sum()
    if all(winners_per_year == 1):
        print("✅ Validation passed: Exactly 1 winner per year")

    # Save Best Picture dataset
    os.makedirs("data/processed", exist_ok=True)

    output_path = "data/processed/best_picture_clean.csv"
    df_bp.to_csv(output_path, index=False)

    print(f"✅ Best Picture dataset saved: {output_path}")

    # --------------------------------------------------
    # 5️⃣ Standardize Category Names (FIXED VERSION)
    # --------------------------------------------------
    print("\n🧹 Standardizing category names...")

    def clean_category(cat):
        cat = str(cat).upper()

        if "ACTOR" in cat and "SUPPORTING" in cat:
            return "Supporting Actor"
        elif "ACTOR" in cat:
            return "Leading Actor"
        elif "ACTRESS" in cat and "SUPPORTING" in cat:
            return "Supporting Actress"
        elif "ACTRESS" in cat:
            return "Leading Actress"
        elif "DIRECTING" in cat:
            return "Director"
        elif "FILM EDITING" in cat:
            return "Film Editing"
        elif "CINEMATOGRAPHY" in cat:
            return "Cinematography"
        elif "BEST PICTURE" in cat:
            return "Best Picture"
        else:
            return "Other"

    df["category_clean"] = df["category"].apply(clean_category)

    print("✅ Category cleaning completed")
    print(df["category_clean"].value_counts())

    # --------------------------------------------------
    # 6️⃣ Create All Categories Master Dataset
    # --------------------------------------------------
    print("\n🌎 Creating unified all-categories dataset...")

    columns_needed = [
        "year_ceremony",
        "category_clean",
        "name",
        "film",
        "winner",
        "total_nominations"
    ]

    df_all = df[columns_needed].copy()

    df_all.rename(columns={
        "year_ceremony": "year",
        "category_clean": "category",
        "name": "nominee",
        "winner": "won"
    }, inplace=True)

    all_output_path = "data/processed/all_categories_master.csv"
    df_all.to_csv(all_output_path, index=False)

    print(f"✅ All categories dataset saved: {all_output_path}")
    print(f"✅ Total records: {len(df_all)}")

    print("\n✅ Preprocessing complete!")

    return df_bp


if __name__ == "__main__":
    preprocess_oscar_data()
