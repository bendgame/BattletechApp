import pandas as pd
import re
#import dash
import plotly
# import dash_core_components as dcc
# import dash_html_components as html 
import dash_bootstrap_components as dbc 
# import dash_table
# from dash.dependencies import Input, Output
import plotly.graph_objs as go

from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL


df = pd.read_csv(r"BTdata.csv", header = 0)

df = df.drop(columns=['Unnamed: 0'])

df['Type']=df['Type'].astype(str)
df['Abilities']=df['Abilities'].astype(str)
df['Move']=df['Move'].astype(str)
df['Type'] = [v.replace('bm', 'BM') for v in df['Type']]

df = df.sort_values('Name')
df = df.reset_index()
df = df.drop(columns=['index'])

bmm1 = df.loc[(df['Size']==1) & (df['Type']=='BM')]
bmm2 = df.loc[(df['Size']==2) & (df['Type']=='BM')]
bmm3 = df.loc[(df['Size']==3) & (df['Type']=='BM')]
bmm4 = df.loc[(df['Size']==4) & (df['Type']=='BM')]

me1 = pd.DataFrame(dict(
    r=[bmm1['Armor'].mean().round(2), bmm1['Structure'].mean().round(2), bmm1['TMM'].mean().round(2),  bmm1['Short'].mean().round(2), bmm1['Medium'].mean().round(2), bmm1['Long'].mean().round(2)],
    theta=['Armor','Structure','TMM', 'Short','Medium','Long']))
me2 = pd.DataFrame(dict(
    r=[bmm2['Armor'].mean().round(2), bmm2['Structure'].mean().round(2), bmm2['TMM'].mean().round(2),  bmm2['Short'].mean().round(2), bmm2['Medium'].mean().round(2), bmm2['Long'].mean().round(2)],
    theta=['Armor','Structure','TMM', 'Short','Medium','Long']))
me3 = pd.DataFrame(dict(
    r=[bmm3['Armor'].mean().round(2), bmm3['Structure'].mean().round(2), bmm3['TMM'].mean().round(2),  bmm3['Short'].mean().round(2), bmm3['Medium'].mean().round(2), bmm3['Long'].mean().round(2)],
    theta=['Armor','Structure','TMM', 'Short','Medium','Long']))
me4 = pd.DataFrame(dict(
    r=[bmm4['Armor'].mean().round(2), bmm4['Structure'].mean().round(2), bmm4['TMM'].mean().round(2),  bmm4['Short'].mean().round(2), bmm4['Medium'].mean().round(2), bmm4['Long'].mean().round(2)],
    theta=['Armor','Structure','TMM', 'Short','Medium','Long']))
