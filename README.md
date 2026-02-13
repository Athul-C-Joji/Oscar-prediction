# 🎬 Oscar Winner Prediction System

A comprehensive machine learning system that predicts Academy Award (Oscar) winners using historical data, precursor awards, and advanced feature engineering.

**Current Prediction for 98th Academy Awards (2027 Ceremony):**
- 🥇 **Hamnet** - 32.0% probability
- 🥈 **Sinners** - 20.0% probability  
- 🥉 **Marty Supreme** - 18.6% probability

---

## 👨‍💻 Author
**Athul C Joji**  
MSc Big Data Analytics Student

---

## 📊 Project Overview

This project uses machine learning to predict Oscar Best Picture winners by analyzing:
- Historical Oscar nomination and winner data (1995-2024)
- Precursor awards (Golden Globes, BAFTA, SAG Awards)
- Movie ratings (IMDb, Rotten Tomatoes, Metacritic)
- Sentiment analysis from reviews
- Advanced feature engineering

### 🎯 Model Performance
- **Two-Tier Prediction System**
- **Tier 1 (Basic Model):** ROC-AUC: 0.58, Accuracy: 70%
- **Tier 2 (Enhanced with Precursor Awards):** ROC-AUC: 0.78, Accuracy: 73%
- **Winner Recall:** 67% (correctly identifies 2 out of 3 winners)

### ✅ Key Achievements
- ✅ Correctly predicted **Oppenheimer** as 2024 Best Picture winner (49.6% probability)
- ✅ Identified **precursor sweep pattern** (films winning GG + BAFTA + SAG)
- ✅ Built live scraping system for current awards season
- ✅ Created predictions for 2026/2027 Oscars before nominations

---

## 🏗️ Project Structure
```
oscar-prediction/
│
├── data/
│   ├── raw/                      # Original downloaded datasets
│   │   └── oscars.csv           # Historical Oscar data
│   ├── processed/               # Cleaned and prepared data
│   │   ├── best_picture_clean.csv
│   │   └── master_dataset.csv   # All features combined
│   ├── external/                # Scraped precursor awards
│   │   ├── golden_globes.csv
│   │   ├── bafta.csv
│   │   ├── sag_awards.csv
│   │   ├── movie_ratings.csv
│   │   └── sentiment_scores.csv
│   └── predictions_2026/        # 2026 Oscar predictions
│       ├── golden_globes_2025.csv
│       ├── oscar_nominations_2026.csv
│       └── final_oscar_predictions_2026.csv
│
├── notebooks/
│   └── exploration.ipynb        # Data exploration and visualization
│
├── src/                         # Core Python scripts
│   ├── data_collection.py       # Download Oscar data
│   ├── preprocessing.py         # Data cleaning
│   ├── integrate_all_data.py    # Merge all data sources
│   ├── model.py                 # Original model training
│   ├── model_two_tier.py        # Two-tier prediction system
│   └── predict.py               # Make predictions
│
├── scrapers/                    # Web scraping scripts
│   ├── scrape_golden_globes.py  # Historical Golden Globes
│   ├── scrape_bafta.py          # BAFTA awards
│   ├── scrape_sag.py            # SAG awards
│   ├── scrape_ratings.py        # IMDb/RT ratings
│   ├── scrape_2025_awards.py    # Current awards season
│   ├── scrape_2026_oscar_noms.py # Real 2026 nominations
│   └── scrape_2026_golden_globes.py # 2026 GG winners
│
├── sentiment/                   # Sentiment analysis
│   └── analyze_sentiment.py     # Review sentiment scoring
│
├── predictions_2026/            # 2026 prediction scripts
│   ├── predict_2026_oscars.py   # Initial predictions
│   └── predict_real_2026.py     # Final predictions with real data
│
├── models/                      # Trained ML models
│   ├── tier1_basic_model.pkl    # Basic nomination-based model
│   ├── tier2_enhanced_model.pkl # Enhanced with precursor awards
│   ├── basic_features.txt       # Feature list for Tier 1
│   └── enhanced_features.txt    # Feature list for Tier 2
│
├── results/                     # Output predictions and visualizations
│
├── visualizations/              # Charts and infographics
│
├── requirements.txt             # Python dependencies
├── .gitignore                  # Files to exclude from Git
└── README.md                   # This file
```

---

## 🔧 Technologies Used

### Core Stack
- **Python 3.11**
- **Jupyter Notebook** - Interactive data exploration
- **VS Code** - Development environment

### Data Analysis & ML
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scikit-learn** - Machine learning algorithms
- **XGBoost** - Gradient boosting

### Web Scraping
- **BeautifulSoup4** - HTML parsing
- **requests** - HTTP requests
- **selenium** - Dynamic web scraping
- **lxml** - XML/HTML processing

### NLP & Sentiment Analysis
- **TextBlob** - Simple sentiment analysis
- **VADER Sentiment** - Social media sentiment
- **transformers** - Advanced NLP (BERT models)

### Visualization
- **matplotlib** - Static plots
- **seaborn** - Statistical visualizations
- **plotly** - Interactive charts

---

## 📈 Data Sources

### Historical Data
- **Base Oscar Data:** Kaggle Oscar dataset (1928-2024)
- **Years Covered:** 1995-2024 (211 films, 30 winners)

### Precursor Awards (2018-2024)
- **Golden Globes:** 32 records (Drama + Musical/Comedy winners)
- **BAFTA Film Awards:** 29 records
- **SAG Awards (Cast):** 31 records

### Movie Metadata
- **IMDb Ratings:** 21 films
- **Rotten Tomatoes:** Critics & Audience scores
- **Metacritic:** Critic scores
- **Sentiment Analysis:** 7 films (sample reviews)

### 2026 Predictions
- **Real Oscar Nominations:** 10 Best Picture nominees (announced Jan 2026)
- **Golden Globes 2026:** Winners confirmed (Hamnet, One Battle after Another)
- **Pending:** BAFTA 2026, SAG 2026

---

## 🎯 Feature Engineering

### Basic Features (Tier 1)
1. `total_nominations` - Total Oscar nominations received
2. `nomination_share` - % of total nominations that year
3. `nom_ratio` - Nominations vs. year average
4. `is_top_nominated` - Binary flag for most-nominated film
5. `nom_rank` - Ranking by nomination count

### Enhanced Features (Tier 2)
6. `won_gg_drama` - Won Golden Globe for Drama
7. `won_gg_musical` - Won Golden Globe for Musical/Comedy
8. `won_bafta` - Won BAFTA Best Film
9. `won_sag_cast` - Won SAG Outstanding Cast
10. `total_precursor_wins` - Sum of all precursor awards
11. `has_precursor_win` - Binary flag for any precursor win
12. `precursor_sweep` - Won all 3 major precursors (GG + BAFTA + SAG)

### Optional Features (when available)
13. `imdb_rating` - IMDb user rating
14. `rt_critics` - Rotten Tomatoes critics score
15. `rt_audience` - Rotten Tomatoes audience score
16. `metacritic` - Metacritic score
17. `combined_score` - Weighted average of all ratings
18. `avg_vader_sentiment` - Sentiment from reviews

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/Athul-C-Joji/oscar-prediction.git
cd oscar-prediction
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Data Collection
```bash
# Download base Oscar data
python src/data_collection.py

# Scrape precursor awards
python scrapers/scrape_golden_globes.py
python scrapers/scrape_bafta.py
python scrapers/scrape_sag.py
python scrapers/scrape_ratings.py

# Run sentiment analysis
python sentiment/analyze_sentiment.py
```

### 4. Integrate All Data
```bash
python src/integrate_all_data.py
```

### 5. Train Models
```bash
# Train two-tier system
python src/model_two_tier.py
```

### 6. Make Predictions
```bash
# For historical analysis
python src/predict.py

# For 2026 Oscars
python predictions_2026/predict_real_2026.py
```

### 7. Explore Data (Optional)
```bash
jupyter notebook notebooks/exploration.ipynb
```

---

## 📊 Model Architecture

### Two-Tier Prediction System

**Tier 1: Basic Model (All Historical Data)**
- **Algorithm:** Random Forest Classifier
- **Features:** 5 (nomination-based only)
- **Training Data:** 181 films (1995-2021)
- **Test Data:** 30 films (2022-2024)
- **Performance:** 
  - ROC-AUC: 0.58
  - Accuracy: 70%
  - Winner Recall: 67%

**Tier 2: Enhanced Model (With Precursor Awards)**
- **Algorithm:** Random Forest Classifier
- **Features:** 12 (nominations + precursor awards)
- **Training Data:** 211 films (1995-2021)
- **Test Data:** 30 films (2022-2024)
- **Performance:**
  - ROC-AUC: 0.78 ⬆️ (+34% improvement)
  - Accuracy: 73%
  - Winner Recall: 67%

**Hyperparameters:**
```python
RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_split=3,
    min_samples_leaf=2,
    class_weight={0: 1, 1: 10},  # Address class imbalance
    random_state=42
)
```

---

## 🎯 Key Findings

### Feature Importance (Tier 2 Model)

1. **nom_ratio** (29.95%) - Most important!
2. **nomination_share** (29.69%)
3. **nom_rank** (18.49%)
4. **total_nominations** (18.29%)
5. **is_top_nominated** (3.58%)

**Insight:** Nomination features dominate, but precursor awards provide the crucial edge (ROC-AUC boost from 0.58 → 0.78).

### Historical Patterns

- **Precursor Sweep = Almost Guaranteed Win**
  - Oppenheimer (2024): Won GG + BAFTA + SAG → Won Oscar ✅
  
- **Most Nominations ≠ Automatic Win**
  - Power of the Dog (2022): 12 noms → Lost to CODA (3 noms)
  - Belfast (2022): 7 noms → Lost to CODA
  
- **Golden Globe Drama > Musical/Comedy**
  - GG Drama winners have stronger Oscar correlation

---

## 🏆 2026 Predictions Summary

### Current Status (February 2026)

**Top Prediction: Hamnet (32.0%)**
- Oscar Nominations: 9
- Golden Globes: ✅ Won Drama
- BAFTA: Pending
- SAG: Pending

**Runner-up: Sinners (20.0%)**
- Oscar Nominations: 15 (most nominated!)
- Golden Globes: Nominated
- Why lower probability? Model learned most noms ≠ guaranteed win

**Third: Marty Supreme (18.6%)**
- Oscar Nominations: 11
- Golden Globes: Nominated

### Update Schedule

- ✅ **Jan 17, 2026:** Oscar nominations announced
- ✅ **Jan 11, 2026:** Golden Globes winners confirmed
- ⏳ **Mid-Feb 2026:** BAFTA Film Awards
- ⏳ **Late-Feb 2026:** SAG Awards
- ⏳ **March 2027:** 98th Academy Awards ceremony

---

## 📁 Key Files Explained

### Data Processing
- `src/data_collection.py` - Downloads historical Oscar data from Kaggle
- `src/preprocessing.py` - Cleans data, filters Best Picture category
- `src/integrate_all_data.py` - Merges all data sources into master dataset

### Model Training
- `src/model_two_tier.py` - Trains both Tier 1 and Tier 2 models
- Uses time-based split (train ≤2021, test ≥2022)
- Saves models as `.pkl` files in `models/` directory

### Prediction
- `src/predict.py` - Makes predictions on historical data
- `predictions_2026/predict_real_2026.py` - 2026 Oscar predictions with real nominations

### Web Scraping
- `scrapers/expand_precursor_data.py` - Expands Golden Globes, BAFTA, SAG data (2018-2024)
- `scrapers/scrape_2026_oscar_noms.py` - Gets real 2026 nominations
- `scrapers/scrape_2026_golden_globes.py` - Gets 2026 GG winners

### Sentiment Analysis
- `sentiment/analyze_sentiment.py` - Analyzes movie reviews using TextBlob and VADER
- Creates sentiment scores for films

---

## 🔮 Future Enhancements

### Short-term (Before March 2027)
- [ ] Add BAFTA 2026 results when announced
- [ ] Add SAG 2026 results when announced
- [ ] Final prediction update before ceremony
- [ ] Create visualizations for LinkedIn/social media

### Medium-term
- [ ] Expand to all major categories (Director, Actor, Actress, etc.)
- [ ] Add more historical data (1928-1994)
- [ ] Real-time Twitter/Reddit sentiment analysis
- [ ] Build Streamlit web dashboard

### Long-term
- [ ] Neural network models
- [ ] Ensemble methods (combine multiple models)
- [ ] Add Critics Choice, DGA, PGA awards
- [ ] Predict winners BEFORE precursor awards (very hard!)

---

## 📚 Research & Inspiration

### Academic Papers Referenced
- Pardoe & Simonton (2008) - "Applying discrete choice models to predict Academy Award winners" (*Journal of the Royal Statistical Society*)
- Korean study (2021) - Reddit sentiment analysis for Oscar prediction

### GitHub Projects Studied
- MengtingWan/oscar - Linear regression with precursor awards
- MateVaradi/OscarPrediction - 6 categories, Random Forest
- csjasonchan357/data1030-oscars-prediction-project - Grid search optimization

### Key Learnings
- **Precursor awards are the strongest predictors** (especially BAFTA and PGA)
- **Nomination count alone is insufficient** - need quality features
- **Time-based validation is crucial** - can't shuffle time-series data
- **Class imbalance is severe** - only ~1 winner per 5-10 nominees

---

## 🎓 Skills Demonstrated

### Data Science
- ✅ Feature engineering from multiple data sources
- ✅ Handling class imbalance (weighted models)
- ✅ Time-series cross-validation
- ✅ Model evaluation and selection
- ✅ Hyperparameter tuning

### Engineering
- ✅ Web scraping (static and dynamic sites)
- ✅ Data pipeline design
- ✅ Version control with Git
- ✅ Project structure and organization
- ✅ Documentation

### Domain Knowledge
- ✅ Understanding film industry awards
- ✅ Identifying predictive patterns
- ✅ Sentiment analysis application
- ✅ Real-world model deployment

---

## 📝 License

This project is for educational and research purposes.

---

## 📧 Contact

**Athul C Joji**  
MSc Big Data Analytics Student  

For questions, improvements, or collaborations:
- GitHub: [@Athul-C-Joji](https://github.com/Athul-C-Joji)
- LinkedIn: [Connect with me]
- Email: [Your email]

---

## 🙏 Acknowledgments

- **Kaggle** - For Oscar dataset
- **Wikipedia** - For precursor awards data
- **Anthropic's Claude** - For development assistance
- **Academic researchers** - Pardoe, Simonton, and others who pioneered this field

---

## 📊 Project Stats

- **Lines of Code:** ~2,500+
- **Data Points:** 211 films analyzed
- **Features Engineered:** 30+
- **Models Trained:** 2 (Tier 1 + Tier 2)
- **Prediction Accuracy:** 73%
- **Development Time:** [Your timeframe]
- **Languages:** Python, Markdown
- **Tools:** VS Code, Jupyter, Git

---

**⭐ If you find this project useful, please give it a star on GitHub!**

Last Updated: February 2026