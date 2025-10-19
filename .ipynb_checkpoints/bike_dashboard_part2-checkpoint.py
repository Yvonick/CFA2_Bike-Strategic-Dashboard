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
from PIL import Image
import json

#### Set up browser tab

st.set_page_config(page_title = 'NYC Bikes - Strategic Dashboard 2022', layout='wide')


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

# Sampled Dataframe
df_sampled = pd.read_csv(
    "Bike Data - Reduced.csv",
    engine="pyarrow",                 # faster & lower memory
    dtype_backend="pyarrow",          # compact Arrow dtypes for ints/strings
)

### Drop-Down Menu to navigate the Dashboard

page = st.sidebar.selectbox('Select an aspect of the analysis',
    ["Intro Page",
    "Most popular stations",
    "Weather component and bike usage",
    "Interactive map with aggregated bike trips", 
    "Summary of recommendations"]
    )

#### Dashboard Pages

### Intro Page
if page == "Intro Page":
    st.title('NYC Bikes - Strategic Dashboard 2022')
    st.markdown("Welcome to the NYC citibike Strategic Dashboard.\
        This dashboard aims to summarize interesting metrics, diagnose problems and help identify areas of improvement for bike-sharing in NYC.\
        The dataset is all trips made on citibikes during the year 2022 in NYC.")
    st.image(Image.open("citibikestockimage.jpg"))
    st.markdown("This dashboard contains the following sections:")
    st.markdown("- Most popular stations: the top 20 stations in terms of volume of traffic.")
    st.markdown("- Weather component and bike usage: how seasonal weather correlates with average daily traffic")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Summary of recommendations")
    st.markdown("Please use the drop-down menu on the left panel to navigate between each section")
    
### Most popular stations page
## Top20 in a bar chart

# Make a nice color scale that stays clear from the whites
elif page ==  "Most popular stations":
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
    
    # Analysis
 
    st.markdown("We observe that the top 5 stations, and especially the top 3 stations are quite significantly more popular than the others in the top 20. After the top 5, the curve flattens.  \nAnother important (though unsurprising) observation is that all stations in the top 20 are in Manhattan.  \nWe recommend a particular focus on Manhattan, and especially the top 5 stations. Opening more stations in the vicinity of the top 5 stations could help solve the biggest challenges related to stations capacity.")

### Weather component vs bike usage page
## Plot the number of rides VS temperature in a dual plot
# Create the figure object that will host the 2 plots

elif page ==  "Weather component and bike usage":
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
        width = 900, height = 600
    )
    
    st.plotly_chart(fig_weather, use_container_width = True)
    
    # Analysis
    
    st.markdown("A strong correlation can be observed between daily average temperatures and daily average number of bike trips. Warmer temperatures are associated with higher bike traffic, up until a certain temperature (around 27ºC).  \nA closer examination reveals that extreme cold events are associated with punctual sharp drops in bike taffic.  \nA seasonal approach to capacity management is recommended. This could materialize by:  \n- focusing more efforts on maintenance during the winter, when we can afford to reduce the available capacity, and  \n- deploying more resources in the summer to regulate capacity between stations.  \n  \nHigh daily precipitations also correlate strongly with low daily traffic, but precipitations are much more unpredictable and harder to act upon. Still, this can also be taken into consideration when allocating resources on a short-term basis.")

    # Bonus graph: precipitation VS traffic

    fig_prcp = make_subplots(specs = [[{"secondary_y": True}]])
    
    fig_prcp.add_trace(
        go.Scatter(
            x = df_weather['date'], 
            y = df_weather['precipitation'],
            name = 'Daily Precipitations', 
            marker={'color': df_weather['precipitation'],'color': 'green'}),
        secondary_y = False
    )

    fig_prcp.add_trace(
        go.Scatter(
            x = df_weather['date'], 
            y = df_weather['rides'], 
            name = 'Daily bike rides', 
            marker={'color': df_weather['rides'],'color': 'blue'}),
        secondary_y = True
    )
    
    fig_prcp.update_layout(
        title = 'Daily Bike Rides VS Daily Precipitation - NYC 2022',
        width = 900, height = 600
    )

    st.plotly_chart(fig_prcp, use_container_width = True)

    
### Interactive map page

elif page ==  "Interactive map with aggregated bike trips":

    path_to_html = "Output/kepler_map.html"
    
    # Read HTLM file in a variable 
    with open(path_to_html, 'r') as f:
        html_data = f.read()
    
    # Show in web page 
    st.header("Aggregated Bike Trips in NYC 2022")
    st.components.v1.html(html_data,height = 1000)

    # Analysis
    
    st.markdown(
        "When increasing the selectiveness of the filter we can see which areas are the most active looking at only start/end pairs with more than 1500 trips gives good legibility.  \nUnsuprisingly, these are mainly focused in and around Manhattan.  \nBy looking more closely, we can see a particularly high density of trips around green areas or areas next to the river:  \n- Central Park  \n- Governors Island  \n- Hudson bank in Manhattan  \n- East River bank in Brooklyn  \n-We can deduce that a nice environment conditions how people use the citibikes:  \n- They may use the bikes for recreational purposes more than just going from point A to point B (an analysis of the times and days with highest activity could give more info here)  \n- They may warp their itineraries around favourable spots  \n- They may choose the bike if the itinerary is nice, but take another means if not.  \nTwo recommendations emerge from these insights:  \n- Identify existing critical areas and allocate resources into increasing the capacity there and creating new bike stations where appropriate.  \n- Identify potential areas favourable to biking that are not sufficiently exploited yet, by looking at areas with similar characteristics as existing high traffic areas."
    )

### Recommendations page

elif page ==  "Summary of recommendations":
        st.markdown(
        'In conclusion, we formulate the following recommendations based on the insights that we highlighted in this dashboard.  \n- Allocate investments to alleviate capacity stress in critical areas : around the top 5 most used stations and along several existing "favourable biking areas" \n- Adopt a seasonal approach to resource management, by doing more maintenance in the winter and more operational support in the summer.  \n- Be reactive to short-term weather events like extreme temperature events or high precipitations.  \n- Discover new potential "favourable biking areas" and invest there for future expansion of the network.'
    )