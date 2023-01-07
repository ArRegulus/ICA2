import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()
vacData = pd.read('datasets/vacData.csv')
app.layout = html.Div(children=[
    html.H1(children='Covid-19 Data'),
    html.Div(children=''' '''),
    dcc.Graph(
        id='Vaccine',
        figure={
            'data': [
                go.Bar(x = [1, 2, 3], y = [4, 1, 2], name ='Cherbourg'),
                go.Bar(x = [1, 2, 3], y = [2, 4, 5], name = 'Queenstown'),
                go.Bar(x = [1, 2, 3], y = [3, 2, 3], name = 'Southampton')
            ],
            'layout': {
                'title': 'Vaccine coverage',
                'x_axis':{'title': 'Region'},
                'y_axis':{'title': 'Number of vaccinated people'}
            }
        }
    )
])
if __name__ == '__main__':
    app.run_server(debug=True)