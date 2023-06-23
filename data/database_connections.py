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

# Main function to execute the queries
def main():
    # Specify the database path
    path = 'C:/Users/Transitorio/Desktop/tesis2023/tesis2023-1/data/mydatabase.db'
    
    # Connect to the database
    conn = connect_to_database(path)
    
    # Query 1: Get column names
    table_clases = 'Datosipc'
    df_clases = query_table_data(conn, table_clases)
    print("Table data for table 'Datosipc':")
    print(df_clases.head())
    
    # Query 2: Get table data
    table_univa = 'ipc_univariado'
    df_univariado = query_table_data(conn, table_univa)
    print("Table data for table 'ipc_univariado':")
    print(df_univariado.head())
    
    # Query 3: Get table data for the third query
    table_fmi = 'Datos_fmi_2022_external'
    df_fmi = query_table_data(conn, table_fmi)
    print("Table data for table 'Datos_fmi_2022_external':")
    print(df_fmi.head())
    
    # Close the database connection
    conn.close()

# Call the main function
main()
