import pandas as pd
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

import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from plotly.subplots import make_subplots
import statsmodels.api as sm
import matplotlib.pyplot as plt

import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['EXTERNAL', 'CLASES_IPC','IPC_gral']
df_dict = data_loader.get_data(DATA_BASE_PATH, tables_list)
# to df
df=df_dict['CLASES_IPC']

############################################
# COMPONENTES IPC
############################################
df['ymd'] = pd.to_datetime(df['ymd']).dt.normalize()



# Create a Plotly figure
fig = px.line(df)

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    dcc.Graph(id='graph', figure=fig),
    dcc.Checklist(
        id='filter-tab',
        options=[{'label': i, 'value': i} for i in df.columns],
        value=df.columns.tolist(),
        inline=True,
    )
])

# Define the callback to update the graph based on the filter tab
@app.callback(
    Output('graph', 'figure'),
    [Input('filter-tab', 'value')]
)
def update_graph(selected_series):
    filtered_df = df[selected_series]
    fig = px.line(filtered_df)
    return fig

# Run the Dash web application
if __name__ == '__main__':
    app.run_server(debug=True)
