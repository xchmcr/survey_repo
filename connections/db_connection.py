import sqlite3
import pandas as pd

def load_data_from_db():
    # Step 2: Connect to the SQLite database
    database_path = r'C:\Users\Migue\survey_folder\SurveyDATABASEtest'  # Use raw string
    conn = sqlite3.connect(database_path)

    # Step 3: Write a SQL query to extract data from the db
    query = "SELECT * FROM Survey_Results1;"  # Adjust this to match your actual table name

    # Step 4: Use pandas to read the data into a DataFrame
    df = pd.read_sql_query(query, conn)

    print(df.head(5))

    # Step 5: Close the database connection
    conn.close()

    return df