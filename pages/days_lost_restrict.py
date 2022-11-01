from matplotlib.pyplot import get
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input, callback, dash_table , State
from .data_base_connections import get_mysql_data
import dash
from .options import *

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__, external_stylesheets=external_stylesheets)
dash.register_page(__name__)

# def interaction_plots_layout():
layout = html.Div([
        html.Div([html.H3('MSHA DropDown')], id = 'title2'),
        
        html.Div([
            html.Div([
                html.Div([
                html.Div([html.H4('Year')], id = 'title2'),
                dcc.Dropdown(id='year',placeholder='Year', multi=True,value='select_all',
                            options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['year']),                   
                 
                        ]),   
                ],className='create_container1 three columns'),
            html.Div([
                html.Div([
                html.Div([html.H4('time')], id = 'title2'),
                    dcc.Dropdown(id='time',placeholder='Time', multi=True,value='select_all',
                                options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['time'])         
                            ]),   
                    ],className='create_container1 three columns'),
            html.Div([
                html.Div([
                html.Div([html.H4('operator or contractor')], id = 'title2'),
                    dcc.Dropdown(id='operator_contractor',placeholder='Contractor or Operator', multi=True,value='select_all',
                                options= [{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['operator_contractor'])      
                            ]),   
                    ],className='create_container1 three columns'),
            html.Div([
                html.Div([
                html.Div([html.H4('accident_date')], id = 'title2'),
                    dcc.Dropdown(id='accident_date',placeholder='Accident Date', multi=True,value='select_all',
                                options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['accident_date'])       
                            ]),   
                    ],className='create_container1 three columns'),
            ], className='row flex-display'),
        html.Br(),
        html.Div([
            html.Div([
                html.Div([
                html.Div([html.H4('state')], id = 'title2'),
                dcc.Dropdown(id='state',placeholder='State', multi=True,value='select_all',
                            options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['state'])       
                        ]),   
                ],className='create_container1 three columns'),
            html.Div([
                html.Div([
                html.Div([html.H4('mining method')], id = 'title2'),
                    dcc.Dropdown(id='mining_method',placeholder='Mining Method', multi=True,value='select_all',
                                options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['mining_method'])         
                            ]),   
                    ],className='create_container1 three columns'),
            html.Div([
                html.Div([
                html.Div([html.H4('mining type')], id = 'title2'),
                    dcc.Dropdown(id='mining_type',placeholder='Mining Type', multi=True,value='select_all',
                                options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['mining_type'])         
                            ]),   
                    ],className='create_container1 three columns'),
            html.Div([
                html.Div([
                html.Div([html.H4('miners occupation category')], id = 'title2'),
                    dcc.Dropdown(id='occupation_category',placeholder='Occupation Category', multi=True,value='select_all',
                                options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['occupation_category'])       
                            ]),   
                    ],className='create_container1 three columns'),
            ], className='row flex-display'),
        html.Br(),
        html.Div([
            html.Div([
                html.Div([
                html.Div([html.H4('activity category')], id = 'title2'),
                dcc.Dropdown(id='activity_category',placeholder='Activity Category', multi=True,value='select_all',
                            options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['activity_category'])         
                        ]),   
                ],className='create_container1 three columns'),
            html.Div([
                html.Div([
                html.Div([html.H4('nature of injury')], id = 'title2'),
                    dcc.Dropdown(id='nature_of_injury',placeholder='Nature of Injury', multi=True,value='select_all',
                                options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['nature_of_injury'])         
                            ]),   
                    ],className='create_container1 three columns'),
            html.Div([
                html.Div([
                html.Div([html.H4('injury body_part')], id = 'title2'),
                    dcc.Dropdown(id='injury_body_part',placeholder='Injury body parts', multi=True,value='select_all',
                                options=[{'label': 'Select All', 'value': 'select_all'}]+dropdown_options['injury_body_part'])         
                            ]),   
                    ],className='create_container1 three columns'),
            ], className='row flex-display'),
        html.Br(),
        html.Div([
            html.Button('Submit', id='submit-val', n_clicks=0),
            html.Br(),
            html.Div( id='table_placeholder3', children=[])
        ]),
        html.Br(),
        html.Br(),
        html.Div([
            html.Div([
                html.Div([
                html.Div([html.H4('Select column name')], id = 'title2'),
                    dcc.Dropdown(id='column_name',placeholder='',value='nature_of_injury',
                                options=list(dropdown_options.keys()))         
                            ]),   
                    ],className='create_container1 three columns'),
            html.Div([
                html.Div([
                html.Div([html.H4('Select column value')], id = 'title2'),
                    dcc.Dropdown(id='column_value',placeholder='Select Value', multi=True,value='select_all',
                                options=[])         
                            ]),   
                    ],className='create_container1 three columns'),
            ], className='row flex-display'),
        html.Br(),
        
        html.Div([
                dcc.Graph(id='graph124')
                ],className='create_container2 six columns'),
            
    ])

query = """
WITH req_accidents as 
(SELECT MINE_ID,ACCIDENT_DT AS accident_date,CAL_YR,ACCIDENT_TIME AS "time", ACTIVITY as activity_category, NATURE_INJURY as nature_of_injury, OCCUPATION AS occupation_category, INJ_BODY_PART as injury_body_part, COAL_METAL_IND as mining_method, DAYS_LOST, DAYS_RESTRICT from ACCIDENTS),
req_mines as 
(SELECT MINE_ID,COAL_METAL_IND,CURRENT_MINE_TYPE as mining_type, STATE as state FROM MINES),
req_violations as 
(SELECT VIOLATOR_TYPE_CD as operator_contractor, MINE_ID, NO_AFFECTED, CAL_YR FROM VIOLATIONS_100)

SELECT 
* 
FROM req_accidents 
JOIN req_mines
USING (MINE_ID) 
JOIN req_violations 
USING (MINE_ID,CAL_YR) """
df = get_mysql_data(query)

@callback(
    Output('column_value','options'),
    Input('column_name','value')
)
def col_vale(column_name):
    return dropdown_options[column_name] + [{'label': 'Select All', 'value': 'select_all'}]    

@callback(
    Output('graph124','figure'),
    Input('column_name','value'),
    Input('column_value','value')
)
def col_val_plot(column_name,column_value):
    column_filter=select_all_check(column_name,column_value)
    dff = df[df[column_name].isin(list(column_filter))] 
    groupbycolumn = [column_name]
    req_df = pd.DataFrame(dff.groupby(groupbycolumn)['DAYS_LOST', 'DAYS_RESTRICT'].sum()).reset_index()
    req_df['DAYS_LOST + DAYS_RESTRICT']=req_df['DAYS_LOST']+req_df['DAYS_RESTRICT']
    fig = px.bar(req_df, x= column_name, y= "DAYS_LOST + DAYS_RESTRICT" , title=" Sample Plot")

    return fig       

@callback(
    Output('table_placeholder3', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('year', 'value'),
    Input('time', 'value'),
    Input('operator_contractor', 'value'),
    Input('accident_date', 'value'),
    Input('state', 'value'),
    Input('mining_method', 'value'),
    Input('mining_type', 'value'),              
    Input('occupation_category', 'value'),
    Input('activity_category', 'value'),
    Input('nature_of_injury', 'value'),
    Input('injury_body_part', 'value')
    
)
def update_output(n_clicks, year,time, operator_contractor,accident_date,state,mining_method,mining_type,occupation_category,activity_category,nature_of_injury,injury_body_part):
    # fetch your data here with all 11 columns 
    # save the data in  df
    year_filter=select_all_check('year',year)
    time_filter=select_all_check('time',time)
    operator_contractor_filter=select_all_check('operator_contractor',operator_contractor)
    accident_date_filter=select_all_check('accident_date',accident_date)
    state_filter=select_all_check('state',state)
    mining_method_filter=select_all_check('mining_method',mining_method)
    mining_type_filter=select_all_check('mining_type',mining_type)
    occupation_category_filter=select_all_check('occupation_category',occupation_category)
    activity_category_filter=select_all_check('activity_category',activity_category)
    nature_of_injury_filter=select_all_check('nature_of_injury',nature_of_injury)
    injury_body_part_filter=select_all_check('injury_body_part',injury_body_part)
    # df=df[df['CAL_YR'].isin(year_filter) & df['CAL_YR'].isin(time_filter) & df['CAL_YR'].isin(year_filter) & df['CAL_YR'].isin(year_filter) & df['CAL_YR'].isin(year_filter) & df['CAL_YR'].isin(year_filter) & df['CAL_YR'].isin(year_filter) ]
    dff=df[["MINE_ID","DAYS_LOST","DAYS_RESTRICT","NO_AFFECTED"]]
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
