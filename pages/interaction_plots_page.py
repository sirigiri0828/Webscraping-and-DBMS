from matplotlib.pyplot import get
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input, callback, dash_table
from .data_base_connections import get_mysql_data
from .data_processing import dtypes_modifications
import dash

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__, external_stylesheets=external_stylesheets)
dash.register_page(__name__)

# def interaction_plots_layout():
layout = html.Div([
        html.Div([html.H3('MSHA Plots')], id = 'title2'),
        
        html.Div([
            html.Div([
                html.Div([
                dcc.Dropdown(id='data_set_chosen1', multi=False,value='violations',
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
                    html.Div(id='table-placeholder1', children=[])
                ],className='create_container1 twelve columns'),
            ], className='row flex-display'),
        
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Choose X axis"),
                        dcc.Dropdown(
                            placeholder="select X axis column",
                            id='xaxis-column1'
                        )
                        ,
                        dcc.Checklist(
                            ['Groupby'],
                            id='xaxis-type1',
                            inline=True
                        )
                    ]),
                    html.Div([
                        html.H3("Choose Y axis"),
                        dcc.Dropdown(
                            placeholder="select Y axis column",
                            id='yaxis-column1'
                        )
                    ])
                ]),
                ],className='create_container2 six columns'),
            html.Div([
                dcc.Graph(id='indicator-graphic1')
                ],className='create_container2 six columns')
        ], className='row flex-display'),
        html.Div([
            html.Div([
                dcc.Graph(id='graph1')
                ],className='create_container2 six columns'),
            html.Div([
                dcc.Graph(id='graph2')
                ],className='create_container2 six columns')
        ], className='row flex-display'),
        html.Div([
            html.Div([
                dcc.Graph(id='graph3')
                ],className='create_container2 six columns'),
            html.Div([
                dcc.Graph(id='graph4')
                ],className='create_container2 six columns')
        ], className='row flex-display'),
        # dcc.Store inside the user's current browser session
        dcc.Store(id='store-data1', data=[],storage_type='memory'), # 'local' or 'session'   
            
    ])
    # return layout


@callback(
    Output('store-data1', 'data'),
    Input('data_set_chosen1', 'value')
)
def store_data123(table_name):
    query = "Select * from "+table_name+" limit 1000;"
    df = get_mysql_data(query)
    if table_name=="violations":
        dtypes_modifications(df)
    return df.to_dict('records')

@callback(
    Output('yaxis-column1', 'options'),
    Output('xaxis-column1', 'options'),
    Input('store-data1', 'data')
)
def drop_down123(data):
    columns = pd.DataFrame(data).columns
    return [columns,columns]
    
@callback(
    Output('indicator-graphic1', 'figure'),
    Input('xaxis-column1', 'value'),
    Input('yaxis-column1', 'value'),
    Input('xaxis-type1', 'value'),
    Input('store-data1', 'data'))
def update_graph123(xaxis_column_name, yaxis_column_name,
                 xaxis_type,data):
    dff = pd.DataFrame(data)

    if xaxis_type==["Groupby"]:
        dff = dff.groupby(xaxis_column_name).sum().reset_index()
    if xaxis_column_name==None or yaxis_column_name==None:
        return {}
    fig = px.scatter(x=dff[xaxis_column_name],
                     y=dff[yaxis_column_name],)

    return fig

@callback(
    Output('graph1', 'figure'),
    Input('store-data1', 'data'))
def graph1231(data):
    df = pd.DataFrame(data)
    groupbycolumn = ["COAL_METAL_IND","CAL_YR"]
    lst = ['PROPOSED_PENALTY', 'NO_AFFECTED']
    df = pd.DataFrame(df.groupby(groupbycolumn)['PROPOSED_PENALTY', 'NO_AFFECTED'].sum()).reset_index()
    fig = px.scatter(df, x= "CAL_YR", y= "NO_AFFECTED" , symbol = "COAL_METAL_IND",facet_col="COAL_METAL_IND", color="COAL_METAL_IND", trendline="lowess", trendline_options=dict(frac=0.1), trendline_color_override="black",title="Number of affected people over the years")

    return fig

@callback(
    Output('graph2', 'figure'),
    Input('store-data1', 'data'))
def graph1232(data):
    df = pd.DataFrame(data)
    groupbycolumn = ["COAL_METAL_IND","CAL_YR"]
    lst = ['PROPOSED_PENALTY', 'NO_AFFECTED']
    df = pd.DataFrame(df.groupby(groupbycolumn)['PROPOSED_PENALTY', 'NO_AFFECTED'].sum()).reset_index()
    fig = px.histogram(df, x="CAL_YR", y="NO_AFFECTED", histfunc="avg", title="Histogram for average number of affected people over the years")
    fig.update_traces(xbins_size="M1")
    fig.update_xaxes(showgrid=True, ticklabelmode="period", dtick="M1", tickformat="%b\n%Y")
    fig.update_layout(bargap=0.2)
    return fig

@callback(
    Output('graph3', 'figure'),
    Input('store-data1', 'data'))
def graph1233(data):
    df = pd.DataFrame(data)
    groupbycolumn = ["COAL_METAL_IND","CAL_YR"]
    lst = ['PROPOSED_PENALTY', 'NO_AFFECTED']
    df = pd.DataFrame(df.groupby(groupbycolumn)['PROPOSED_PENALTY', 'NO_AFFECTED'].sum()).reset_index()
    fig = px.line(df, x='CAL_YR', y='NO_AFFECTED', title='Time series with number of affected people')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=1, label="5y", step="month", stepmode="backward"),
                dict(count=1, label="10y", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all")
        ])
    )
)
    return fig

@callback(
    Output('graph4', 'figure'),
    Input('store-data1', 'data'))
def graph1234(data):
    df = pd.DataFrame(data)
    groupbycolumn = ["COAL_METAL_IND","CAL_YR"]
    lst = ['PROPOSED_PENALTY', 'NO_AFFECTED']
    df = pd.DataFrame(df.groupby(groupbycolumn)['PROPOSED_PENALTY', 'NO_AFFECTED'].sum()).reset_index()
    fig = px.line(df, x='CAL_YR', y='NO_AFFECTED', title='Time series with number of affected people')
# Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="5y",
                        step="year",
                        stepmode="backward"),
                    dict(count=5,
                        label="10y",
                        step="year",
                        stepmode="backward"),
                    dict(count=10,
                        label="15y",
                        step="year",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
    return fig


@callback(
    Output('table-placeholder1', 'children'),
    Input('store-data1', 'data')
)
def table_view_sample_data123(data):
    # if data==None:
    #     return{}
    dff = pd.DataFrame(data) 
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

# interaction_plots_layout()
# if __name__ == '__main__':
#     run_server(debug=True,port=8050)