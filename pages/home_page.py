import pandas as pd
import plotly.express as px
from dash import html, dcc, Output, Input, callback, dash_table
from .data_base_connections import get_mysql_data
from .data_processing import dtypes_modifications
from .risk_index import risk_index
from .queries import *
import dash

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__, external_stylesheets=external_stylesheets)
dash.register_page(__name__, path='/')

# def home_page_layout():
    
layout = html.Div([
        html.Div([html.H2('MSHA Dashboard')], id = 'title1'),
        
        html.Div([
            html.Div([
                html.H4(children='Number of affected people',
                        style={'textAlign': 'center',
                            'color': 'white'}),
                html.P(f"{get_no_affected():,.0f}",
                        style={'textAlign': 'center',
                            'color': 'orange',
                            'fontSize':30}),

            ], className='card_container three columns'),

            html.Div([
                html.H4(children='Amount of Penalty',
                        style={'textAlign': 'center',
                            'color': 'white'}),
                html.P(f"{get_penalty():,.0f}",
                        style={'textAlign': 'center',
                            'color': '#dd1e35',
                            'fontSize': 30}),

            ], className='card_container three columns'),

            html.Div([
                html.H4(children='Inspection hours',
                        style={'textAlign': 'center',
                            'color': 'white'}),
                html.P(f"{get_insp_hours():,.0f}",
                        style={'textAlign': 'center',
                            'color': 'green',
                            'fontSize': 30}),

            ], className='card_container three columns'),

            html.Div([
                html.H4(children='Number of violations',
                            style={'textAlign': 'center',
                                'color': 'white'}),
                html.P(f"{get_violations():,.0f}",
                            style={'textAlign': 'center',
                                'color': '#e55467',
                                'fontSize': 30}),
            ], className='card_container three columns'),

        ], className='row flex display'),
        html.Div([
            html.Div([
                html.Div([
                dcc.Dropdown(id='data_set_chosen', multi=False,value='mines',
                            options=[{'label':'Mines Data', 'value':'mines'},
                                    {'label':'Violations Data', 'value':'violations'},
                                    {'label':'Accidents Data', 'value':'accidents'},
                                    {'label':'Address of Record Data', 'value':'addressofrecord'}, 
                                    {'label':'Area Samples Data', 'value':'areasamples'},
                                    {'label':'Assessed Violations Data', 'value':'assessedviolations'},
                                    {'label':'Civil Penalty Docket Decisions Data', 'value':'civilpenaltydocketsdecisions'},
                                    {'label':'Coal Dust Samples Data', 'value':'coaldustsamples'},
                                    {'label':'Conferences Data', 'value':'conferences'},
                                    {'label':'Contested Violations Data', 'value':'contestedviolations'},
                                    {'label':'Contractor Production Yearly Data', 'value':'contractorprodyearly'},
                                    {'label':'Contractor Production Quarterly Data', 'value':'contractorprodquarterly'},
                                    {'label':'Controller Operator History Data', 'value':'controlleroperatorhistory'},
                                    {'label':'Inspections Data', 'value':'inspections'},
                                    {'label':'Mines Production Quarterly Data', 'value':'minesprodquarterly'},
                                    {'label':'Mines Production Yearly Data', 'value':'minesprodyearly'},
                                    {'label':'Noise Samples Data', 'value':'noisesamples'},
                                    {'label':'Personal Health Samples Data', 'value':'personalhealthsamples'},
                                    {'label':'Quartz Samples Data', 'value':'quartzsamples'},
                                    {'label':'Mines Production Yearly Data', 'value':'minesprodyearly'}])         
                        ]),   
                    html.Div(id='table_placeholder', children=[])
                ],className='create_container2 six columns'),
                html.Div([
                    html.Div([
                        html.H4("Choose X axis"),
                        dcc.Dropdown(
                            placeholder="select X axis column",
                            id='xaxis_column'
                        )
                        ,
                        dcc.Checklist(
                            ['Groupby'],
                            id='xaxis_type',
                            inline=True
                        )
                    ]),
                    html.Div([
                        html.H4("Choose Y axis"),
                        dcc.Dropdown(
                            placeholder="select Y axis column",
                            id='yaxis_column'
                        )
                    ])
                ],className='create_container2 six columns'),
            ], className='row flex-display'),

        html.Div([  
            html.Div([
                html.Div([
                    html.H4("Statistics")])
                ],className='create_container2 six columns'),
            html.Div([
                html.Div([
                    dcc.Graph(id='indicator-graphic')])
                ],className='create_container2 six columns'),
            ], className='row flex-display'),
        html.Div([
            html.Div([
            
                html.H4("Risk index"),
                dcc.RangeSlider(2010, 2020, 1, value=[2011,2014], id='year',marks=None,
                    tooltip={"placement": "bottom", "always_visible": True}),
                html.Div( id='risk_index_table_placeholder', children=[])
            ], className='create_container2 six columns'),
            html.Div([
                html.Div([
                        html.H4("Choose Mine Id"),
                        dcc.Dropdown(
                            placeholder="select Mine Id",
                            id='risk_mine_id'
                        ),
                        dcc.Graph(id='risk_index_plot')
                    ])    
                ], className='create_container2 six columns'),
            ], className='row flex-display'),
            
        # dcc.Store inside the user's current browser session
        dcc.Store(id='store_data', data=[],storage_type='memory'), # 'local' or 'session'
        # dcc.Store inside the user's current browser session
        dcc.Store(id='store_risk_data', data=[],storage_type='memory'), # 'local' or 'session'
    ])
    # return layout

@callback(
    Output('store_data', 'data'),
    Input('data_set_chosen', 'value')
)
def store_data(data_set_chosen):
    if data_set_chosen == None:
        return {}
    query = "Select * from "+data_set_chosen+" limit 1000;"
    df = get_mysql_data(query)
    if data_set_chosen=="violations":
        dtypes_modifications(df)
    return df.to_dict('records')

@callback(
    Output('yaxis_column', 'options'),
    Output('xaxis_column', 'options'),
    Input('store_data', 'data')
)
def drop_down(store_data):
    if store_data == None :
        return [[],[]]
    columns = pd.DataFrame(store_data).columns
    return [columns,columns]
    
@callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis_column', 'value'),
    Input('yaxis_column', 'value'),
    Input('xaxis_type', 'value'),
    Input('store_data', 'data'))
def update_graph(xaxis_column, yaxis_column,
                 xaxis_type,store_data):
    dff = pd.DataFrame(store_data)
    if xaxis_column==None or yaxis_column == None or store_data ==None:
        return {}
    if xaxis_type==["Groupby"]:
        dff = dff.groupby(xaxis_column).sum().reset_index()
    fig = px.scatter(x=dff[xaxis_column],
                     y=dff[yaxis_column])

    return fig

@callback(
    Output('risk_index_plot', 'figure'),
    Input('risk_mine_id', 'value'),
    Input('store_risk_data', 'data'))
def update_graph111(risk_mine_id,store_risk_data):
    if store_risk_data == None :
        return {}
    df = pd.DataFrame(store_risk_data)
    if risk_mine_id == None :
        return {}
    df=df[df["MINE_ID"]==risk_mine_id]
    print(df[["CAL_YR","Risk_Index"]])    
    fig = px.scatter(x=df["CAL_YR"],
                     y=df["Risk_Index"],)

    return fig

@callback(
    Output('table_placeholder', 'children'),
    Input('store_data', 'data')
)
def table_view_sample_data(store_data):
    if store_data==None:
        return {}
    dff = pd.DataFrame(store_data) 
    my_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dff.columns],
        data=dff.head().to_dict('records'),
        virtualization=True,
        style_cell={'textAlign': 'left',
                    'min-width': '100px',
                    'backgroundColor': '#1f2c56',
                    'color': '#FEFEFE',
                    'border-bottom': '0.01rem solid #19AAE1'},
        style_header={'backgroundColor': '#1f2c56',
                    'fontWeight': 'bold',
                    'font': 'Lato, sans-serif',
                    'color': 'orange',
                    'border': '#1f2c56'},
        style_as_list_view=True,
        style_data={'styleOverflow': 'hidden', 'color': 'white'},
        fixed_rows={'headers': True},
        sort_action='native',
        sort_mode='multi'
    )
    return my_table 

@callback(
    Output('store_risk_data', 'data'),
    Output('risk_index_table_placeholder', 'children'),
    Input('year', 'value')
)
def risk_index_callback(year):
    dff=risk_index(year)
    print(dff)
    my_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dff.columns],
        data=dff.head().to_dict('records'),
        virtualization=True,
        style_cell={'textAlign': 'left',
                    'min-width': '100px',
                    'backgroundColor': '#1f2c56',
                    'color': '#FEFEFE',
                    'border-bottom': '0.01rem solid #19AAE1'},
        style_header={'backgroundColor': '#1f2c56',
                    'fontWeight': 'bold',
                    'font': 'Lato, sans-serif',
                    'color': 'orange',
                    'border': '#1f2c56'},
        style_as_list_view=True,
        style_data={'styleOverflow': 'hidden', 'color': 'white'},
        fixed_rows={'headers': True},
        sort_action='native',
        sort_mode='multi'
    )
    return [dff.to_dict('records'),my_table ] 

@callback(
    Output('risk_mine_id', 'options'),
    Input('store_risk_data', 'data')
)
def drop_down_mine_id(store_risk_data):
    df = pd.DataFrame(store_risk_data)
    columns = list(set(df.MINE_ID))
    return columns

# home_page_layout()
# if __name__ == '__main__':
#     run_server(debug=True,port=8050)