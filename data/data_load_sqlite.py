import sqlite3
import pandas as pd

# Connect to the SQLite database
path = 'C:/Users/Transitorio/Desktop/tesis2023/tesis2023-1/data/mydatabase.db'

conn = sqlite3.connect(path)

# Create a cursor object
cursor = conn.cursor()

# Write an SQL query to select column names
query_col_names = "PRAGMA table_info(Datosipc);"

# Execute the query to get column names
cursor.execute(query_col_names)

# Fetch the column names
col_names = [col[1] for col in cursor.fetchall()]

# Write an SQL query to select data from the table
query_data = "SELECT * FROM Datosipc;"

# Execute the query
cursor.execute(query_data)

# Fetch the results
results = cursor.fetchall()

# Create a DataFrame from the fetched results with column names
df = pd.DataFrame(results, columns=col_names)

# Process and display the DataFrame
print(df.head())

# Close the cursor and the database connection
cursor.close()

