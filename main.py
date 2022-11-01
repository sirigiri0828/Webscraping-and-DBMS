from dash import Dash, html, dcc
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,external_stylesheets=external_stylesheets, use_pages=True)

app.layout = html.Div([    
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

    dash.page_container  
])

    
if __name__ == '__main__':
    app.run_server(debug=True,port=8051)