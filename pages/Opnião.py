import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import time

# CONFIG DA PÁGINA
st.set_page_config(
    page_title="Contato",
    layout="wide"
)

# CONEXÃO
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/Spotify"
)

# SESSION STATE
if "enviado" not in st.session_state:
    st.session_state.enviado = False

if "limpar" not in st.session_state:
    st.session_state.limpar = False

if "nome" not in st.session_state:
    st.session_state.nome = ""

if "email" not in st.session_state:
    st.session_state.email = ""

if "mensagem" not in st.session_state:
    st.session_state.mensagem = ""

if "avaliacao" not in st.session_state:
    st.session_state.avaliacao = 5

# 👇 LIMPA OS CAMPOS ANTES DE RENDERIZAR (SEM ERRO)
if st.session_state.limpar:
    st.session_state.nome = ""
    st.session_state.email = ""
    st.session_state.mensagem = ""
    st.session_state.avaliacao = 5
    st.session_state.limpar = False

# TÍTULO
st.title("Contato / Sugestões")
st.subheader("Deixe sua opinião")
st.write("Sua opinião ajuda a melhorar o sistema!")

# LAYOUT
with st.container(border=True):

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            nome = st.text_input(
                "Nome",
                placeholder="Ex: Borges",
                key="nome"
            )

    with col2:
        with st.container(border=True):
            email = st.text_input(
                "Email",
                placeholder="Ex: email@email.com",
                key="email"
            )

    with st.container(border=True):
        mensagem = st.text_area(
            "Sua opinião",
            placeholder="Digite aqui o que você achou do app...",
            key="mensagem"
        )

    with st.container(border=True):
        avaliacao = st.slider(
            "Sua avaliação (1 a 10)",
            min_value=1,
            max_value=10,
            key="avaliacao"
        )

    enviar = st.button("Enviar 🚀")

# LÓGICA
if enviar:

    erros = []

    if not nome:
        erros.append(" Preencha o nome")

    if not email:
        erros.append("Preencha o email")

    if not mensagem:
        erros.append(" Escreva sua opinião")

    if erros:
        for erro in erros:
            st.error(erro)

    else:
        dados = {
            "nome": [nome],
            "email": [email],
            "mensagem": [mensagem],
            "avaliacao": [avaliacao]
        }

        df = pd.DataFrame(dados)

        df.to_sql(
            "opinioes",
            engine,
            if_exists="append",
            index=False
        )

        st.session_state.enviado = True
        st.rerun()

# SUCESSO TEMPORÁRIO
if st.session_state.enviado:
    sucesso = st.empty()

    sucesso.success("✅ Opinião enviada com sucesso!")

    time.sleep(2)

    sucesso.empty()

    # prepara limpeza segura
    st.session_state.limpar = True
    st.session_state.enviado = False

    st.rerun()