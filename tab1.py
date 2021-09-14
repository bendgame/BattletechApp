# import dash
import plotly
# import dash_core_components as dcc
# import dash_html_components as html 
import dash_bootstrap_components as dbc 
# import dash_table
import pandas as pd
# from dash.dependencies import Input, Output
#from index import app 
from database import transforms
import plotly.graph_objects as go
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

df = transforms.df

PAGE_SIZE = 15

def tab1():
    layout =  html.Div(children =[dbc.Row([dbc.Col(dbc.Card([dbc.CardBody([html.H2('Select a unit:'), dash_table.DataTable(
        id='table-sorting-filtering'
        , columns=[{'name': i, 'id': i} for i in df.columns]
        , style_table={'height':'600px'
            ,'overflowX': 'scroll'}
        , style_data_conditional=[
             {'if': {'row_index': 'odd'}
             , 'backgroundColor': 'rgb(248, 248, 248)'
            }]
        , style_cell={
            'height': '30'
            # all three widths are needed
            , 'minWidth': '120px'
            , 'width': '120px'
            , 'maxWidth': '190px'
            , 'textAlign': 'left'
            , 'whiteSpace': 'normal'
        }
        , style_cell_conditional=[
            {'if': {'column_id': 'Name'},
            'width': '900px'},
            # {'if': {'column_id': 'title'},
            # 'width': '18%'},
        ],
        page_current= 0,
        row_selectable="single",
        page_size= PAGE_SIZE,
        page_action='custom',
        filter_action='custom',
        filter_query='',
        sort_action='custom',
        sort_mode='multi',
        sort_by=[]
        )#end data table
        ])])#end card
        , width=6)#end col
                    
    ,  dbc.Col(dbc.Card(dbc.CardBody(html.Div(id = 'radar-graph'))), width=6)
    #,  html.Br()
    ])#end row   
    ])#end div

    return layout

layout = tab1()
