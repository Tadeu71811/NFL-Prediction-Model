## Data Aggregation Script
```python
import mysql.connector
import pandas as pd
from mysql.connector import Error

try:
    print("Connecting to MySQL database...")
    db_connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="EnterPassword",
        database="nfl_stats_data_new",
        connection_timeout=60
    )

    if db_connection.is_connected():
        print("Connection successful.")

        # Function to execute and print SQL command success messages
        def execute_and_print(query, success_msg):
            cursor.execute(query)
            print(success_msg)

        # Set up cursor
        cursor = db_connection.cursor()

        # Step 1: Load and Transform `league_weekly_stats` table data
        league_query = """
            SELECT player_name, player_display_name, position, recent_team, game_id, opponent_team, season, week, passing_yards, rushing_yards, fantasy_points 
            FROM league_weekly_stats
        """
        cursor.execute(league_query)
        league_data = cursor.fetchall()
        league_columns = [col[0] for col in cursor.description]
        league_df = pd.DataFrame(league_data, columns=league_columns)

        # Fill missing values
        league_df.fillna(0, inplace=True)  # Filling numeric columns with 0
        league_df.fillna('Unknown', inplace=True)  # Filling categorical columns

        # Create transformed `league_weekly_stats_transformed`
        cursor.execute("DROP TABLE IF EXISTS league_weekly_stats_transformed")
        create_league_table_query = """
            CREATE TABLE league_weekly_stats_transformed (
                player_name VARCHAR(255),
                player_display_name VARCHAR(255),
                position VARCHAR(50),
                recent_team VARCHAR(10),
                game_id VARCHAR(20),
                opponent_team VARCHAR(10),
                season INT,
                week INT,
                passing_yards FLOAT,
                rushing_yards FLOAT,
                fantasy_points FLOAT
            )
        """
        execute_and_print(create_league_table_query, "Table 'league_weekly_stats_transformed' created successfully.")
        
        # Insert league data
        insert_league_query = """
            INSERT INTO league_weekly_stats_transformed (player_name, player_display_name, position, recent_team, game_id, opponent_team, season, week, passing_yards, rushing_yards, fantasy_points)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_league_query, league_df.values.tolist())
        db_connection.commit()
        print("Data successfully inserted into 'league_weekly_stats_transformed'.")

        # Step 2: Load `team_descriptions` for Basic Team Information
        team_query = "SELECT team_id, team_abbr, team_name FROM team_descriptions"
        cursor.execute(team_query)
        team_data = cursor.fetchall()
        team_columns = [col[0] for col in cursor.description]
        team_df = pd.DataFrame(team_data, columns=team_columns)

        # Create `team_stats_transformed` table with minimal columns
        cursor.execute("DROP TABLE IF EXISTS team_stats_transformed")
        create_team_table_query = """
            CREATE TABLE team_stats_transformed (
                team_id VARCHAR(10),
                team_abbr VARCHAR(10),
                team_name VARCHAR(255)
            )
        """
        execute_and_print(create_team_table_query, "Table 'team_stats_transformed' created successfully.")
        
        # Insert team information data
        insert_team_query = """
            INSERT INTO team_stats_transformed (team_id, team_abbr, team_name)
            VALUES (%s, %s, %s)
        """
        cursor.executemany(insert_team_query, team_df.values.tolist())
        db_connection.commit()
        print("Data successfully inserted into 'team_stats_transformed'.")

        # Step 3: Game Information - Load `schedules` and include necessary details
        schedule_query = "SELECT game_id, season, week, home_team, away_team, home_score, away_score FROM schedules"
        cursor.execute(schedule_query)
        schedule_data = cursor.fetchall()
        schedule_columns = [col[0] for col in cursor.description]
        schedule_df = pd.DataFrame(schedule_data, columns=schedule_columns)

        # Replace NaNs with None manually in data list
        schedule_data_cleaned = [
            tuple(None if pd.isna(value) else value for value in row)
            for row in schedule_df.values.tolist()
        ]

        # Create `game_info_transformed` table
        cursor.execute("DROP TABLE IF EXISTS game_info_transformed")
        create_game_table_query = """
            CREATE TABLE game_info_transformed (
                game_id VARCHAR(20),
                season INT,
                week INT,
                home_team VARCHAR(10),
                away_team VARCHAR(10),
                home_score INT,
                away_score INT
            )
        """
        execute_and_print(create_game_table_query, "Table 'game_info_transformed' created successfully.")
        
        # Insert game information data
        insert_game_query = """
            INSERT INTO game_info_transformed (game_id, season, week, home_team, away_team, home_score, away_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_game_query, schedule_data_cleaned)
        db_connection.commit()
        print("Data successfully inserted into 'game_info_transformed'.")

        # Step 4: Load and Transform `win_totals` table data
        win_totals_query = """
            SELECT game_id, market_type, abbr, `lines`, `odds`, opening_lines, opening_odds, book, season
            FROM win_totals
        """
        cursor.execute(win_totals_query)
        win_totals_data = cursor.fetchall()
        win_totals_columns = [col[0] for col in cursor.description]
        win_totals_df = pd.DataFrame(win_totals_data, columns=win_totals_columns)

        # Convert columns to FLOAT and handle non-numeric values
        for col in ['lines', 'odds', 'opening_lines', 'opening_odds']:
            win_totals_df[col] = pd.to_numeric(win_totals_df[col], errors='coerce').fillna(0)

        # Create transformed `win_totals_transformed` table
        cursor.execute("DROP TABLE IF EXISTS win_totals_transformed")
        create_win_totals_table_query = """
            CREATE TABLE win_totals_transformed (
                game_id VARCHAR(20),
                market_type VARCHAR(50),
                abbr VARCHAR(10),
                `lines` FLOAT,
                `odds` FLOAT,
                opening_lines FLOAT,
                opening_odds FLOAT,
                book VARCHAR(255),
                season INT
            )
        """
        execute_and_print(create_win_totals_table_query, "Table 'win_totals_transformed' created successfully.")

        # Insert win_totals data
        insert_win_totals_query = """
            INSERT INTO win_totals_transformed (game_id, market_type, abbr, `lines`, `odds`, opening_lines, opening_odds, book, season)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_win_totals_query, win_totals_df.values.tolist())
        db_connection.commit()
        print("Data successfully inserted into 'win_totals_transformed'.")

except Error as db_error:
    print(f"Database error: {db_error}")
except Exception as e:
    print(f"General error: {e}")

finally:
    if 'db_connection' in locals() and db_connection.is_connected():
        db_connection.close()
        print("Database connection closed.")
