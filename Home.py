import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
from analysis import ParkAnalysis


st.set_page_config(
    page_title="National Parks Data",
    page_icon="random",
    layout="wide"
)

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none
        }
    </style>
    """,
    unsafe_allow_html=True,
)

header = st.container()

dataset = st.container()
left_column, right_column = st.columns([3, 1])

title_text = "National Parks Interactive Planning"
with header:
    st.write(
        f"<h1 style= 'text-align: center;'>{title_text}</h1",
        unsafe_allow_html=True
    )
m = leafmap.Map(center=[40, -100], zoom=4)

parkAnalysis = ParkAnalysis()
weather_data = pd.DataFrame.from_dict(parkAnalysis.parks_df_dct)

m.add_points_from_xy(
    weather_data,
    x="Longitude",
    y="Latitude",
    popup=["Name"],
    add_legend=False
)


with dataset:
    st.header("Interactive Map")

with left_column:
    m.to_streamlit(height=600,)

with right_column:
    value = st.slider(
        "Select your desired temperature range",
        32, 110, (55, 85))
    #st.write("Temperature Range:", value)
    mint = value[0]
    maxt = value[1]
    rain = st.select_slider(
        "Select how much precipitation you are comfortable with. Based on averages for the National Park",
        options=['Low', 'Medium-Low', 'Medium', 'Medium-High', 'High'])
    #st.write("Precipitation:", rain)
    st.header("The best 5 National Parks to visit this month")
    top_5 = parkAnalysis.best_parks(mint, maxt, rain)
    for i in range(len(top_5)):
        st.subheader(top_5[i])

    # st.subheader(top_5[1])
    # st.subheader(top_5[2])
    # st.subheader(top_5[3])
    # st.subheader(top_5[4])
