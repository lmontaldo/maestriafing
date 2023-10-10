import sqlite3
import pandas as pd

def connect_to_database(database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    return conn

def execute_query(conn, query):
    # Create a cursor object
    cursor = conn.cursor()
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch the results
    results = cursor.fetchall()
    
    # Close the cursor
    cursor.close()
    
    return results

def query_column_names(conn, table_name):
    # Write an SQL query to select column names
    query = f"PRAGMA table_info({table_name});"
    
    # Execute the query to get column names
    results = execute_query(conn, query)
    
    # Fetch the column names
    col_names = [col[1] for col in results]
    
    return col_names

def query_table_data(conn, table_name):
    # Write an SQL query to select data from the table
    query = f"SELECT * FROM {table_name};"
    
    # Execute the query
    results = execute_query(conn, query)
    
    # Fetch the column names
    col_names = query_column_names(conn, table_name)
    
    # Create a DataFrame from the fetched results with column names
    df = pd.DataFrame(results, columns=col_names)
    
    return df
def get_data(database_path, table_names):
    # Connect to the database
    conn = connect_to_database(database_path)

    # Create a dictionary to hold your DataFrames
    df_dict = {}

    for table in table_names:
        # Query table data
        df_dict[table] = query_table_data(conn, table)

    # Close the database connection
    
    conn.close()
    
    return df_dict    


