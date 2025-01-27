import pandas as pd
import lightgbm as lgb

# Define the expected features based on the model output
expected_features = [
    'week', 'home_score', 'away_score', 'home_team_ARI', 'home_team_ATL', 'home_team_BAL', 'home_team_BUF', 
    'home_team_CAR', 'home_team_CHI', 'home_team_CIN', 'home_team_CLE', 'home_team_DAL', 'home_team_DEN', 
    'home_team_DET', 'home_team_GB', 'home_team_HOU', 'home_team_IND', 'home_team_JAX', 'home_team_KC', 
    'home_team_LA', 'home_team_LAC', 'home_team_LV', 'home_team_MIA', 'home_team_MIN', 'home_team_NE', 
    'home_team_NO', 'home_team_NYG', 'home_team_NYJ', 'home_team_OAK', 'home_team_PHI', 'home_team_PIT', 
    'home_team_SEA', 'home_team_SF', 'home_team_TB', 'home_team_TEN', 'home_team_WAS', 'away_team_ARI', 
    'away_team_ATL', 'away_team_BAL', 'away_team_BUF', 'away_team_CAR', 'away_team_CHI', 'away_team_CIN', 
    'away_team_CLE', 'away_team_DAL', 'away_team_DEN', 'away_team_DET', 'away_team_GB', 'away_team_HOU', 
    'away_team_IND', 'away_team_JAX', 'away_team_KC', 'away_team_LA', 'away_team_LAC', 'away_team_LV', 
    'away_team_MIA', 'away_team_MIN', 'away_team_NE', 'away_team_NO', 'away_team_NYG', 'away_team_NYJ', 
    'away_team_OAK', 'away_team_PHI', 'away_team_PIT', 'away_team_SEA', 'away_team_SF', 'away_team_TB', 
    'away_team_TEN', 'away_team_WAS'
]

# Initialize the input data with all features set to 0
input_data = pd.DataFrame(0, index=[0], columns=expected_features)

# Set values for Tampa Bay Buccaneers vs Kansas City Chiefs game
input_data['week'] = 8                  # Set the week of the game
input_data['home_team_TB'] = 1          # Set Tampa Bay as the home team
input_data['away_team_KC'] = 1          # Set Kansas City as the away team
input_data['home_score'] = 0            # Placeholder for home score
input_data['away_score'] = 0            # Placeholder for away score

# Load the model
loaded_model = lgb.Booster(model_file="C:/Users/Peter/Desktop/models/lgbm_model.txt")

# Make the prediction
pred_prob = loaded_model.predict(input_data)[0]
predicted_win = pred_prob > 0.5

# Interpret the prediction
print(f"Prediction: {'Tampa Bay will likely win' if predicted_win else 'Tampa Bay will likely lose'} against Kansas City with probability {pred_prob:.2f}")
