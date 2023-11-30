import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template_string, request
import plotly.graph_objs as go
from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load COVID-19 data
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = pd.read_csv(url)

# Create a Flask web application
app = Flask(__name__)

# Define a route to render the HTML page
@app.route('/', methods=['GET', 'POST'])
def render_dashboard():
    # Get the selected countries from the dropdowns (default to Australia and Brazil)
    selected_country1 = request.form.get('country1', 'Austrailia')
    selected_country2 = request.form.get('country2', 'Brazil')

    # Filter data for the selected countries
    country_data1 = df[df['Country/Region'] == selected_country1]
    country_data2 = df[df['Country/Region'] == selected_country2]

    # Extract the date columns
    dates = pd.to_datetime(country_data1.columns[4:], format='%m/%d/%y')

    # Extract the corresponding data for both countries
    cases1 = country_data1.iloc[:, 4:].sum().astype(int).values
    cases2 = country_data2.iloc[:, 4:].sum().astype(int).values

    # Create a line chart for cases
    fig = go.Figure()

    # Add lines for the selected countries
    fig.add_trace(go.Scatter(x=dates, y=cases1, mode='lines+markers', name=selected_country1))
    fig.add_trace(go.Scatter(x=dates, y=cases2, mode='lines+markers', name=selected_country2))

    # Customize the layout
    fig.update_layout(
        title_text="COVID-19 Cases Comparison",
        xaxis=dict(title_text="Date"),
        yaxis=dict(title_text="Total Cases"),
        paper_bgcolor='white',
        autosize=True,
        margin=dict(t=50, b=30, l=50, r=10),
    )

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    # Define a list of country options for the dropdowns
    country_options = df['Country/Region'].unique()
    country_options.sort()

    # Define an HTML template with improved styling
    template = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>COVID-19 Cases Comparison</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css">
        <style>
            
            body {{
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                padding: 20px;
                text-align: center;
            }}
            h1 {{
                color: #333;
            }}
            form {{
                margin-top: 20px;
            }}
            label, select, input[type="submit"] {{
                font-size: 16px;
                margin: 5px;
                padding: 5px;
            }}
            select {{
                width: 200px;
            }}
            #chartDiv {{
                margin-top: 30px;
                border:1px solid lightgrey;
            }}
            
        </style>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>COVID-19 Cases</h1>
        <form method="post">
            <label for="country1">Select the First Country:</label>
            <select name="country1" id="country1">
                {"".join([f'<option value="{country}" {"selected" if country == selected_country1 else ""}>{country}</option>' for country in country_options])}
            </select>
            <label for="country2">Select the Second Country:</label>
            <select name="country2" id="country2">
                {"".join([f'<option value="{country}" {"selected" if country == selected_country2 else ""}>{country}</option>' for country in country_options])}
            </select>
            <input type="submit" value="Compare">
        </form>
        <div id="chartDiv">
            {plot_html}
        </div>
    </body>
    </html>
    '''

    return render_template_string(template)

server = Flask(__name__)

# Initialize Dash on your Flask server
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/')

# Define a dark theme for your layout
app.layout = html.Div(style={'backgroundColor': '#111', 'color': '#fff'}, children=[
    html.H1('COVID-19 Cases Dashboard', style={'textAlign': 'center', 'color': '#7FDBFF'}),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in sorted(df['Country/Region'].unique())],
        value=['Australia', 'Brazil'],  # default value
        multi=True,
        style={'backgroundColor': '#333', 'color': '#000000'}
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
    server.run(debug=True)