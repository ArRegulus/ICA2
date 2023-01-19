from dash import Dash, dcc, html, Input, Output
from pandas import read_csv
from plotly.graph_objects import Figure,Bar,Pie,Histogram

app = Dash(__name__)
#Datasets setup
vacData = read_csv("datasets/vacDataClean.csv") #Main dataframe w/ all vaccine data
vacTotal = read_csv("datasets/vacTotalData.csv")#Second dataframe w/ only total data
countryTotal = read_csv("datasets/totalCountry.csv")#Third dataframe w/ only country total data
ERTotal = read_csv('datasets/totalReceivedExported.csv')#4th dataframe w/ only exported and received doses by countries data

#Infile styling
colors = {
    'background': '#161a1d',
    'text': 'rgb(184, 184, 184)',
    'trace1':'#119dff',
    'trace2':'#1D9F65',
}

#Figure Setup
def pie_chart(labels,values,pieTitle): #Generates pie chart
    figure = Figure(
            data=[
                Pie(labels=labels,values=values)
                ],
            layout=dict(title=dict(text=pieTitle))
        )
    figure.update_layout( #pie chart styling
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
    figure.update_traces( #Pie chart display options
        hoverinfo='label+percent', 
        textinfo='label',
        textposition='inside',
        marker=dict(line=dict(color='#000000', width=2))
    )
    return figure

def bar_chart(x,y1,y2,xName,YName,barTitle):
    figure = Figure(
            data=[
                Bar(x=x, y= y1,name=xName,marker_color=colors['trace1']),
                Bar(x=x, y= y2,name=YName,marker_color=colors['trace2'])
            ],
            layout=dict(title=dict(text=barTitle))
        )
    figure.update_layout( #year graph layout
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(family='Century Gothic'),
        font_color=colors['text'],
        title_x=0.5,
        title_xanchor = 'center'
    )
    return figure
#App Layout
app.layout = html.Div(children=[
    
    html.H1(
        className="app-header--title",
        children='Covid-19 Vaccination', # H1 Title
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
        ),
        dcc.RadioItems(
                        [
                            'Doses Received',
                            'Doses Exported',
                        ],
                        'Doses Received',
                        id='pieRadio',
        ),
    ]),
    
])


@app.callback( #Callback outputs the graph selected in input
    Output('graph','figure'),
    Input('graph_selector','value'),
)
def update_figure(graph_selector):
    if graph_selector == 'Vaccination by Year and Week': #generate Year Week vaccine histogram if selected in dropdown menu
        fig = Figure(
            data=[
                Histogram(x=vacData.YearWeek, y= vacData.FirstDose,name='First Dose',marker_color=colors['trace1']),
                Histogram(x=vacData.YearWeek, y= vacData.SecondDose,name='Second Dose',marker_color=colors['trace2'])
            ],
            layout=dict(title=dict(text='Vaccination by Year and Week'))
        )
        fig.update_layout( #year graph layout
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font=dict(family='Century Gothic'),
            font_color=colors['text'],
            title_x=0.5,
            title_xanchor = 'center'
        )
        
    elif graph_selector == 'Vaccination by countries': #generate country vaccine histogram if selected in dropdown menu 
        fig = bar_chart(
            countryTotal.Countries,
            countryTotal.FirstTotal,
            countryTotal.SecondTotal,
            'First Dose',
            'Second Dose',
            'Vaccinations stats by countries'
            )
    else: #generate total vaccine bar chart if selected in dropdown menu
        fig = bar_chart(
            vacTotal.Vaccine,
            vacTotal.FirstTotal,
            vacTotal.SecondTotal,
            'First Dose',
            'Second Dose',
            'Total of people vaccinated with each vaccine'
            )
        
    return fig
@app.callback(
    Output('pieChart','figure'),
    Input('pieRadio','value'),
)
def update_pie(pieRadio):
    if pieRadio == 'Doses Exported':
        output = pie_chart(ERTotal.Countries,ERTotal.ExportedTotal,'Doses Exported by each countries :')
    else:
        output = pie_chart(ERTotal.Countries,ERTotal.ReceivedTotal,'Doses Received by each countries :')
        
    return output


if __name__ == '__main__':
    app.run_server(debug=True)