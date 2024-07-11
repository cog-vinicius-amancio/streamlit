import streamlit as st
import requests as req
from unidecode import unidecode
import json


def request_api_fathers_day(
    opcao1: str, opcao2: str, opcao3: str, opcao4: str, size: str, email: str
):
    URL = "https://homolog-father-day-apimanagement.azure-api.net/api/v1/father_day"

    body = {
        "email": unidecode(email.lower()),
        "question1": unidecode(opcao1.lower()),
        "question2": unidecode(opcao2.lower()),
        "question3": unidecode(opcao3.lower().replace(" ", "")),
        "question4": unidecode(opcao4.lower()),
        "sizes": {"top-size": size},
    }

    response = req.post(URL, json=body)

    try:
        return response.json()
    except req.JSONDecodeError:
        return None


def request_api_vtex(product_search: str):
    URL = "https://www.aramis.com.br/_v/api/intelligent-search/product_search/"

    params = {
        "query": product_search.replace("|", ""),
    }

    response = req.get(URL, params=params)

    try:
        return response.json()
    except req.JSONDecodeError:
        return None


st.title("Father's Day Quiz :necktie:")

API_OR_MOCK = st.checkbox(
    "Utilizar API (API ok! :white_check_mark:)", value=True, disabled=True
)

st.write("Selecione as opções:")

opcao1 = st.radio(
    "1. Qual estilo combina melhor com seu pai?", ["Sofisticado", "Casual"]
)

opcao2 = st.radio("2. Qual a ocasião de uso?", ["Trabalho", "Lazer"])

opcao3 = st.radio(
    "3. Quais cores predominam nas roupas do seu pai?", ["Tons Claros", "Tons Escuros"]
)

opcao4 = st.radio("4. Acessórios fazem parte do estilo do seu pai?", ["Sim", "Não"])

size = st.radio(
    "5. Qual tamanho de roupa o seu pai usa?", 
    ["P", "M", "G", "GG", "XGG", "XXG"]
)

email = st.text_input("Digite o e-mail para receber desconto:")

if st.button("Enviar"):
    if API_OR_MOCK:
        response: dict = request_api_fathers_day(opcao1, opcao2, opcao3, opcao4, size, email)

        if response:
            for look, values in response.items():
                st.write(f"#### **Look {look[-1]}**")
                for product in values:
                    st.write(f"**Categoria:** {product["category"]}")
                    st.write(f"**Nome**: {product['VtexProduct']['productName']}")
                    st.image(
                        product["VtexProduct"]["items"][0]["images"][0]["imageUrl"],
                        width=200,
                    )
                    st.write(f"**Descrição**: {product['VtexProduct']['description']}")
                    st.write(
                        f"**Preço**: R$ {product['VtexProduct']['items'][0]['sellers'][0]['commertialOffer']['Price']}"
                    )
                    st.write("---" * 50)
        else:
            st.write("Erro ao processar requisição")
    else:
        data_mock: dict = json.load(open("mock.json", "r"))

        option = "-".join(
            [unidecode(eval(f"opcao{i}").lower().replace(" ", "")) for i in range(1, 5)]
        )

        classes = data_mock.get(option, [])

        for cl, recs in classes.items():
            st.write(f"Classe: {cl}")
            for part, rec in recs.items():
                for product in [rec["master-item"]] + rec["secondary-items"]:
                    response = request_api_vtex(product)

                    if response:
                        if len(response["products"]) > 0:
                            st.text(response["products"][0]["productName"])
                            st.image(
                                response["products"][0]["items"][0]["images"][0][
                                    "imageUrl"
                                ],
                                width=100,
                            )
                            st.text(response["products"][0]["description"])
                            break
else:
    pass
