import streamlit as st
import folium as fl
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://img.freepik.com/premium-photo/wood-desk-wood-floor-with-sea-beach-sand-blue-background-summer-background_35652-2616.jpg?size=626&ext=jpg&ga=GA1.1.1826414947.1699747200&semt=ais");
        background-size: cover;
        background-position: center;
        background-attachment: local;
    }}
    </style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

image1 = Image.open('image1.png')


# Añadimos un panel de control
tab1, tab2, tab3 = st.tabs(["Inicio", "Análisis a nivel nacional", "Anális a nivel departamental"])

with tab1:
   st.image(image1)


# Análisis a nivel nacional
with tab2:
    st.image(image1)
