import streamlit as st
from pathlib import Path
import pandas as pd
import base64
import psycopg2

# ========================
# Configuração da página
# ========================
st.set_page_config(
    page_title="Spotify 2010-2019",
    page_icon="🟢",
    layout="wide"
)

# ========================
# Banco de dados
# ========================
conn = psycopg2.connect(
    host="localhost",
    database="Spotify",
    user="postgres",
    password="postgres"
)

df = pd.read_sql("SELECT * FROM dados_spotify", conn)




# ========================
# HERO SECTION
# ========================
col1, col2 = st.columns([1.3, 1])

with col1:
    st.title(" Spotify Análise (2010 - 2019)")
    st.markdown("### Dashboard interativo para análise musical")

    st.write(
        """
        Este site analisa músicas do Spotify entre 2010 a 2019,
        explorando **popularidade, artistas, tendências e lançamentos**.

        Você poderá:
        - Comparar artistas
        - Descobrir rankings populares
        - Analisar tendências
        - Explorar lançamentos
        """
    )

    st.success("Utilize o menu lateral para navegar.")

# ========================
# Imagem clicável (COM PROTEÇÃO)
# ========================

BASE_DIR = Path(__file__).resolve().parent
spotify_img = BASE_DIR / "image" / "spotify_branco.png"

spotify_link = "https://open.spotify.com/intl-pt"

with col2:
    st.success("Aperte na imagem abaixo para acessar o Spotify")

    if spotify_img.exists():
        with open(spotify_img, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        html_code = f"""
        <div style="display:flex; justify-content:center;">
            <a href="{spotify_link}" target="_blank">
                <img src="data:image/png;base64,{encoded}" 
                    style="
                        width:1200px;
                        border-radius:20px;
                        transition:0.3s;
                        cursor:pointer;
                    "
                    onmouseover="this.style.transform='scale(1.1)'"
                    onmouseout="this.style.transform='scale(1)'"
                >
            </a>
        </div>
        """

        st.markdown(html_code, unsafe_allow_html=True)

    else:
        st.warning("Imagem não encontrada, usando alternativa...")
        st.image("https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", width=120)
st.divider()

# ========================
# VISÃO GERAL DO DATASET
# ========================
with st.container(border=True):

    st.subheader(" Visão Geral do Dataset")

    c1, c2, c3, c4 = st.columns(4)

    anos = sorted(df["year"].unique())
#bloco1
    with open('sql/total_musicas.sql', 'r', encoding='utf-8') as f:
        query = f.read()
        df_total_musicas = pd.read_sql_query(query, conn)
        print(df_total_musicas)

    with c1:
        st.metric(" Músicas analisadas",df_total_musicas["count"])



#bloco2
    with open('sql/total_artista.sql', 'r', encoding='utf-8') as f:
        query = f.read()
        df_total_artista = pd.read_sql_query(query, conn)
       
    with c2:
        st.metric("total de artista",df_total_artista["count"][0])

#bloco3 
    with open('sql/ano_inicial.sql', 'r', encoding='utf-8') as f:
        query = f.read()
        df_ano_incial = pd.read_sql_query(query, conn)

    with open('sql/ano_final.sql', 'r', encoding='utf-8') as f:
        query = f.read()
        df_ano_final = pd.read_sql_query(query, conn)

    ano_inicial = df_ano_incial["ano_inicial"][0]
    ano_final = df_ano_final["ano_final"][0]

    with c3:
        st.metric("Periodo analisado", f"{ano_inicial} - {ano_final}")

#bloco4
    with open('sql/media.sql', 'r', encoding='utf-8') as f:
        query = f.read()
        df_media = pd.read_sql_query(query, conn)    
    with c4:
        st.metric("Popularidade média", round(df_media["media"].iloc[0], 2))







