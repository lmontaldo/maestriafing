import os
import pickle

# Get the root directory of the project (assuming config.py is in the root)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct paths relative to the root directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATA_BASE_PATH = os.path.join(DATA_DIR, 'datos_fred_procesados.csv')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
MODEL_DIR = os.path.join(ROOT_DIR, 'models')
IMAGE_PATH = os.path.join(ROOT_DIR, 'docs', 'images')
DESCRIPTIONS_PATH = os.path.join(DATA_DIR, 'descripciones.txt')
#pickled data
PKL_HOUTSMW_PATH = os.path.join(DATA_DIR, 'residualsHOUTSMW.pkl')
PKL_NORM_PATH = os.path.join(DATA_DIR, 'data_normalized.pkl')
PKL_X_SLOW_FAST_PATH = os.path.join(DATA_DIR, 'x_slow_fast.pkl')
PKL_YDATA_PATH = os.path.join(DATA_DIR, 'ydata.pkl')

#PKL_TRANSF_DATA_PATH = os.path.join(DATA_DIR, 'transf_data_fred_conditions.pkl')
#PKL_TCODES_PATH = os.path.join(DATA_DIR, 'tcodes.pkl')