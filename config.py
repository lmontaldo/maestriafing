import os

# Get the root directory of the project (assuming config.py is in the root)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct paths relative to the root directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATA_BASE_PATH = os.path.join(DATA_DIR, '2023-09.csv')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
MODEL_DIR = os.path.join(ROOT_DIR, 'models')
IMAGE_PATH = os.path.join(ROOT_DIR, 'docs', 'images')
PKL_RAW_DATA_PATH = os.path.join(DATA_DIR, 'fred_data.pkl')
PKL_TRANSF_DATA_PATH = os.path.join(DATA_DIR, 'transf_data_fred_conditions.pkl')
PKL_TCODES_PATH = os.path.join(DATA_DIR, 'tcodes.pkl')