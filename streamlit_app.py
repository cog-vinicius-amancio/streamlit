import streamlit as st

from pages.fathes_days_page.fathers_days import fathers_day
from pages.alr_test_ab.validation_recs_alt_test_ab import model_alr

st.set_page_config(
    page_title="Aramis Testing Pages",
    page_icon=":tshirt:",
    layout="centered"
)

PAGES = {
    "Dia dos Pais": fathers_day,
    "Modelo ALR - Teste A/B": model_alr,
}

st.sidebar.title("Menu")

selection = st.sidebar.radio("Escolha a página:", list(PAGES.keys()))

page = PAGES[selection]
page()