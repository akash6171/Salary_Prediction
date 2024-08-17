import streamlit as st 
from predictionPage import showPredictPage
from explorePage import showExplorePage

page = st.sidebar.selectbox("Explore or predict", ("Predict", "Explore"))
if page == "Predict":
    showPredictPage()
else:
    showExplorePage()