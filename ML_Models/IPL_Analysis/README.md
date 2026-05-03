# IPL Data Analysis & Hypothesis Testing

This project explores an IPL (Indian Premier League) dataset containing detailed match and delivery statistics. It is designed to demonstrate data processing, machine learning prediction methods, and rigorous statistical analysis techniques to validate common cricketing assumptions.

## Features & Contents

### 1. Match Outcome Predictor (`predictor.ipynb`)
A Jupyter Notebook dedicated to exploring the dataset and building predictive models. It processes features from `matches.csv` to predict outcomes or analyze patterns within historical IPL games.

### 2. Hypothesis Testing & Statistical Analysis (`toss_hypothesis_test.py`)
A dedicated Python script that uses `scipy.stats` to mathematically prove or disprove assumptions around the famous "Toss Advantage". 

It contains two primary statistical tests:
* **Binomial Test:** Evaluates whether simply winning the toss gives a team an inherent, statistically significant advantage over a 50% baseline (Result: No it doesn't).
* **Chi-Square Test of Independence (A/B Testing):** Analyzes whether the *decision* made after winning the toss (Batting vs Fielding) significantly affects the win probability (Result: Yes, fielding first is statistically advantageous!).

### 3. Exploratory Data Analysis (EDA) (`eda_venue_scores.py`)
A script that processes the core `deliveries.csv` and `matches.csv` to find hidden patterns, outliers, and correlations. 
* **Example Insight:** Finding which IPL venue produces the highest scores by analyzing average 1st innings scores, supported by factors like pitch characteristics, boundaries, and venue altitude.

### 4. Environment Config
* **`requirements.txt`**: Contains the dependencies required to run the analysis (e.g., pandas, scipy, scikit-learn).
* **Datasets**: Powered by the included `matches.csv` and `deliveries.csv` files containing historical IPL data.

## Getting Started

1. Set up the virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run the statistical analysis tests:
   ```bash
   python toss_hypothesis_test.py
   ```
3. Run the Exploratory Data Analysis (EDA):
   ```bash
   python eda_venue_scores.py
   ```
4. Open `predictor.ipynb` in your Jupyter environment to explore models and predictions.
