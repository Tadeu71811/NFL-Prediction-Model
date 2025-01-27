# NFL Prediction Model

## Overview
This project involves building an NFL prediction model to analyze historical data and make game outcome predictions. The model uses machine learning algorithms like TabNet and LightGBM. Data is sourced and processed from nfl_data_py and The Odds API, with results stored in a MySQL database for analysis and visualization.

## Features
1. **Data Import**: Pull historical and live NFL data using nfl_data_py and The Odds API.
2. **Database Management**: Store data in a MySQL database with structured tables for teams, players, and games.
3. **Data Processing**: Clean, transform, and aggregate data for training and predictions.
4. **Model Training**: Train machine learning models (TabNet, LightGBM) to predict outcomes and player performances.
5. **Prediction Analysis**: Evaluate predictions using metrics and visualize results.

---

## Requirements
- Python 3.9+
- MySQL
- nfl_data_py
- LightGBM
- SQLAlchemy
- Pandas
- NumPy
- mysql-connector-python

---

## File Structure
```
nfl-prediction-model/
├── data_processing/           # Scripts for cleaning and aggregating data
│   ├── import_data.py         # Import NFL and Odds API data
│   ├── transform_data.py      # Transform raw data into structured tables
│   ├── database_setup.sql     # SQL scripts for setting up MySQL tables
├── model_training/            # Machine learning model training scripts
│   ├── tabnet_training.py     # Train TabNet model
│   ├── lightgbm_training.py   # Train LightGBM model
│   ├── feature_engineering.py # Feature engineering utilities
├── app/                       # Application to run predictions
│   ├── predict.py             # Script to make predictions
├── requirements.txt           # Dependencies
└── README.md                  # Project documentation
```

---

## Database Structure
- **`league_weekly_stats`**: Contains player statistics.
- **`game_info`**: Stores game details like scores and participating teams.
- **`win_totals`**: Contains betting odds and related data.
- **`team_stats`**: Aggregated team-level statistics.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/nfl-prediction-model.git
   cd nfl-prediction-model
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the MySQL database using the provided `database_setup.sql` script.

4. Configure database credentials in environment variables:
   - `MYSQL_HOST`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`
   - `MYSQL_DATABASE`
  
## Usage
1. **Data Import**:
   Run the `import_data.py` script to pull and store data in the database:
   ```bash
   python data_processing/import_data.py
   ```

2. **Data Transformation**:
   Process raw data into structured tables:
   ```bash
   python data_processing/transform_data.py
   ```

3. **Model Training**:
   Train models on the processed data:
   ```bash
   python model_training/tabnet_training.py
   python model_training/lightgbm_training.py
   ```

4. **Prediction**:
   Use the `predict.py` script to generate predictions:
   ```bash
   python app/predict.py
   ```

---

## Recommendations
1. Regularly update data using nfl_data_py to ensure predictions remain accurate.
2. Expand the feature set by incorporating more columns from `league_weekly_stats` and `win_totals`.
3. Optimize machine learning models with hyperparameter tuning (e.g., using Optuna).
4. Add a visualization layer for better analysis of predictions.

