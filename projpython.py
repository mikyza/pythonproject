# covid_tracker.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load data
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)

# 2. Basic info
print(df.columns)
print(df.head())

# 3. Data Cleaning
df['date'] = pd.to_datetime(df['date'])
# Select relevant columns
data = df[['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations', 'people_vaccinated']]

# Filter out aggregate locations like continents and world summary
data = data[~data['location'].isin(['World', 'Asia', 'Europe', 'Africa', 'North America', 'South America', 'Oceania'])]

# 4. Global total cases over time
global_data = data.groupby('date').sum().reset_index()

plt.figure(figsize=(12,6))
plt.plot(global_data['date'], global_data['total_cases'], label='Total Cases')
plt.plot(global_data['date'], global_data['total_deaths'], label='Total Deaths')
plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Global COVID-19 Total Cases and Deaths Over Time')
plt.legend()
plt.show()

# 5. Top 10 countries by total cases (latest date)
latest_date = data['date'].max()
latest_data = data[data['date'] == latest_date]
top10 = latest_data.sort_values('total_cases', ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(data=top10, x='total_cases', y='location')
plt.title('Top 10 Countries by Total COVID-19 Cases')
plt.xlabel('Total Cases')
plt.ylabel('Country')
plt.show()

# 6. Vaccination trends for a few countries
countries = ['United States', 'India', 'Brazil', 'United Kingdom', 'Germany']
vacc_data = data[data['location'].isin(countries)]

plt.figure(figsize=(12,6))
sns.lineplot(data=vacc_data, x='date', y='total_vaccinations', hue='location')
plt.title('Vaccination Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.show()

# 7. Correlation example: cases vs vaccinations on latest date for these countries
corr_data = latest_data[latest_data['location'].isin(countries)][['location', 'total_cases', 'total_vaccinations']]
print(corr_data)
print("Correlation between total cases and total vaccinations:",
      corr_data['total_cases'].corr(corr_data['total_vaccinations']))
