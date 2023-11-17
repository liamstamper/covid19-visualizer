import pandas as pd
import plotly.express as px
from flask import Flask, render_template_string

# Load COVID-19 data
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = pd.read_csv(url)

# Create a Flask web application
app = Flask(__name__)

# Define a route to render the HTML page
@app.route('/')
def render_dashboard():
    # Filter data for a specific country
    country_name = 'United States'
    country_data = df[df['Country/Region'] == country_name]

    # Extract the date columns
    dates = pd.to_datetime(country_data.columns[4:], format='%m/%d/%y')

    # Extract the corresponding data
    cases = country_data.iloc[:, 4:].sum().astype(int).values

    # Create an interactive Plotly chart
    fig = px.line(x=dates, y=cases, markers=True, title=f"COVID-19 Cases in {country_name}")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Total Cases")

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    # Define an HTML template
    template = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>COVID-19 Data Visualization</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>COVID-19 Data Visualization</h1>
        <div id="chartDiv">
            {plot_html}
        </div>
    </body>
    </html>
    '''

    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)
