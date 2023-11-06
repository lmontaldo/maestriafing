import sys
import os

# Append the src directory to sys.path so you can import modules from there
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from data_retrieval import retrieve_and_transform_data

def main():
    tcode = [1, 2, 4, 5, 6, 7]
    transformed_data = retrieve_and_transform_data(tcode)
    
    # Print the results
    print(transformed_data)

    # Optionally, save or further process the transformed_data as needed

if __name__ == "__main__":
    main()


