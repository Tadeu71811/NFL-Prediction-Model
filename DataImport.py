## Data Import Script
```python
import mysql.connector
import warnings
import nfl_data_py as nfl
import pandas as pd
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)

# Establish MySQL connection and create a fresh database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="EnterPassword"
)
cursor = db_connection.cursor()

# Create a new database and switch to it
cursor.execute("CREATE DATABASE IF NOT EXISTS nfl_stats_data_new")
cursor.execute("USE nfl_stats_data_new")

# Helper function to create and insert data into MySQL tables
def create_and_insert_table(dataframe, table_name, exclude_columns=None):
    if exclude_columns:
        dataframe = dataframe[[col for col in dataframe.columns if col not in exclude_columns]]
    
    # Replace infinite values and NaNs
    dataframe.replace([np.inf, -np.inf], None, inplace=True)
    dataframe = dataframe.where(pd.notnull(dataframe), None)

    # Convert date columns explicitly to datetime format in pandas
    if 'date_modified' in dataframe.columns:
        dataframe['date_modified'] = pd.to_datetime(dataframe['date_modified'], errors='coerce')

    # Drop the table if it exists to recreate with the correct schema
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Dynamically define column types based on DataFrame dtypes
    columns = []
    for col in dataframe.columns:
        if col == 'date_modified':
            columns.append(f"`{col}` DATETIME")
        elif pd.api.types.is_datetime64_any_dtype(dataframe[col]):
            columns.append(f"`{col}` DATETIME")
        elif dataframe[col].dtype == "object":
            columns.append(f"`{col}` TEXT")
        elif dataframe[col].dtype == "float64":
            columns.append(f"`{col}` FLOAT")
        elif dataframe[col].dtype == "int64":
            columns.append(f"`{col}` INT")
        else:
            columns.append(f"`{col}` TEXT")

    # Create table with dynamically defined columns
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})")

    # Insert data into table
    cols = ",".join([f"`{col}`" for col in dataframe.columns])
    for _, row in dataframe.iterrows():
        vals = tuple(None if pd.isna(val) else val for val in row)
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({', '.join(['%s'] * len(vals))})"
        try:
            cursor.execute(sql, vals)
        except mysql.connector.Error as err:
            print(f"Error inserting row into {table_name}: {err}")
    db_connection.commit()

try:
    # Define year ranges
    full_year_range = range(2018, 2025)
    limited_year_range = range(2018, 2025)  # For functions with data only available post-2018

    # Load data and insert it into the database
    create_and_insert_table(nfl.import_weekly_data(full_year_range), 'weekly')
    create_and_insert_table(nfl.import_seasonal_data(full_year_range), 'seasonal')
    create_and_insert_table(nfl.import_team_desc(), 'team_descriptions')
    create_and_insert_table(nfl.import_players(), 'players')
    create_and_insert_table(nfl.import_win_totals(full_year_range), 'win_totals')
    create_and_insert_table(nfl.import_sc_lines(full_year_range), 'score_lines')
    create_and_insert_table(nfl.import_officials(full_year_range), 'officials')
    create_and_insert_table(nfl.import_draft_picks(full_year_range), 'draft_picks')
    create_and_insert_table(nfl.import_draft_values(), 'draft_values')
    create_and_insert_table(nfl.import_combine_data(full_year_range), 'combine')
    create_and_insert_table(nfl.import_schedules(full_year_range), 'schedules')
    create_and_insert_table(nfl.import_ids(), 'ids')
    create_and_insert_table(nfl.import_ngs_data('passing', full_year_range), 'ngs_pass')
    create_and_insert_table(nfl.import_ngs_data('receiving', full_year_range), 'ngs_rec')
    create_and_insert_table(nfl.import_ngs_data('rushing', full_year_range), 'ngs_rush')
    create_and_insert_table(nfl.import_injuries(range(2018, 2025)), 'injuries')
    create_and_insert_table(nfl.import_qbr(range(2018, 2025)), 'qbr')

    # Import PFR data with limited year range (2018 onward)
    create_and_insert_table(nfl.import_seasonal_pfr("pass", limited_year_range), 'seasonal_pfr_pass')
    create_and_insert_table(nfl.import_seasonal_pfr("rec", limited_year_range), 'seasonal_pfr_rec')
    create_and_insert_table(nfl.import_seasonal_pfr("rush", limited_year_range), 'seasonal_pfr_rush')
    create_and_insert_table(nfl.import_seasonal_pfr("def", limited_year_range), 'seasonal_pfr_def')
    
    create_and_insert_table(nfl.import_weekly_pfr("pass", limited_year_range), 'weekly_pfr_pass')
    create_and_insert_table(nfl.import_weekly_pfr("rec", limited_year_range), 'weekly_pfr_rec')
    create_and_insert_table(nfl.import_weekly_pfr("rush", limited_year_range), 'weekly_pfr_rush')
    create_and_insert_table(nfl.import_weekly_pfr("def", limited_year_range), 'weekly_pfr_def')
    
    create_and_insert_table(nfl.import_snap_counts(range(2018, 2025)), 'snap_counts')

    # Confirm successful load
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("\nList of tables:\n")
    for table in tables:
        print(table[0])

except Exception as e:
    print("Error:", e)

finally:
    # Close the connection
    cursor.close()
    db_connection.close()
    print("\nThe MySQL connection is closed.")
