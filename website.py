from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)

vacData = pd.read_csv("ICA2\datasets/vacDataClean.csv") #Main dataframe w/ all vaccine data
vacTotal = pd.read_csv("ICA2\datasets/vacTotalData.csv")#Second dataframe w/ only total data
countryTotal = pd.read_csv("ICA2\datasets/totalCountry.csv")#Third dataframe w/ only country total data

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    
    html.H1(
        children='Covid-19 Vaccination and Transmission', # H1 Title
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
        ),
    
    html.Label('Choose Graph'), #Dropdown menu 
    dcc.Dropdown(['Total Vaccine Stats',
                  'Vaccination by Year and Week',
                  'Vaccination by countries'
                  ],
                 'Total Vaccine Stats',
                 id='graph_selector'
                 ),
    html.Br(),
    
    dcc.Graph(
        id = 'graph',
    ),
    
    """ dcc.Slider(                 #Slider to modify the Year/Week displayed on the graph 
        vacData.YearWeek[0], #slider min
        vacData.YearWeek[201949], #slider max
        step = None,
        id = 'yearWeekSlider',
        value = vacData.YearWeek[(201949//2)], #default value
        marks = {str(yearWeek): str(yearWeek) for yearWeek in vacData.YearWeek.unique()} #not working
    ) """
    
    
])


@app.callback( #Callback outputs the graph selected in input
    Output('graph','figure'),
    Input('graph_selector','value')
)
def update_figure(graph_selector):
    if graph_selector == 'Total Vaccine Stats': #generate total vaccine bar chart if selected in dropdown menu
        fig = vacTotalFigure = go.Figure(
        data=[
            go.Bar(x = vacTotal.Vaccine, y = vacTotal.FirstTotal,name='First Dose'),
            go.Bar(x = vacTotal.Vaccine, y = vacTotal.SecondTotal,name='Second Dose')
            ],
        layout=dict(title=dict(text='Total of people vaccinated with such Vaccine'))
        )
        vacTotalFigure.update_layout( #total graph layout
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            title_xref='container',
        )
        
    elif graph_selector == 'Vaccination by Year and Week': #generate Year Week vaccine histogram if selected in dropdown menu
        fig = vacYearFigure = go.Figure(
            data=[
                go.Histogram(x=vacData.YearWeek, y= vacData.FirstDose,name='First Dose'),
                go.Histogram(x=vacData.YearWeek, y= vacData.SecondDose,name='Second Dose')
            ],
            layout=dict(title=dict(text='Vaccination by Year and Week'))
        )
        vacYearFigure.update_layout( #year graph layout
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            title_xref='container',
        )
        
    elif graph_selector == 'Vaccination by countries': #generate country vaccine histogram if selected in dropdown menu 
        fig = vacCountryFigure = go.Figure(
            data=[
                go.Bar(x=countryTotal.Countries, y= countryTotal.FirstTotal,name='First Dose'),
                go.Bar(x=countryTotal.Countries, y= countryTotal.SecondTotal,name='Second Dose')
            ],
            layout=dict(title=dict(text='Vaccination by Countries'))
        )
        vacCountryFigure.update_layout( #country graph layout
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            title_xref='container',
        )
        
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)