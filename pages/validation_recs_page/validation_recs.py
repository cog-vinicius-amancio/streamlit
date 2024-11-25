import streamlit as st
import pandas as pd
from pages.fathes_days_page.fathers_days import request_api_vtex
from typing import List
import json

PAGE_URL = 'pages/validation_recs_page/'

def string_to_list(string: str) -> List:
    return json.loads(string)

def request_images(row):
    st.write(f"Recomendações para o produto {row['cd_prod_cor']}:")
    st.write(string_to_list(row['recs']))

def validation_recs():

    st.title("Página de validação de recomendações")
    df = pd.read_csv(PAGE_URL+'rec.csv')

    if not df.empty:
        st.write("Selecione Linhas do CSV contendo os produtos, para obter as imagens das recomendações:")
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
                if not filtered_df.empty:
                    filtered_df.apply(request_images, axis=1)
                else:
                    st.write("Selecione algum produto.")