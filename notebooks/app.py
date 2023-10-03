import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import DATA_BASE_PATH
from config import image_path
from utils import data_loader 
#from utils.ADF_tests import adf_test 
import sqlite3
import sys
import numbers
import time
import math
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from utils.datetime import *
from utils.plot_saver import PlotSaver
from arch.unitroot import ADF
from utils.unitroot import UnitRootTests
from utils.datetime import *
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html