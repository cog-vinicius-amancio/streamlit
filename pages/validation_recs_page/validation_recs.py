import streamlit as st
import pandas as pd
from pages.fathes_days_page.fathers_days import request_api_vtex
from typing import List
import json

PAGE_URL = 'pages/validation_recs_page/'

def string_to_list(string: str) -> List:
    return json.loads(string)

def validation_recs():

    st.title("Selecione Linhas do CSV")
    df = pd.read_csv(PAGE_URL+'rec.csv')

    st.write("Dados carregados do CSV:")
    event = st.dataframe(
        df,
        use_container_width=True,
        on_select="rerun",
        hide_index=True,
        selection_mode="multi-row"
    )

    st.write("Produtos selecionados:")
    selected_rows = event.selection.rows
    filtered_df = df.iloc[selected_rows]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("Buscar recomendações"):
        with st.spinner("Buscando recomendações..."):
            for cd_prod_cor in filtered_df:
                st.write(f"{cd_prod_cor}:")