from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)
#Datasets setup
vacData = pd.read_csv("datasets/vacDataClean.csv") #Main dataframe w/ all vaccine data
vacTotal = pd.read_csv("datasets/vacTotalData.csv")#Second dataframe w/ only total data
countryTotal = pd.read_csv("datasets/totalCountry.csv")#Third dataframe w/ only country total data
ERTotal = pd.read_csv('datasets/totalReceivedExported.csv')#4th dataframe w/ only exported and received doses by countries data

#Infile styling
colors = {
    'background': '#161a1d',
    'text': 'rgb(184, 184, 184)',
    'trace1':'#119dff',
    'trace2':'#1D9F65',
}

#Figure Setup
pieColors = [
    
]
pieChart = go.Figure(
                    data=[
                        go.Pie(labels=ERTotal.Countries,values=ERTotal.ReceivedTotal)
                        ],
                    layout=dict(title=dict(text='Doses Received by each countries :'))
        )
pieChart.update_layout( #pie chart styling
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font=dict(family='Century Gothic'),
    font_color=colors['text'],
    uniformtext_minsize=12, 
    uniformtext_mode='hide',
    title_x=0.5,
    title_xanchor = 'center',
    title_y=1,
    title_yanchor = 'top',
)
pieChart.update_traces( #Pie chart display options
    hoverinfo='label+percent', 
    textinfo='label',
    textposition='inside',
    marker=dict(line=dict(color='#000000', width=2))
)

#App Layout
app.layout = html.Div(children=[
    
    html.H1(
        className="app-header--title",
        children='Covid-19 Vaccination and Transmission', # H1 Title
        ),
    
    html.Div(className='dropdownMenu',children=[ # div for the dropdwn menu 
        html.Label('Choose the Graph you want to display :'), 
        dcc.Dropdown(['Total Vaccine Stats',
                    'Vaccination by Year and Week',
                    'Vaccination by countries'
                    ],
                    'Total Vaccine Stats',
                    searchable = False,
                    id='graph_selector'
                    ),
        html.Br(),
    ]),
    
    html.Div(className='graphs',children=[ # div for the graphs
        dcc.Graph(
            id = 'graph',
        ),
        dcc.Graph(
            id = 'pieChart',
            figure=pieChart,
        ),
        dcc.RadioItems(
                        [
                            'Doses Received',
                            'Doses Exported',
                        ],
                        'Doses Received',
        ),
    ]),
    
])


@app.callback( #Callback outputs the graph selected in input
    Output('graph','figure'),
    Input('graph_selector','value')
)
def update_figure(graph_selector):
    if graph_selector == 'Vaccination by Year and Week': #generate Year Week vaccine histogram if selected in dropdown menu
        fig = vacYearFigure = go.Figure(
            data=[
                go.Histogram(x=vacData.YearWeek, y= vacData.FirstDose,name='First Dose',marker_color=colors['trace1']),
                go.Histogram(x=vacData.YearWeek, y= vacData.SecondDose,name='Second Dose',marker_color=colors['trace2'])
            ],
            layout=dict(title=dict(text='Vaccination by Year and Week'))
        )
        vacYearFigure.update_layout( #year graph layout
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font=dict(family='Century Gothic'),
            font_color=colors['text'],
            title_x=0.5,
            title_xanchor = 'center'
        )
        
    elif graph_selector == 'Vaccination by countries': #generate country vaccine histogram if selected in dropdown menu 
        fig = vacCountryFigure = go.Figure(
            data=[
                go.Bar(x=countryTotal.Countries, y= countryTotal.FirstTotal,name='First Dose',marker_color=colors['trace1']),
                go.Bar(x=countryTotal.Countries, y= countryTotal.SecondTotal,name='Second Dose',marker_color=colors['trace2'])
            ],
            layout=dict(title=dict(text='Vaccination by Countries'))
        )
        vacCountryFigure.update_layout( #country graph layout
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font=dict(family='Century Gothic'),
            font_color=colors['text'],
            title_x=0.5,
            title_xanchor = 'center'
        )
    else: #generate total vaccine bar chart if selected in dropdown menu
        fig = vacTotalFigure = go.Figure(
            data=[
                go.Bar(x = vacTotal.Vaccine, y = vacTotal.FirstTotal,name='First Dose',marker_color=colors['trace1']),
                go.Bar(x = vacTotal.Vaccine, y = vacTotal.SecondTotal,name='Second Dose',marker_color=colors['trace2'])
                ],
            layout=dict(title=dict(text='Total of people vaccinated by each Vaccine :'))
        )
        vacTotalFigure.update_layout( #total graph layout
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font=dict(family='Century Gothic'),
            font_color=colors['text'],
            title_x=0.5,
            title_xanchor = 'center'
        )
        
        
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)