import streamlit as st
import pandas as pd
#from pages.fathes_days_page.fathers_days import request_api_vtex
from typing import List
#from pages.test_api.test_api_recommendations import BASE_URL, MAPPER_ENDPOINTS
#from pages.test_api.test_api_recommendations import request_api, process_json
import json
import requests as req

PAGE_URL = 'pages/validation_recs_page/'

def string_to_list(string: str) -> List:
    return json.loads(string)

def request_image(product_reference: str):
    URL = "https://aramisnova.myvtex.com/_v/api/intelligent-search/product_search/?query="
    #product_reference_formated = product_reference.replace("|","")

    response = req.get(URL+product_reference)
    if response.status_code == 200:
        json_response = response.json()
        if json_response['products'] and json_response['products'][0]['productReference'] == product_reference:
            image_url = json_response['products'][0]["items"][0]["images"][0]["imageUrl"]
            return image_url 
        else:
            return None
    else:
        return None

def request_images(row,num_recs):

    produtos_df = pd.read_csv(PAGE_URL+'produtos_infos.csv')
    produtos_df.set_index('cd_prod_cor', inplace=True)

    cd_prod_cor = row['cd_prod_cor']
    st.subheader(f"Imagem do produto {cd_prod_cor}:")
    image_url = request_image(cd_prod_cor)

    col1, col2 = st.columns([1, 2])
    
    if image_url:
        with col1:
            st.image(image_url, width=300)
    else:
        st.write("Imagem não encontrada.")

    with col2:
        st.write(f"**Nome:** {row['nm_prod']}")
        st.write(f"**Grupo:** {row['ds_grupo']}")
        st.write(f"**Subgrupo:** {row['ds_subgrupo']}")
        st.write(f"**Cor:** {row['ds_cor']}")
        st.write(f"**Cor Predominante:** {row['ds_cor_predominante']}")
        st.write(f"**Modelagem:** {row['ds_modelagem']}")
        st.write(f"**Composição:** {row['ds_composicao']}")

    st.subheader(f"As imagens das {num_recs} primeiras recomendações (que foram encontradas imagens) para o produto {row['cd_prod_cor']}:")
    recs_list = string_to_list(row['recs'])
    count_images_showed = 1
    for rec in recs_list:
        rec_infos = produtos_df.loc[rec['productId']]
        image_url = request_image(rec['productId'])
        if image_url:
            st.write(f'{count_images_showed}. {rec['productId']}:')

            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(image_url, width=300)

            with col2:
                st.write(f"**Nome:** {rec_infos['nm_prod']}")
                st.write(f"**Grupo:** {rec_infos['ds_grupo']}")
                st.write(f"**Subgrupo:** {rec_infos['ds_subgrupo']}")
                st.write(f"**Cor:** {rec_infos['ds_cor']}")
                st.write(f"**Cor Predominante:** {rec_infos['ds_cor_predominante']}")
                st.write(f"**Modelagem:** {rec_infos['ds_modelagem']}")
                st.write(f"**Composição:** {rec_infos['ds_composicao']}")

            count_images_showed += 1
        if count_images_showed == num_recs+1:
            break

def validation_recs():

    st.title("Página de validação de recomendações")

    #api_or_csv = st.selectbox(
    #    "API ou CSV", ["API", "CSV"], index=0
    #)

    itens_pai_df = pd.read_csv(PAGE_URL+'itens_pai_recs.csv')

    if not itens_pai_df.empty:
        st.write("Selecione a página e linhas do CSV contendo os produtos, para obter as imagens das recomendações:")

        page_size = 9000  
        total_rows = len(itens_pai_df)
        total_pages = (total_rows + page_size - 1) // page_size
    
        page_number = st.number_input("Página", min_value=1, max_value=total_pages, step=1, value=1)

        start_idx = (page_number - 1) * page_size
        end_idx = start_idx + page_size

        st.write(f"Exibindo página {page_number} de {total_pages}")
        
        page_df = itens_pai_df.iloc[start_idx:end_idx]

        grupos_filtro_info = itens_pai_df['ds_grupo'].unique()
        subgrupo_filtro_info = itens_pai_df['ds_subgrupo'].unique()
        cor_filtro_info = itens_pai_df['ds_cor'].unique()
        cor_predominante_filtro_info = itens_pai_df['ds_cor_predominante'].unique()
        modelagem_filtro_info = itens_pai_df['ds_modelagem'].unique()
        composicao_filtro_info = itens_pai_df['ds_composicao'].unique()

        st.write("### Filtros para o CSV:")
        grupo_select = st.selectbox("Grupo: ",grupos_filtro_info,index=None)
        subgrupo_select = st.selectbox("Subgrupo: ",subgrupo_filtro_info,index=None)
        cor_select = st.selectbox("Cor: ",cor_filtro_info,index=None)
        cor_predominante_select = st.selectbox("Cor Predominante: ",cor_predominante_filtro_info,index=None)
        modelagem_select = st.selectbox("Modelagem: ",modelagem_filtro_info,index=None)
        composicao_select = st.selectbox("Composição: ",composicao_filtro_info,index=None)

        filtered_page_df = page_df.copy()

        if grupo_select:
            filtered_page_df = filtered_page_df[filtered_page_df['ds_grupo'] == grupo_select]

        if subgrupo_select:
            filtered_page_df = filtered_page_df[filtered_page_df['ds_subgrupo'] == subgrupo_select]

        if cor_select:
            filtered_page_df = filtered_page_df[filtered_page_df['ds_cor'] == cor_select]

        if cor_predominante_select:
            filtered_page_df = filtered_page_df[filtered_page_df['ds_cor_predominante'] == cor_predominante_select]

        if modelagem_select:
            filtered_page_df = filtered_page_df[filtered_page_df['ds_modelagem'] == modelagem_select]

        if composicao_select:
            filtered_page_df = filtered_page_df[filtered_page_df['ds_composicao'] == composicao_select]

        event = st.dataframe(
            filtered_page_df,
            use_container_width=True,
            on_select="rerun",
            hide_index=True,
            selection_mode="multi-row",
        )

        #if api_or_csv == "API":
        #    key = st.selectbox(
        #        "Selecione o produto para pesquisar",
        #        df["cd_prod_cor"].unique(),
        #        index=None
        #    )

        #     if key:
        #         st.subheader(f"Imagem do produto {key}:")
        #         image_url = request_image(key)
        #         if image_url:
        #             st.image(image_url, width=300)
        #         else:
        #             st.write("Imagem não encontrada.")
        #         st.subheader(f"As imagens das recomendações para o produto {key}:")

        #         with st.spinner("Buscando recomendações..."):
        #             response, success = request_api("Produto Indisponível", key)

        #             if success:
        #                 products = process_json(response)

        #                 for product in products:
        #                     st.write(f"**ID:** {product['id']}")
        #                     st.write(f"**Nome:** {product['name']}")
        #                     st.image(product["image"], width=300)
        #                     st.write(f"**Link:** {product['link']}")
        #                     st.write(f"**Preço de:** R$ {product['price_per']}")
        #                     st.write(f"**Preço por:** R$ {product['price_of']}")
        #                     st.write("---")
        #             else:
        #                 st.error(response)
        #     else:
        #         st.warning("Selecione um produto para continuar")
        # else:

        st.write("### Produtos selecionados:")
        selected_rows = event.selection.rows
        page_selected_rows_df = filtered_page_df.iloc[selected_rows]

        st.dataframe(
            page_selected_rows_df,
            use_container_width=True,
            hide_index=True
        )

        num_recs = st.number_input('Número de recomendações que serão exibidas para cada produto selecionado:', min_value=1, value=5, step=1)

        if st.button("Buscar recomendações"):
            with st.spinner("Buscando recomendações..."):
                if not page_selected_rows_df.empty:
                    page_selected_rows_df.apply(lambda row: request_images(row, num_recs), axis=1)
                else:
                    st.write("Selecione algum produto.")