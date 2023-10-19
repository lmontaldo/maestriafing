import pandas as pd
import pickle
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
prepro_file_path = os.path.join(project_root, "data", "prepro", "datos_fred_procesados.csv")
def main():
    fred = pd.read_csv(prepro_file_path, sep=",", index_col='index')
    start_date = fred.index.min()
    end_date = fred.index.min()
    expected_index = pd.date_range(start=start_date, end=end_date, freq='MS')  # 'MS' for monthly start
    print(expected_index.max())
    print(len(expected_index))
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

if __name__ == "__main__":
    main()
