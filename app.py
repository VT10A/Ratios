# AUTOGENERATED! DO NOT EDIT! File to edit: Ratio_BV.ipynb.

# %% auto 0
__all__ = []

# %% Ratio_BV.ipynb 4
import pandas as pd
import polars as pl
import numpy as np
from sklearn.preprocessing import StandardScaler
import plotly.express as px
#import highcharts_core.chart as hc
import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm

StreamlitPatcher().jupyter() 

st.title("Correlations:")
st.write("Note: This is indicative only given we are correlating a short list of aggregated measures rather than respondent level data so n is small")

# Define a function to load the data and cache it

@st.cache_data()
def load_data(path):
    return pd.read_csv(path)

data = load_data('Ratio_scores2.csv')


#Page filters

metric_list = ['Consideration','Rejectors']

selected_metric = st.sidebar.radio("Select metric:", metric_list)

if selected_metric == "Consideration":
    key_metric = "Consideration"
else:
    key_metric = "Rejectors"




brand_list = data['Brand'].unique().tolist()
selected_brand = st.sidebar.selectbox("Select Brand:", brand_list)

# Filter cached data
df_filtered = data[(data['Brand'] == selected_brand)]

scores = df_filtered[['Preference Ratio','Relative Buzz',key_metric]].corr()
st.write(round(scores,2))

# Define custom color scale from dark red to dark green
custom_color_scale = [
    [0.0, 'darkred'],  # Start of the scale (low consideration)
    [0.5, 'grey'],   # Middle of the scale
    [1.0, 'darkblue']  # End of the scale (high consideration)
]


#Plot title
st.title("Preference Ratio vs Relative Buzz:")


# Create bubble chart using Plotly
fig = px.scatter(df_filtered, 
                 x='Preference Ratio', 
                 y='Relative Buzz', 
                 size= key_metric,  
                 color=key_metric, 
                 color_continuous_scale=custom_color_scale,
                 opacity=0.7,
                 labels={
                     'Preference Ratio': 'Preference Ratio',
                     'Relative Buzz': 'Relative Buzz',
                     'key_metric': key_metric
                 },
               #  title="Test",
                 hover_name='Brand',  # Show brand name on hover
                 text='QuarterYear'  # Label points with 'Cleaned Label' column values
                )

fig.update_traces(marker=dict(symbol='circle', sizemode='diameter'), selector=dict(mode='markers'))

# Adjust the position of labels relative to markers
for trace in fig.data:
    trace.textposition = 'top center'

# Update layout to make the plot wider and longer
fig.update_layout(
    coloraxis_colorbar=dict(title=key_metric),
    plot_bgcolor='white',  # Set plot background color to white
    width=1000,  # Set the width of the plot
    height=500,  # Set the height of the plot
    #title=dict(
   #     x=0.5,  # Center the title horizontally
    #    font=dict(size=24)  # Increase title font size
    #),
    xaxis=dict(
        title='Preference Ratio',  # Set x-axis title
        titlefont=dict(size=18),  # Set x-axis title font size
        tickfont=dict(size=14)  # Set x-axis tick font size
    ),
    yaxis=dict(
        title='Relative Buzz',  # Set y-axis title
        titlefont=dict(size=18),  # Set y-axis title font size
        tickfont=dict(size=14)  # Set y-axis tick font size
    )
)

st.plotly_chart(fig)




from nbdev.export import nb_export
nb_export("Ratio_BV.ipynb", lib_path="./", name="app")
