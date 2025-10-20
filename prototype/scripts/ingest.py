# This script will be responsible for:
# 1. Reading the mock_namaste.csv file.
# 2. Creating and connecting to the SQLite database (terminology.db).
# 3. Populating the database with the harmonized terminology data.
# (In the future, it will also fetch data from the WHO API)

import pandas as pd
import sqlite3
import os

# Get the absolute path of the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the path of the parent directory (the 'prototype' folder)
PROTOTYPE_DIR = os.path.dirname(SCRIPT_DIR)


def create_database():
    # Define paths relative to the script's location
    csv_path = os.path.join(PROTOTYPE_DIR, 'mock_namaste.csv')
    db_path = os.path.join(PROTOTYPE_DIR, 'terminology.db')

    # Read the mock CSV data
    try:
        df = pd.read_csv(csv_path)
        print(f"Successfully read {csv_path}")
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
        return

    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS terminology_map (
            namaste_code TEXT PRIMARY KEY,
            term_name TEXT,
            description TEXT,
            equivalent_icd11_code TEXT
        )
    ''')
    print(f"Database and table created successfully at {db_path}")

    # Insert data from dataframe into the database
    df.to_sql('terminology_map', conn, if_exists='replace', index=False)
    print(f"Inserted {len(df)} records into the database.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()