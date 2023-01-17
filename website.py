import pathlib
from dash import Dash, dcc, html 
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
app = Dash(__name__)
vacData = pd.read_csv("ICA2\datasets/vacDataClean.csv")
vacTotal = pd.read_csv("ICA2\datasets/vacTotalData.csv")
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(
        children='Covid-19 Vaccination and Transmission',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
        ),
    
    html.Label('Choose Graph'),
    dcc.Dropdown(['Total Vaccine Stats', 'Vaccination by Countries', 'Transmission'], 'Total Vaccine Stats',id='graph_selector'),
    html.Br(),
    
    dcc.Graph(
        id = 'graph',
    ),
    dcc.Slider(
        vacData.YearWeek[0],
        vacData.YearWeek[201949],
        step = None,
        id = 'yearWeekSlider',
        value = vacData.YearWeek[201949],
        marks = {str(yearWeek): str(yearWeek) for yearWeek in vacData.YearWeek.unique()}
    )
])
@app.callback(
    Output('graph','figure'),
    Input('graph_selector','value')
)
def update_figure(graph_selector):
    if graph_selector == 'Total Vaccine Stats':
        fig = vacTotalFigure = go.Figure(
        data=[
            go.Bar(x = vacTotal.Vaccine, y = vacTotal.FirstTotal,name='First Dose'),
            go.Bar(x = vacTotal.Vaccine, y = vacTotal.SecondTotal,name='Second Dose')
            ],
        layout=dict(title=dict(text='Total of people vaccinated with such Vaccine'))
        )
        vacTotalFigure.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            title_xref='container',
        )
    elif graph_selector == 'Vaccination by Countries':
        fig = vacCountryFigure = go.Figure(
            data=[
                go.Bar(x=vacData.YearWeek, y= vacData.FirstDose,hovertext=vacData.Country,name='First Dose'),
                go.Bar(x=vacData.YearWeek, y= vacData.SecondDose,hovertext=vacData.Country,name='Second Dose')
            ],
            layout=dict(title=dict(text='Vaccination each week in different countries'))
        )
        vacCountryFigure.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            title_xref='container',
        )
    
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)