#### Import packages

import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt
import json

#### Set title and description of the page

st.set_page_config(page_title = 'NYC Bikes - Strategic Dashboard 2022', layout='wide')
st.title('NYC Bikes - Strategic Dashboard 2022')
st.markdown("The dashboard aims to summarize interesting metrics, diagnose problems and help identify areas of improvement for bike-sharing in NYC.")

#### Import the data

# Top20 Stations
df_top20 = pd.read_csv(
    "Output/Top20 Bike Stations - NYC 2022.csv",
    engine="pyarrow",                 # faster & lower memory
    dtype_backend="pyarrow",          # compact Arrow dtypes for ints/strings
)

# Trips VS Weather
df_weather = pd.read_csv(
    "Output/Ride Count VS Weather - NYC 2022.csv",
    engine="pyarrow",                 # faster & lower memory
    dtype_backend="pyarrow",          # compact Arrow dtypes for ints/strings
)

#### Display the charts

## Plot the top20 in a bar chart

# Make a nice color scale that stays clear from the whites

green_scale = px.colors.sequential.Greens[3:]


# Create the figure object

fig_top20 = go.Figure(go.Bar(
    x = df_top20['start_station_name'], 
    y = df_top20['trips'],
    marker=dict(
        color=df_top20['trips'],
        colorscale=green_scale
    )
))


# Add title and clean labels

fig_top20.update_layout(
     title = 'Top 20 most popular bike stations in NYC in 2022',
     xaxis_title = 'Start stations',
     yaxis_title ='Sum of trips',
     width = 900, height = 600)


st.plotly_chart(fig_top20, use_container_width = True)

## Plot the number of rides VS temperature in a dual plot
# Create the figure object that will host the 2 plots

fig_weather = make_subplots(specs = [[{"secondary_y": True}]])

# Add the first subplot: temperature

fig_weather.add_trace(
    go.Scatter(
        x = df_weather['date'], 
        y = df_weather['avgTemp'], 
        name = 'Daily Average Temperature', 
        marker={'color': df_weather['avgTemp'],'color': 'red'}),
    secondary_y = False)

# Add the second subplot: daily rides

fig_weather.add_trace(
    go.Scatter(
        x = df_weather['date'], 
        y = df_weather['rides'], 
        name = 'Daily bike rides', 
        marker={'color': df_weather['rides'],'color': 'blue'}),
    secondary_y = True)

# Add title

fig_weather.update_layout(
     title = 'Daily Bike Rides VS Daily Average Temperatures - NYC 2022',
     width = 900, height = 600)

st.plotly_chart(fig_weather, use_container_width = True)


### Displaying the map of trips

path_to_html = "Output/kepler_map.html"

# Read HTLM file in a variable 
with open(path_to_html, 'r') as f:
    html_data = f.read()

# Show in web page 
st.header("Aggregated Bike Trips in NYC 2022")
st.components.v1.html(html_data,height = 1000)