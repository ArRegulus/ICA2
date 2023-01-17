import pathlib
from dash import Dash, dcc, html 
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
app = Dash(__name__)
df = pd.read_csv("ICA2\datasets/vacDataClean.csv")

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
fig = px.bar(df, x= 'YearWeek', y=['FirstDose','SecondDose'],barmode='group')

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(
        children='Covid-19 Vaccination and Transmission',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
        ),
    
    html.Div(children='''
        C19 data
    '''),
    
    dcc.Graph(
        id = 'graph1',
        figure = fig,
    )
])
if __name__ == '__main__':
    app.run_server(debug=True)