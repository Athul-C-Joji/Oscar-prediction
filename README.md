# 🎬 Oscar Winner Prediction

Machine Learning project to predict Academy Award (Oscar) winners using historical data and advanced analytics.

## 👨‍🎓 Author
**Athul C Joji**  
MSc Big Data Analytics Student

## 📊 Project Overview

This project analyzes historical Oscar nomination data to predict winners using machine learning algorithms. The focus is on the **Best Picture** category with plans to expand to other categories.

### Key Features:
- Historical Oscar data analysis (1928-2024)
- Data preprocessing and feature engineering
- Machine learning models (Random Forest, XGBoost)
- Interactive Jupyter notebooks for exploration
- Visualization of trends and patterns

## 🛠️ Technologies Used

- **Python 3.11**
- **Data Analysis:** pandas, numpy
- **Machine Learning:** scikit-learn, XGBoost
- **Visualization:** matplotlib, seaborn
- **Development:** VS Code, Jupyter Notebook

## 📁 Project Structure
```
oscar-prediction/
│
├── data/
│   ├── raw/              # Original downloaded datasets
│   └── processed/        # Cleaned and prepared data
│
├── notebooks/            # Jupyter notebooks for analysis
│   └── exploration.ipynb
│
├── src/                  # Python source code
│   ├── data_collection.py
│   ├── preprocessing.py
│   ├── model.py
│   └── predict.py
│
├── models/               # Saved trained models
│
├── results/              # Predictions and visualizations
│
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🚀 How to Run

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/oscar-prediction.git
cd oscar-prediction
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Collect data:**
```bash
python src/data_collection.py
```

4. **Preprocess data:**
```bash
python src/preprocessing.py
```

5. **Explore data:**
Open `notebooks/exploration.ipynb` in VS Code or Jupyter

## 📈 Current Progress

- [x] Project setup
- [x] Data collection
- [x] Data preprocessing
- [x] Exploratory data analysis
- [ ] Feature engineering
- [ ] Model training
- [ ] Model evaluation
- [ ] Predictions for upcoming Oscars

## 🎯 Future Enhancements

- Add precursor awards data (Golden Globes, BAFTA, SAG)
- Include movie metadata (ratings, revenue, genre)
- Expand to multiple categories
- Build a web interface for predictions
- Real-time prediction updates

## 📝 License

This project is for educational purposes.

## 📧 Contact

For questions or collaborations, reach out via GitHub!