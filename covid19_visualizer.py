import pandas as pd
import plotly.graph_objs as go
from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load COVID-19 data
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = pd.read_csv(url)

# Create a Flask web application
server = Flask(__name__)

# Initialize Dash on your Flask server
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/')

# Define a dark theme for your layout
app.layout = html.Div(style={'backgroundColor': '#111', 'color': '#fff'}, children=[
    html.H1('COVID-19 Cases Dashboard', style={'textAlign': 'center', 'color': '#7FDBFF'}),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in sorted(df['Country/Region'].unique())],
        value=['Afghanistan', 'Brazil'],  # default value
        multi=True,
        style={'backgroundColor': '#333', 'color': '#fff'}
    ),
    dcc.Graph(id='covid-cases-linechart'),
])

# Define callback to update graph
@app.callback(
    Output('covid-cases-linechart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_graph(selected_countries):
    traces = []
    for country in selected_countries:
        country_data = df[df['Country/Region'] == country]
        dates = pd.to_datetime(country_data.columns[4:], format='%m/%d/%y')
        cases = country_data.iloc[:, 4:].sum().astype(int).values
        traces.append(go.Scatter(x=dates, y=cases, mode='lines+markers', name=country))

    figure = {
        'data': traces,
        'layout': go.Layout(
            title='COVID-19 Cases Over Time',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Number of Cases'},
            paper_bgcolor='#111',
            plot_bgcolor='#111',
            font={'color': '#fff'},
        ),
    }
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
