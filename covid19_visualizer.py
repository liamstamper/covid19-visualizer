import pandas as pd
import plotly.express as px
from flask import Flask, render_template_string, request

# Load COVID-19 data
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = pd.read_csv(url)

# Create a Flask web application
app = Flask(__name__)

# Define a route to render the HTML page
@app.route('/', methods=['GET', 'POST'])
def render_dashboard():
    # Get the selected country from the dropdown (default to United States)
    selected_country = request.form.get('country', 'United States')

    # Filter data for the selected country
    country_data = df[df['Country/Region'] == selected_country]

    # Extract the date columns
    dates = pd.to_datetime(country_data.columns[4:], format='%m/%d/%y')

    # Extract the corresponding data
    cases = country_data.iloc[:, 4:].sum().astype(int).values

    # Create an interactive Plotly chart
    fig = px.line(x=dates, y=cases, markers=True, title=f"COVID-19 Cases in {selected_country}")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Total Cases")

    # Customize chart appearance
    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
        paper_bgcolor='white'
    )

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    # Define a list of country options for the dropdown
    country_options = df['Country/Region'].unique()
    country_options.sort()

    # Define an HTML template with improved styling
    template = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>COVID-19 Data Visualization</title>
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
            }}
        </style>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>COVID-19 Data Visualization</h1>
        <form method="post">
            <label for="country">Select a Country:</label>
            <select name="country" id="country">
                {"".join([f'<option value="{country}" {"selected" if country == selected_country else ""}>{country}</option>' for country in country_options])}
            </select>
            <input type="submit" value="Submit">
        </form>
        <div id="chartDiv">
            {plot_html}
        </div>
    </body>
    </html>
    '''

    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)
