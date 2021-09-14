# import dash
import plotly
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_table
# from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import plotly.express as px
# import sqlite3
import pandas as pd
# from app import app
from tabs import sidepanel, tab1, tab2#, tab3
from database import transforms

import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = sidepanel.layout

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.layout
    elif tab == 'tab-2':
       return tab2.layout
    # elif tab == 'tab-3':
    #   return tab3.layout

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
                        # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value
    return [None] * 3

@app.callback(
    Output('table-sorting-filtering', 'data')
    , [Input('table-sorting-filtering', "page_current")
     , Input('table-sorting-filtering', "page_size")
     , Input('table-sorting-filtering', 'sort_by')
     , Input('table-sorting-filtering', 'filter_query')
     , Input('battlemech-only', 'value')
     , Input('points-slider', 'value')
     , Input('role-drop', 'value')
    #  , Input('type-drop', 'value')
    #  , Input('ability-drop', 'value')
    #  , Input('move-drop', 'value')
    #  , Input('size-drop', 'value')
    # , Input('shortdamage-slider', 'value')
    # , Input('mediumdamage-slider', 'value')
    # , Input('longdamage-slider', 'value')
    # , Input('ability-input', 'value')
    ])
def update_table(page_current, page_size, sort_by, filter, bmcheck, points, role): #, type, abilities, tmm, size, short, medium,long,ability): #
    filtering_expressions = filter.split(' && ')
    dff = transforms.df
    print(bmcheck)
    low = points[0]
    high = points[1]

    # sl = short[0]
    # sh = short[1]

    # ml = medium[0]
    # mh = medium[1]

    # ll = long[0]
    # lh = long[1]

    dff = dff.loc[(dff['Points'] >= low) & (dff['Points'] <= high)]
    # dff = dff.loc[(dff['Short'] >= sl) & (dff['Short'] <= sh)]
    # dff = dff.loc[(dff['Medium'] >= ml) & (dff['Medium'] <= mh)]
    # dff = dff.loc[(dff['Long'] >= ll) & (dff['Long'] <= lh)]
    
    if bmcheck == ['Y']:
        dff = dff.loc[dff['Type'] == 'BM']
    else:
        dff
    if role is None or role == []:
        dff
    else:
        dff = dff.loc[dff['Role'].isin(role)]
    
    # if type is None or type == []:
    #     dff
    # else:
    #     dff = dff.loc[dff['Type'].isin(type)]
    
    # if ability is None or ability == []:
    #     dff
    # else:
    #     dff = dff.loc[dff['Abilities'].str.contains(ability)==True]

    # if tmm is None or tmm == []:
    #     dff
    # else:
    #     dff = dff.loc[dff['TMM'].isin(tmm)]

    # if size is None or size == []:
    #     dff
    # else:
    #     dff = dff.loc[dff['Size'].isin(size)]
    
    # if abilities is None or abilities == []:
    #     dff
    # else:
    #     dff = dff.loc[dff['Abilities'].isin(abilities)]

 
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    page = page_current
    size = page_size
    
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')


@app.callback(
    Output('radar-graph', 'children')
    , [Input('table-sorting-filtering', "derived_virtual_data"),
        Input('table-sorting-filtering', "derived_virtual_selected_rows")
     ])
def update_radar(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    
    dff = transforms.df if rows is None else pd.DataFrame(rows)
    
    # print(derived_virtual_selected_rows)
    # print(rows[derived_virtual_selected_rows[0]])
    try:
        bm = rows[derived_virtual_selected_rows[0]]
        adf = pd.DataFrame(dict(
        r=[bm['Armor'], bm['Structure'], bm['TMM'],  bm['Short'], bm['Medium'], bm['Long']],
        theta=['Armor','Structure','TMM', 'Short','Medium','Long']))
    except:
        bm = []
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=transforms.me4['r'],
        theta=transforms.me4['theta'],
        fill='toself',
        name='Average Size 4 BM'
    ))
    fig.add_trace(go.Scatterpolar(
        r=transforms.me3['r'],
        theta=transforms.me3['theta'],
        fill='toself',
        name='Average Size 3 BM'
    ))
    fig.add_trace(go.Scatterpolar(
        r=transforms.me2['r'],
        theta=transforms.me2['theta'],
        fill='toself',
        name='Average Size 2 BM'
    ))
    fig.add_trace(go.Scatterpolar(
        r=transforms.me1['r'],
        theta=transforms.me1['theta'],
        fill='toself',
        name='Average Size 1 BM'
    ))
    try:
        fig.add_trace(go.Scatterpolar(
            r=adf['r'],
            theta=adf['theta'],
            fill='toself',
            name=bm['Name']
        ))
    except:
        fig.update_layout(
        polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 11]
        )),
        showlegend=True
        )

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 11]
        )),
    showlegend=True
    )

    return [dcc.Graph(id = 'graph2', figure=fig)]

@app.callback(Output('table-paging-with-graph-container', "children"),
[ Input('battlemech-only', 'value')
    , Input('points-slider', 'value')
    , Input('role-drop', 'value')
])
def update_graph(bmcheck,points, role):
    dff = transforms.df
    low = points[0]
    high = points[1]

    dff = dff.loc[(dff['Points'] >= low) & (dff['Points'] <= high)]
    
    if bmcheck == ['Y']:
        dff = dff.loc[dff['Type'] == 'BM']
    else:
        dff
    if role is None or role == []:
        dff
    else:
        dff = dff.loc[dff['Role'].isin(role)]
  
    fig = px.scatter(dff, x='Points', y='total', color="Points", marginal_y="box"
              ,  marginal_x="box", trendline="ols", hover_data = ['Name', 'Abilities']
              )
        
    return html.Div([
        dcc.Graph(
            id='rating-price'
            , figure=fig
        )
    ])

@app.callback(Output('scatter-matrix-container', "children"),
[     Input('battlemech-only', 'value')
     , Input('points-slider', 'value')
     , Input('role-drop', 'value')
    ])
def update_graph(bmcheck, points, role):
    dff = transforms.df
    low = points[0]
    high = points[1]

    dff = dff.loc[(dff['Points'] >= low) & (dff['Points'] <= high)]
    
    
    if bmcheck == ['Y']:
        dff = dff.loc[dff['Type'] == 'BM']
    else:
        dff
    if role is None or role == []:
        dff
    else:
        dff = dff.loc[dff['Role'].isin(role)]
    
    fig = px.scatter_matrix(dff, dimensions=["Points", "Size", "Armor", "Structure","TMM", "Short", "Medium", "Long"], color="Role" ,height = 1200)

    return html.Div([dcc.Graph(figure = fig)])

if __name__ == '__main__':
    app.run_server(debug = True, port = 8050)
