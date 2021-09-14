# import dash
# import dash_core_components as dcc
# import dash_html_components as html
import dash_bootstrap_components as dbc 
import pandas as pd
import plotly.graph_objs as go
# from dash.dependencies import Input, Output
# import dash_table
#from BTindex import app
from database import transforms
import plotly.express as px
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

df = transforms.df

def tab2():
    df = transforms.df
    layout = html.Div([
     dbc.Card(dbc.CardBody(html.Div(
            id='table-paging-with-graph-container'
            , className="five columns"
     ))) #end card
     , dbc.Card(dbc.CardBody(html.Div(id = 'scatter-matrix-container')))
    ])#End div
    return layout

layout = tab2()
