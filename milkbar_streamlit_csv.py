import pydeck as pdk
import datetime
import math
import altair as alt
from altair import Chart, X, Y, Axis, SortField, OpacityValue
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import streamlit as st

#READ CSV FILE AND TEST STREAMLIT DEVELOPMENT IN THIS FILE.
def load_data(nrows):
    data = pd.read_csv('sweetpea.csv')
    return data
data = load_data(10000)
print(data)

data['date_time'] = pd.to_datetime(data['date_time']) # this creates an odd time stamp in streamlit. Not required.

st.title('Sweet Pea Movements')
st.image('./Sweet_Pea.jpg', caption='Feeling those wiggles')

st.subheader('Record wiggles here https://forms.gle/xW1HJuyCyQ4bywFU7')

st.subheader('View all wiggles')
st.write(data)
st.altair_chart(alt.Chart(data)
				.mark_rect()
				.encode(
	alt.X('hours(date_time):O', title='hour'),
	alt.Y('monthdate(date_time):O', title='day'),
	color='count(data):Q',
	tooltip=[
		alt.Tooltip('hours(date_time):O', title='hour'),
		alt.Tooltip('count(data):Q', title='Wiggle count')
	]
).properties(
	title='All the wiggles'
))


st.title("Wiggles by hour")
hour_selected = st.slider("Select hour of wiggles", 0, 23)

# FILTERING DATA BY HOUR SELECTED
data = data[data['date_time'].dt.hour == hour_selected]

# FILTERING DATA FOR THE HISTORGRAM

filtered = data[
	(data['date_time'].dt.hour >= hour_selected) & (data['date_time'].dt.hour < (hour_selected + 1))
	]

hist = np.histogram(filtered['date_time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "movement": hist})

#LAYING OUT THE HISTOGRAM SECTIONs

st.write("")
st.write("**Wiggles per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data)
	.mark_area(
		interpolate='step-after',
	).encode(
		x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
		y=alt.Y("movement:Q"),
		tooltip=['minute', 'movement']
	).configure_mark(
		opacity=0.5,
		color='blue'
	), use_container_width=True)





st.line_chart(data)
st.write(data)

