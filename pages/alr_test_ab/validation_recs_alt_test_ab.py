import streamlit as st
import pandas as pd

from pages.fathes_days_page.fathers_days import request_api_vtex


def model_alr():
    st.write("Modelo ALR - Teste A/B")

    model_type = st.sidebar.selectbox(
        "Modelo",
        ["Categorias Diferentes", "Categorias Iguais"],
    )

    if model_type == "Categorias Diferentes":
        data = pd.read_csv("pages/alr_test_ab/diff_categ.csv")
    else:
        data = pd.read_csv("pages/alr_test_ab/same_categ.csv")

    product = st.text_input("Digite o código do produto (sem cor):").upper().strip()

    recs_filtered = data.loc[data["productId"].str.contains(product, case=False)][
        "cd_prods_rec"
    ].unique()[:12]

    if st.button("Buscar"):
        if recs_filtered.size > 0:
            st.write("Produtos recomendados:")
            for rec in recs_filtered:
                response = request_api_vtex(rec)
                if response:
                    st.write(f"**Nome**: {response['products'][0]['productName']}")
                    st.image(
                        response["products"][0]["items"][0]["images"][0]["imageUrl"],
                        width=200,
                    )
                    st.write(
                        f"**Descrição**: {response['products'][0]['description']}"
                    )
                    st.write(
                        f"**Preço**: R$ {response['products'][0]['items'][0]['sellers'][0]['commertialOffer']['Price']}"
                    )
                    st.write("---" * 50)
                else:
                    st.write("Erro ao processar requisição")
        else:
            st.write("Produto não encontrado")
