import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = pd.read_csv(url)

# Filter data for a specific country
country_name = 'United States'
country_data = df[df['Country/Region'] == country_name]

# Extract the date columns
dates = country_data.columns[4:]

# Extract the corresponding data
cases = country_data.iloc[:, 4:].sum().values

plt.figure(figsize=(10, 6))
plt.plot(dates, cases, marker='o')
plt.title("COVID-19 Cases Over Time in Your Country")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.ylabel("Total Cases")
plt.tight_layout()
plt.show()