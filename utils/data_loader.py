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

def get_data(database_path):
    # Connect to the database
    conn = connect_to_database(database_path)
    # Query 1: Get table data for 'Datosipc'
    table_clases = 'Datosipc'
    df_clases = query_table_data(conn, table_clases)
    # Query 2: Get table data for 'ipc_univariado'
    table_univa = 'ipc_general_ine'
    df_univariado = query_table_data(conn, table_univa)
    # Query 3: Get table data for 'Datos_fmi_2022_external'
    table_fmi = 'Datos_fmi_2022_external'
    df_fmi = query_table_data(conn, table_fmi)
    # Query 4: get the ipc clases to keep and filter  
    table_clases_filter = 'clases_ipc_filtradas'
    df_clases_filter = query_table_data(conn, table_clases_filter)
    # Query 5: IpC general log and z-score 
    table_ipc_gral_re = 'clases_ipc_filtradas'
    df_clases_filter = query_table_data(conn, table_clases_filter)
    
    
    # Close the database connection
    conn.close()
    
    return df_clases, df_univariado, df_fmi, df_clases_filter, 



