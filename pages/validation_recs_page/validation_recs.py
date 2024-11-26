import streamlit as st
import pandas as pd
from pages.fathes_days_page.fathers_days import request_api_vtex
from typing import List
import json
import requests as req

PAGE_URL = 'pages/validation_recs_page/'

def string_to_list(string: str) -> List:
    return json.loads(string)

def request_image(product_reference: str):
    URL = "https://aramisnova.myvtex.com/_v/api/intelligent-search/product_search/?query="

    product_reference_formated = product_reference.replace("|","")

    response = req.get(URL+product_reference_formated)
    if response.status_code == 200:
        json_response = response.json()
        if json_response['products'] and json_response['products'][0]['productReference'] == product_reference_formated:
            image_url = json_response['products'][0]["items"][0]["images"][0]["imageUrl"]
            return image_url 
        else:
            return None
    else:
        return None

def request_images(row,num_recs):
    cd_prod_cor = row['cd_prod_cor']
    st.subheader(f"Imagem do produto {cd_prod_cor}:")
    image_url = request_image(cd_prod_cor)
    if image_url:
        st.image(image_url, width=300)
    else:
        st.write("Imagem não encontrada.")
    st.subheader(f"As imagens das {num_recs} primeiras recomendações (que foram encontradas imagens) para o produto {row['cd_prod_cor']}:")
    recs_list = string_to_list(row['recs']) 
    count_images_showed = 1
    for rec in recs_list:
        image_url = request_image(rec)
        if image_url:
            st.write(f'{count_images_showed}. {rec}:')
            st.image(request_image(rec), width=300)
            count_images_showed += 1
        if count_images_showed == num_recs+1:
            break

def validation_recs():

    st.title("Página de validação de recomendações")
    df = pd.read_csv(PAGE_URL+'recs.csv')

    if not df.empty:
        st.write("Selecione linhas do CSV contendo os produtos, para obter as imagens das recomendações:")
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

        num_recs = st.number_input('Número de recomendações que serão exibidas para cada produto selecionado:', min_value=1, value=5, step=1)

        if st.button("Buscar recomendações"):
            with st.spinner("Buscando recomendações..."):
                if not filtered_df.empty:
                    filtered_df.apply(lambda row: request_images(row, num_recs), axis=1)
                else:
                    st.write("Selecione algum produto.")