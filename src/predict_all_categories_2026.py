"""
COMPLETE 2026 Oscar Predictions - ALL 24 Categories
Predicts winners across every major Oscar category
"""

import pandas as pd
import joblib
import os
from datetime import datetime


# ALL 24 OSCAR CATEGORIES DATA
ALL_CATEGORIES_DATA = {
    # ========== MAIN CATEGORIES ==========
    'Best Picture': [
        {'nominee': 'Bugonia', 'noms': 4, 'film': 'Bugonia'},
        {'nominee': 'F1', 'noms': 5, 'film': 'F1'},
        {'nominee': 'Frankenstein', 'noms': 10, 'film': 'Frankenstein'},
        {'nominee': 'Hamnet', 'noms': 9, 'film': 'Hamnet'},
        {'nominee': 'Marty Supreme', 'noms': 11, 'film': 'Marty Supreme'},
        {'nominee': 'One Battle after Another', 'noms': 13, 'film': 'One Battle after Another'},
        {'nominee': 'The Secret Agent', 'noms': 2, 'film': 'The Secret Agent'},
        {'nominee': 'Sentimental Value', 'noms': 6, 'film': 'Sentimental Value'},
        {'nominee': 'Sinners', 'noms': 15, 'film': 'Sinners'},
        {'nominee': 'Train Dreams', 'noms': 3, 'film': 'Train Dreams'},
    ],
    
    'Best Director': [
        {'nominee': 'Chloé Zhao', 'film': 'Hamnet', 'noms': 9},
        {'nominee': 'Josh Safdie', 'film': 'Marty Supreme', 'noms': 11},
        {'nominee': 'Paul Thomas Anderson', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Joachim Trier', 'film': 'Sentimental Value', 'noms': 6},
        {'nominee': 'Ryan Coogler', 'film': 'Sinners', 'noms': 15},
    ],
    
    'Best Actor in a Leading Role': [
        {'nominee': 'Timothée Chalamet', 'film': 'Marty Supreme', 'noms': 11},
        {'nominee': 'Leonardo DiCaprio', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Ethan Hawke', 'film': 'Blue Moon', 'noms': 2},
        {'nominee': 'Michael B. Jordan', 'film': 'Sinners', 'noms': 15},
        {'nominee': 'Wagner Moura', 'film': 'The Secret Agent', 'noms': 2},
    ],
    
    'Best Actress in a Leading Role': [
        {'nominee': 'Jessie Buckley', 'film': 'Hamnet', 'noms': 9},
        {'nominee': 'Rose Byrne', 'film': 'If I Had Legs I\'d Kick You', 'noms': 1},
        {'nominee': 'Kate Hudson', 'film': 'Song Sung Blue', 'noms': 1},
        {'nominee': 'Renate Reinsve', 'film': 'Sentimental Value', 'noms': 6},
        {'nominee': 'Emma Stone', 'film': 'Bugonia', 'noms': 4},
    ],
    
    'Best Actor in a Supporting Role': [
        {'nominee': 'Benicio Del Toro', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Jacob Elordi', 'film': 'Frankenstein', 'noms': 10},
        {'nominee': 'Delroy Lindo', 'film': 'Sinners', 'noms': 15},
        {'nominee': 'Sean Penn', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Stellan Skarsgård', 'film': 'Sentimental Value', 'noms': 6},
    ],
    
    'Best Actress in a Supporting Role': [
        {'nominee': 'Elle Fanning', 'film': 'Sentimental Value', 'noms': 6},
        {'nominee': 'Inga Ibsdotter Lilleaas', 'film': 'Sentimental Value', 'noms': 6},
        {'nominee': 'Amy Madigan', 'film': 'Weapons', 'noms': 1},
        {'nominee': 'Wunmi Mosaku', 'film': 'Sinners', 'noms': 15},
        {'nominee': 'Teyana Taylor', 'film': 'One Battle after Another', 'noms': 13},
    ],
    
    'Best Original Screenplay': [
        {'nominee': 'Blue Moon', 'film': 'Blue Moon', 'noms': 2},
        {'nominee': 'It Was Just an Accident', 'film': 'It Was Just an Accident', 'noms': 1},
        {'nominee': 'Marty Supreme', 'film': 'Marty Supreme', 'noms': 11},
        {'nominee': 'Sentimental Value', 'film': 'Sentimental Value', 'noms': 6},
        {'nominee': 'Sinners', 'film': 'Sinners', 'noms': 15},
    ],
    
    'Best Adapted Screenplay': [
        {'nominee': 'Bugonia', 'film': 'Bugonia', 'noms': 4},
        {'nominee': 'Frankenstein', 'film': 'Frankenstein', 'noms': 10},
        {'nominee': 'Hamnet', 'film': 'Hamnet', 'noms': 9},
        {'nominee': 'One Battle after Another', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Train Dreams', 'film': 'Train Dreams', 'noms': 3},
    ],
    
    # ========== TECHNICAL CATEGORIES ==========
    'Best Cinematography': [
        {'nominee': 'Dan Laustsen', 'film': 'Frankenstein', 'noms': 10},
        {'nominee': 'Darius Khondji', 'film': 'Marty Supreme', 'noms': 11},
        {'nominee': 'Michael Bauman', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Autumn Durald Arkapaw', 'film': 'Sinners', 'noms': 15},
        {'nominee': 'Adolpho Veloso', 'film': 'Train Dreams', 'noms': 3},
    ],
    
    'Best Film Editing': [
        {'nominee': 'Stephen Mirrione', 'film': 'F1', 'noms': 5},
        {'nominee': 'Ronald Bronstein & Josh Safdie', 'film': 'Marty Supreme', 'noms': 11},
        {'nominee': 'Andy Jurgensen', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Olivier Bugge Coutté', 'film': 'Sentimental Value', 'noms': 6},
        {'nominee': 'Michael P. Shawver', 'film': 'Sinners', 'noms': 15},
    ],
    
    'Best Production Design': [
        {'nominee': 'Tamara Deverell & Shane Vieau', 'film': 'Frankenstein', 'noms': 10},
        {'nominee': 'Fiona Crombie & Alice Felton', 'film': 'Hamnet', 'noms': 9},
        {'nominee': 'Jack Fisk & Adam Willis', 'film': 'Marty Supreme', 'noms': 11},
        {'nominee': 'Florencia Martin & Anthony Carlino', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Hannah Beachler & Monique Champagne', 'film': 'Sinners', 'noms': 15},
    ],
    
    'Best Costume Design': [
        {'nominee': 'Deborah L. Scott', 'film': 'Avatar: Fire and Ash', 'noms': 2},
        {'nominee': 'Kate Hawley', 'film': 'Frankenstein', 'noms': 10},
        {'nominee': 'Malgosia Turzanska', 'film': 'Hamnet', 'noms': 9},
        {'nominee': 'Miyako Bellizzi', 'film': 'Marty Supreme', 'noms': 11},
        {'nominee': 'Ruth E. Carter', 'film': 'Sinners', 'noms': 15},
    ],
    
    'Best Makeup and Hairstyling': [
        {'nominee': 'Mike Hill, Jordan Samuel & Cliona Furey', 'film': 'Frankenstein', 'noms': 10},
        {'nominee': 'Kyoko Toyokawa, Naomi Hibino & Tadashi Nishimatsu', 'film': 'Kokuho', 'noms': 1},
        {'nominee': 'Ken Diaz, Mike Fontaine & Shunika Terry', 'film': 'Sinners', 'noms': 15},
        {'nominee': 'Kazu Hiro, Glen Griffin & Bjoern Rehbein', 'film': 'The Smashing Machine', 'noms': 2},
        {'nominee': 'Thomas Foldberg & Anne Cathrine Sauerberg', 'film': 'The Ugly Stepsister', 'noms': 1},
    ],
    
    'Best Visual Effects': [
        {'nominee': 'Joe Letteri, Richard Baneham, Eric Saindon & Daniel Barrett', 'film': 'Avatar: Fire and Ash', 'noms': 2},
        {'nominee': 'Ryan Tudhope, Nicolas Chevallier, Robert Harrington & Keith Dawson', 'film': 'F1', 'noms': 5},
        {'nominee': 'David Vickery, Stephen Aplin, Charmaine Chan & Neil Corbould', 'film': 'Jurassic World Rebirth', 'noms': 1},
        {'nominee': 'Charlie Noble, David Zaretti, Russell Bowen & Brandon K. McLaughlin', 'film': 'The Lost Bus', 'noms': 1},
        {'nominee': 'Michael Ralla, Espen Nordahl, Guido Wolter & Donnie Dean', 'film': 'Sinners', 'noms': 15},
    ],
    
    # ========== SOUND & MUSIC ==========
    'Best Sound': [
        {'nominee': 'Gareth John, Al Nelson, Gwendolyn Yates Whittle, Gary A. Rizzo & Juan Peralta', 'film': 'F1', 'noms': 5},
        {'nominee': 'Greg Chapman, Nathan Robitaille, Nelson Ferreira, Christian Cooke & Brad Zoern', 'film': 'Frankenstein', 'noms': 10},
        {'nominee': 'José Antonio García, Christopher Scarabosio & Tony Villaflor', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Chris Welcker, Benjamin A. Burtt, Felipe Pacheco, Brandon Proctor & Steve Boeddeker', 'film': 'Sinners', 'noms': 15},
        {'nominee': 'Amanda Villavieja, Laia Casanovas & Yasmina Praderas', 'film': 'Sirāt', 'noms': 2},
    ],
    
    'Best Original Score': [
        {'nominee': 'Jerskin Fendrix', 'film': 'Bugonia', 'noms': 4},
        {'nominee': 'Alexandre Desplat', 'film': 'Frankenstein', 'noms': 10},
        {'nominee': 'Max Richter', 'film': 'Hamnet', 'noms': 9},
        {'nominee': 'Jonny Greenwood', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Ludwig Goransson', 'film': 'Sinners', 'noms': 15},
    ],
    
    'Best Original Song': [
        {'nominee': 'Dear Me', 'film': 'Diane Warren: Relentless', 'noms': 1, 'artist': 'Diane Warren'},
        {'nominee': 'Golden', 'film': 'KPop Demon Hunters', 'noms': 3, 'artist': 'EJAE et al.'},
        {'nominee': 'I Lied To You', 'film': 'Sinners', 'noms': 15, 'artist': 'Raphael Saadiq & Ludwig Goransson'},
        {'nominee': 'Sweet Dreams Of Joy', 'film': 'Viva Verdi!', 'noms': 1, 'artist': 'Nicholas Pike'},
        {'nominee': 'Train Dreams', 'film': 'Train Dreams', 'noms': 3, 'artist': 'Nick Cave & Bryce Dessner'},
    ],
    
    # ========== SPECIALTY CATEGORIES ==========
    'Best Casting': [
        {'nominee': 'Nina Gold', 'film': 'Hamnet', 'noms': 9},
        {'nominee': 'Jennifer Venditti', 'film': 'Marty Supreme', 'noms': 11},
        {'nominee': 'Cassandra Kulukundis', 'film': 'One Battle after Another', 'noms': 13},
        {'nominee': 'Gabriel Domingues', 'film': 'The Secret Agent', 'noms': 2},
        {'nominee': 'Francine Maisler', 'film': 'Sinners', 'noms': 15},
    ],
    
    'Best International Feature Film': [
        {'nominee': 'The Secret Agent', 'film': 'The Secret Agent', 'noms': 2, 'country': 'Brazil'},
        {'nominee': 'It Was Just an Accident', 'film': 'It Was Just an Accident', 'noms': 1, 'country': 'France'},
        {'nominee': 'Sentimental Value', 'film': 'Sentimental Value', 'noms': 6, 'country': 'Norway'},
        {'nominee': 'Sirāt', 'film': 'Sirāt', 'noms': 2, 'country': 'Spain'},
        {'nominee': 'The Voice of Hind Rajab', 'film': 'The Voice of Hind Rajab', 'noms': 1, 'country': 'Tunisia'},
    ],
    
    'Best Animated Feature Film': [
        {'nominee': 'Arco', 'film': 'Arco', 'noms': 1},
        {'nominee': 'Elio', 'film': 'Elio', 'noms': 1},
        {'nominee': 'KPop Demon Hunters', 'film': 'KPop Demon Hunters', 'noms': 3},
        {'nominee': 'Little Amélie or the Character of Rain', 'film': 'Little Amélie', 'noms': 1},
        {'nominee': 'Zootopia 2', 'film': 'Zootopia 2', 'noms': 1},
    ],
    
    'Best Animated Short Film': [
        {'nominee': 'Butterfly', 'film': 'Butterfly', 'noms': 1},
        {'nominee': 'Forevergreen', 'film': 'Forevergreen', 'noms': 1},
        {'nominee': 'The Girl Who Cried Pearls', 'film': 'The Girl Who Cried Pearls', 'noms': 1},
        {'nominee': 'Retirement Plan', 'film': 'Retirement Plan', 'noms': 1},
        {'nominee': 'The Three Sisters', 'film': 'The Three Sisters', 'noms': 1},
    ],
    
    'Best Live Action Short Film': [
        {'nominee': 'Butcher\'s Stain', 'film': 'Butcher\'s Stain', 'noms': 1},
        {'nominee': 'A Friend of Dorothy', 'film': 'A Friend of Dorothy', 'noms': 1},
        {'nominee': 'Jane Austen\'s Period Drama', 'film': 'Jane Austen\'s Period Drama', 'noms': 1},
        {'nominee': 'The Singers', 'film': 'The Singers', 'noms': 1},
        {'nominee': 'Two People Exchanging Saliva', 'film': 'Two People Exchanging Saliva', 'noms': 1},
    ],
    
    'Best Documentary Feature': [
        {'nominee': 'The Alabama Solution', 'film': 'The Alabama Solution', 'noms': 1},
        {'nominee': 'Come See Me in the Good Light', 'film': 'Come See Me in the Good Light', 'noms': 1},
        {'nominee': 'Cutting through Rocks', 'film': 'Cutting through Rocks', 'noms': 1},
        {'nominee': 'Mr. Nobody against Putin', 'film': 'Mr. Nobody against Putin', 'noms': 1},
        {'nominee': 'The Perfect Neighbor', 'film': 'The Perfect Neighbor', 'noms': 1},
    ],
    
    'Best Documentary Short Film': [
        {'nominee': 'All the Empty Rooms', 'film': 'All the Empty Rooms', 'noms': 1},
        {'nominee': 'Armed Only with a Camera', 'film': 'Armed Only with a Camera', 'noms': 1},
        {'nominee': 'Children No More', 'film': 'Children No More', 'noms': 1},
        {'nominee': 'The Devil Is Busy', 'film': 'The Devil Is Busy', 'noms': 1},
        {'nominee': 'Perfectly a Strangeness', 'film': 'Perfectly a Strangeness', 'noms': 1},
    ],
}


def predict_single_category(category_name, nominees_data, model, features):
    """
    Predict winner for a single category
    """
    print(f"\n{'='*70}")
    print(f"📋 {category_name}")
    print('='*70)
    
    # Create DataFrame
    df = pd.DataFrame(nominees_data)
    
    # Calculate features
    df['year_ceremony'] = 2026
    df['total_nominations'] = df['noms']
    df['nomination_share'] = df['noms'] / df['noms'].sum()
    df['year_total_nominations'] = df['noms'].sum()
    df['nom_ratio'] = df['noms'] / df['year_total_nominations']
    df['is_top_nominated'] = (df['noms'] == df['noms'].max()).astype(int)
    df['nom_rank'] = df['noms'].rank(ascending=False, method='min')
    
    # Precursor awards (placeholder)
    df['won_gg_drama'] = 0
    df['won_gg_musical'] = 0
    df['won_bafta'] = 0
    df['won_sag_cast'] = 0
    df['total_precursor_wins'] = 0
    df['has_precursor_win'] = 0
    df['precursor_sweep'] = 0
    
    # Prepare features
    X = df[features]
    
    # Predict
    try:
        probabilities = model.predict_proba(X)[:, 1]
        df['win_probability'] = probabilities
    except:
        df['win_probability'] = df['nomination_share']
    
    # Sort by probability
    df = df.sort_values('win_probability', ascending=False)
    
    # Display results (top 3 only for brevity)
    for idx, (i, row) in enumerate(df.head(3).iterrows()):
        name = row.get('nominee', row.get('film', 'Unknown'))
        prob = row['win_probability']
        noms = row['noms']
        film = row.get('film', '')
        
        medal = ['🥇', '🥈', '🥉'][idx] if idx < 3 else '  '
        
        if film and film != name:
            print(f"\n{medal} {name} - {film}")
        else:
            print(f"\n{medal} {name}")
        
        print(f"   Win Probability: {prob:.1%}")
        print(f"   Film Nominations: {int(noms)}")
    
    # Winner
    winner = df.iloc[0]
    winner_name = winner.get('nominee', winner.get('film', 'Unknown'))
    
    return df, winner_name, winner['win_probability']


def predict_all_categories():
    """
    Predict winners for ALL 24 Oscar categories
    """
    print("="*70)
    print("🎬 COMPLETE 2026 OSCAR PREDICTIONS - ALL 24 CATEGORIES")
    print("="*70)
    
    # Load model
    print("\n🤖 Loading prediction model...")
    try:
        model = joblib.load('models/tier2_enhanced_model.pkl')
        print("✅ Loaded Tier 2 Enhanced Model")
    except:
        try:
            model = joblib.load('models/tier1_basic_model.pkl')
            print("✅ Loaded Tier 1 Basic Model")
        except:
            print("❌ No model found!")
            return
    
    # Features
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
    
    # Predict each category
    all_predictions = {}
    summary = []
    
    for category_name, nominees_data in ALL_CATEGORIES_DATA.items():
        predictions, winner_name, win_prob = predict_single_category(
            category_name, 
            nominees_data, 
            model, 
            features
        )
        all_predictions[category_name] = predictions
        summary.append({
            'Category': category_name,
            'Winner': winner_name,
            'Probability': win_prob
        })
    
    # Summary
    print("\n" + "="*70)
    print("📊 COMPLETE PREDICTIONS SUMMARY - ALL 24 CATEGORIES")
    print("="*70)
    
    # Group by type
    main_cats = ['Best Picture', 'Best Director', 'Best Actor in a Leading Role', 
                 'Best Actress in a Leading Role', 'Best Actor in a Supporting Role',
                 'Best Actress in a Supporting Role', 'Best Original Screenplay', 
                 'Best Adapted Screenplay']
    
    print("\n🏆 MAIN CATEGORIES:")
    for item in summary:
        if item['Category'] in main_cats:
            print(f"   {item['Category']}")
            print(f"   → {item['Winner']} ({item['Probability']:.1%})\n")
    
    print("\n🎨 TECHNICAL CATEGORIES:")
    tech_cats = ['Best Cinematography', 'Best Film Editing', 'Best Production Design',
                 'Best Costume Design', 'Best Makeup and Hairstyling', 'Best Visual Effects',
                 'Best Sound', 'Best Original Score', 'Best Original Song', 'Best Casting']
    for item in summary:
        if item['Category'] in tech_cats:
            print(f"   {item['Category']}: {item['Winner']} ({item['Probability']:.1%})")
    
    print("\n🌍 SPECIALTY CATEGORIES:")
    for item in summary:
        if item['Category'] not in main_cats and item['Category'] not in tech_cats:
            print(f"   {item['Category']}: {item['Winner']} ({item['Probability']:.1%})")
    
    # Save
    os.makedirs('data/predictions_2026', exist_ok=True)
    
    for category_name, predictions in all_predictions.items():
        safe_name = category_name.lower().replace(' ', '_').replace(',', '').replace('-', '_')
        filename = f'data/predictions_2026/{safe_name}_predictions.csv'
        predictions.to_csv(filename, index=False)
    
    # Master summary
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv('data/predictions_2026/ALL_CATEGORIES_SUMMARY.csv', index=False)
    
    print(f"\n💾 All 24 category predictions saved!")
    print(f"📊 Summary: data/predictions_2026/ALL_CATEGORIES_SUMMARY.csv")
    
    # Film analysis
    print("\n" + "="*70)
    print("🎬 PREDICTIONS BY FILM")
    print("="*70)
    
    film_wins = {}
    for item in summary:
        # Extract film name from winner
        parts = item['Winner'].split(' - ')
        if len(parts) > 1:
            film = parts[-1]
        else:
            film = item['Winner']
        
        if film not in film_wins:
            film_wins[film] = []
        film_wins[film].append(item['Category'])
    
    # Sort by number of predicted wins
    sorted_films = sorted(film_wins.items(), key=lambda x: len(x[1]), reverse=True)
    
    for film, categories in sorted_films[:10]:
        if len(categories) >= 2:
            print(f"\n🎬 {film}: {len(categories)} predicted wins")
            for cat in categories:
                print(f"   • {cat}")
    
    print("\n✅ COMPLETE! All 24 categories predicted.")
    
    return all_predictions


if __name__ == "__main__":
    predict_all_categories()