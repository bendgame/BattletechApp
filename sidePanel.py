# import dash
import plotly
# import dash_core_components as dcc
# import dash_html_components as html 
import dash_bootstrap_components as dbc 
# import dash_table
import pandas
#from dash.dependencies import Input, Output

from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
#from BTindex import *

from tabs import tab1, tab2#, tab3
                       
from database import transforms

df = transforms.df
min_p=df.Points.min()
max_p=df.Points.max()

def side_panel():
    sp = html.Div([
      html.Img(src= "/assets/BattleTech_Logo.png")
      , dbc.Row([dbc.Col(
        html.Div([dbc.Card(dbc.CardBody([
          html.H2('Filters')
          ,dcc.Checklist(id='battlemech-only'
            , options = [{'label':' Only BattleMechs '
                , 'value':'Y'}]
            ) #end checklist
          , html.H5('Points Slider')
          , dcc.RangeSlider(id='points-slider'
            , min = min_p
            , max= max_p
            , marks = {0: '0',
                    20: '20',
                    40: '40',
                    60: '60',
                    80: '80',
                    100: '100',
                    }
            , value = [1,100]
            ) #end slider            
          , html.H5('Role')
          , dcc.Dropdown(id = 'role-drop'
            , options= [{'label':i, 'value': i} 
                    for i in sorted(df['Role'].unique())]
            , multi = True
            )
            ]))        
        ], style={'marginBottom': 50, 'marginTop': 25
                , 'marginLeft':15, 'marginRight':15}
        ) #end div  
            , width=2
        )#end col 1
    , dbc.Col(html.Div( children=[
         dbc.Card(dbc.CardBody([
           dcc.Tabs(id="tabs", value='tab-1', children=[
             dcc.Tab(label='Unit Finder', value='tab-1')
             , dcc.Tab(label='Macro Analysis', value='tab-2')
            ])
           ]))#end card
        , html.Div(id='tabs-content')
        ]), width=10) #end col 2
        ])#end row
    
    ],style={
        'background-image': 'url("/assets/btimage1.png")',
        'background-position': 'center',
        },) #end div
    return sp


layout = side_panel()
