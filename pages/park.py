import streamlit as st
from analysis import ParkAnalysis
import pandas as pd
import plotly.graph_objs as go
from chatbot import GeneralModel

parkAnalysis = ParkAnalysis()

st.set_page_config(
    page_title="National Parks Too",
    page_icon="random",
    layout="wide",)

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
left_column, right_column = st.columns([2, 1])


name = st.experimental_get_query_params()["name"][0]
title_text = parkAnalysis.get_pretty(name) + " National Park"
with header:
    st.write(
        f"<h1 style= 'text-align: center;'>{title_text}</h1",
        unsafe_allow_html=True,
    )

# with dataset:
#     st.write(name)

with left_column:
    st.subheader("Monthly Visitors")
    data = parkAnalysis.line_chart(name)
    av = []
    av.append(0)
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    for i in range(12):
        av.append(data[i])
#    st.write(av)

    #chatGPT integration
    # recommender = GeneralModel()
    # recommendation = recommender.model_prediction(title_text, api_key="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")
    # print(recommendation)



    line_graph = go.Scatter(x=months, y=av, mode='lines')
    fig = go.Figure(line_graph)
    st.plotly_chart(fig)
    # #df = pd.DataFrame({'Number of visitors': av})
    #                       #, months[1]: av[1], months[2]: av[2],months[3]: av[3], months[4]: av[4], months[5]: av[5], months[6]: av[6], months[7]: av[7], months[8]: av[8], months[9]: av[9], months[10]: av[10], months[11]: av[11]})
    # st.line_chart(av[1:])
    st.write("Here are some recommendations provided by GPT from OpenAI:")
    # st.write(recommendation)
    st.write("https://www.nps.gov/" + name + "/index.htm")


with right_column:
    value = st.slider(
        "Select your desired temperature range",
        0, 130, (55, 85))
    #st.write("Temperature Range:", value)
    rain = st.select_slider(
        "Select how much precipitation you are comfortable with. Based on averages for the National Park",
        options=['Low', 'Medium-Low', 'Medium', 'Medium-High', 'High'])
    #st.write("Precipitation:", rain)
    mint = value[0]
    maxt = value[1]

    top_3 = parkAnalysis.best_months(name, mint, maxt, rain)
    # top_3 = ["Your top 3 months to visit", "January", "January", "January"]
    st.header(top_3[0])
    if len(top_3) == 2:
        st.subheader(top_3[1])
    if len(top_3) == 3:
        st.subheader(top_3[1])
        st.subheader(top_3[2])
    if len(top_3) == 4:
        st.subheader(top_3[1])
        st.subheader(top_3[2])
        st.subheader(top_3[3])


#def print_months(top_3):
