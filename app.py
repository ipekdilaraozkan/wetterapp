import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from meteostat import Point, Daily
import pandas as pd

# Streamlit app title
st.title("Aachen Historical Weather Data")

# Function to get the start and end date based on user's choice
def get_time_period(option):
    today = datetime.today()

    if option == 'Last Week':
        start_date = today - timedelta(days=7)
    elif option == 'Last Month':
        start_date = today - timedelta(days=30)
    elif option == 'Last Three Months':
        start_date = today - timedelta(days=90)
    elif option == 'Last Six Months':
        start_date = today - timedelta(days=180)
    elif option == 'Last Year':
        start_date = today - timedelta(days=365)
    else:
        st.error("Invalid choice. Please select a valid option.")
        return None, None
    
    return start_date, today

# Function to plot weather data (temperature, rain, snow)
def plot_weather_data(data, plot_type):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if plot_type == 'Temperature':
        ax.plot(data.index, data['tavg'], marker='o', color='b')
        ax.set_title(f'Average Daily Temperature in Aachen')
        ax.set_ylabel('Temperature (°C)')
    elif plot_type == 'Rain':
        ax.plot(data.index, data['prcp'], marker='o', color='g')
        ax.set_title(f'Daily Rainfall in Aachen')
        ax.set_ylabel('Rainfall (mm)')
    elif plot_type == 'Snow':
        ax.plot(data.index, data['snow'], marker='o', color='c')
        ax.set_title(f'Daily Snowfall in Aachen')
        ax.set_ylabel('Snowfall (mm)')
    
    ax.set_xlabel('Date')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Fixed location (Aachen) for weather data
location = Point(50.7753, 6.0839, 200)

# Select a time period using Streamlit's selectbox
option = st.selectbox(
    "Select a time period for historical weather data:",
    ['Last Week', 'Last Month', 'Last Three Months', 'Last Six Months', 'Last Year']
)

# Get the start and end dates based on user input
start_date, end_date = get_time_period(option)

if start_date and end_date:
    # Fetch daily weather data
    data = Daily(location, start=start_date, end=end_date)
    data = data.fetch()

    # Check if the data is empty or not
    if data.empty:
        st.warning("No data available for the selected period.")
    else:
        # Convert dates using pd.to_datetime if needed
        data.index = pd.to_datetime(data.index)

        # Plot temperature, rain, and snow data
        st.subheader(f"Weather data from {start_date.date()} to {end_date.date()}")

        # Plot temperature data
        plot_weather_data(data, 'Temperature')

        # Plot rain data
        plot_weather_data(data, 'Rain')

        # Check for snowfall data: if all values are 0, skip plotting
        if data['snow'].sum() == 0:
            st.info("No snowfall recorded during the selected period.")
        else:
            # Plot snow data if there is any snowfall
            plot_weather_data(data, 'Snow')
