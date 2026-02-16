"""
Scrape SAG Awards (Best Actor) winners safely
Clean column selection properly
"""

import pandas as pd
import requests
from io import StringIO


def scrape_sag_actor():
    print("=" * 50)
    print("SCRAPING SAG BEST ACTOR WINNERS")
    print("=" * 50)

    url = "https://en.wikipedia.org/wiki/Screen_Actors_Guild_Award_for_Outstanding_Performance_by_a_Male_Actor_in_a_Leading_Role"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch page:", response.status_code)
        return

    tables = pd.read_html(StringIO(response.text))
    print(f"Total tables found: {len(tables)}")

    winners_df = None

    for table in tables:
        cols = [str(col).lower() for col in table.columns]
        if "year" in cols and "actor" in cols and "film" in cols:
            winners_df = table
            break

    if winners_df is None:
        print("Could not find correct winners table.")
        return

    print("Correct table found.")
    print("Columns detected:", winners_df.columns)

    # Select only required columns
    winners_df = winners_df[["Year", "Actor", "Film"]]

    # Extract year
    winners_df["Year"] = winners_df["Year"].astype(str).str.extract(r"(\d{4})")
    winners_df = winners_df.dropna(subset=["Year"])
    winners_df["Year"] = winners_df["Year"].astype(int)

    # Filter modern era
    winners_df = winners_df[
        (winners_df["Year"] >= 1995) & (winners_df["Year"] <= 2024)
    ]

    winners_df["category"] = "Actor"
    winners_df["won_sag"] = 1

    winners_df = winners_df.rename(columns={
        "Year": "year",
        "Actor": "nominee",
        "Film": "film"
    })

    winners_df = winners_df[["year", "category", "nominee", "film", "won_sag"]]

    print(f"Total SAG winners scraped: {len(winners_df)}")

    winners_df.to_csv("data/external/sag_actor_winners.csv", index=False)

    print("Saved to data/external/sag_actor_winners.csv")

    return winners_df


if __name__ == "__main__":
    scrape_sag_actor()
