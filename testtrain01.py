import mysql.connector
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# Define the path to save the model
model_directory = "Modelpath"
model_path = os.path.join(model_directory, "lgbm_model.txt")

# Create the directory if it doesn't exist
os.makedirs(model_directory, exist_ok=True)

try:
    # Step 1: Connect to MySQL database without SQLAlchemy
    db_connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="PASSWORD",
        database="nfl_stats_data_new"
    )
    if db_connection.is_connected():
        print("Connected to MySQL database.")

        # Step 2: Load Data from Database
        game_info_df = pd.read_sql("SELECT * FROM game_info_transformed", db_connection)
        
        # Step 3: Prepare Dataset for Prediction
        # Creating a binary target variable (1 if home team wins, else 0)
        game_info_df['home_win'] = (game_info_df['home_score'] > game_info_df['away_score']).astype(int)

        # Selecting features for training
        features = game_info_df[['week', 'home_team', 'away_team', 'home_score', 'away_score']]
        labels = game_info_df['home_win']

        # Handling NaN values by filling them with 0
        features.fillna(0, inplace=True)

        # One-hot encoding categorical features for `home_team` and `away_team`
        features = pd.get_dummies(features, columns=['home_team', 'away_team'])

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

        # Step 4: Initialize LGBMClassifier and Train Model with Early Stopping
        model = lgb.LGBMClassifier(
            objective='binary',
            learning_rate=0.1,
            n_estimators=100
        )

        # Define an early stopping callback
        callbacks = [lgb.early_stopping(stopping_rounds=10)]

        # Train the model with early stopping callback
        print("Training the model with early stopping...")
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            eval_metric='binary_error',
            callbacks=callbacks
        )

        # Step 5: Make Predictions and Evaluate Model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy:.2f}")

        # Step 6: Save the trained model to the specified directory
        model.booster_.save_model(model_path)
        print(f"Model saved as '{model_path}'")

except mysql.connector.Error as db_error:
    print(f"Database connection error: {db_error}")

finally:
    # Close the database connection
    if 'db_connection' in locals() and db_connection.is_connected():
        db_connection.close()
        print("Database connection closed.")
