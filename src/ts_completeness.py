import pandas as pd
import sys
import os

# Append the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, PKL_TRANSF_DATA_PATH, PKL_RAW_DATA_PATH 
import pandas as pd

# Example: Generate an expected complete time index
# Example: Generate an expected complete time index with monthly frequency
start_date = '1959-01'
end_date = '2023-08'
expected_index = pd.date_range(start=start_date, end=end_date, freq='MS')  # 'MS' for monthly start
print(expected_index.max())
print(len(expected_index))
fred = pd.read_pickle(PKL_RAW_DATA_PATH)
# Assuming df is your DataFrame with the time index
actual_index = fred.index
print(len(actual_index))

# Check if the actual index matches the expected index
is_complete = actual_index.equals(expected_index)

if is_complete:
    print("The time index is complete.")
else:
    print("The time index is not complete.")
    
missing_time_points = expected_index.difference(actual_index)   
num_missing_time_points = len(missing_time_points) 
print("Missing time points:")
print(missing_time_points)
print(f"Number of missing time points: {num_missing_time_points}")