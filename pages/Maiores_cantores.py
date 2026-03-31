import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

from config.style import PERSON

st.set_page_config(
    "Maiores Cantores",
    layout="wide"
)

# ========================
# Conexão com banco
# ========================
conn = psycopg2.connect(
    host="localhost",
    database="Spotify",
    user="postgres",
    password="postgres"
)

st.title("Maiores Cantores por Ano ou Período (2010 - 2019)")

# ========================
# Escolha do modo
# ========================
with st.container(border=True):

    opcoes = ["Por ano", "De 2010 a 2019"]

    modo = st.radio(
        "Escolha como deseja visualizar:",
        options=opcoes,
        index=None
    )

if modo is None:
    st.stop()

# ==========================================================
# ======================== MODO POR ANO ====================
# ==========================================================
if modo == "Por ano":

    # Buscar anos do banco
    df_anos = pd.read_sql(
        "SELECT DISTINCT year FROM dados_spotify ORDER BY year",
        conn
    )

    anos_disponiveis = df_anos["year"].tolist()

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.success("Escolha o ano:")
            ano_selecionado = st.selectbox(
                "",
                anos_disponiveis,
                label_visibility="collapsed"
            )

    # Query agrupada direto no banco
    query = """
    SELECT artist, AVG(pop) as pop
    FROM dados_spotify
    WHERE year = %s
    GROUP BY artist
    ORDER BY pop DESC
    """

    df_agrupado = pd.read_sql(query, conn, params=(ano_selecionado,))

    with col2:
        with st.container(border=True):
            st.success(f"Veja até o top 20 cantores de {ano_selecionado}")
            top_n = st.slider(
                "",
                min_value=2,
                max_value=min(20, len(df_agrupado)),
                value=5
            )

    top_cantores = df_agrupado.head(top_n)

    # ------------------ GRÁFICO ------------------
    fig = px.bar(
        top_cantores,
        x="artist",
        y="pop",
        color="pop",
        color_continuous_scale=[
        "#16a34a",
        "#15803d",
        "#166534",
        "#14532d",
        "#0b3d2e"
    ],
        title=f"Top {top_n} cantores mais populares em {ano_selecionado}",
        labels={
            "artist": "Cantor",
            "pop": "Popularidade Média"
        }
    )



    st.plotly_chart(fig, use_container_width=True)

    # Base detalhada (somente artistas selecionados)
    artistas = top_cantores["artist"].tolist()
    placeholders = ",".join(["%s"] * len(artistas))

    query_detalhes = f"""
    SELECT artist, title, pop
    FROM dados_spotify
    WHERE year = %s
    AND artist IN ({placeholders})
    """

    df_base = pd.read_sql(
        query_detalhes,
        conn,
        params=[ano_selecionado] + artistas
    )


# ==========================================================
# ==================== MODO 2010 A 2019 ====================
# ==========================================================
elif modo == "De 2010 a 2019":

    query = """
    SELECT artist, AVG(pop) as pop
    FROM dados_spotify
    GROUP BY artist
    ORDER BY pop DESC
    """

    df_agrupado = pd.read_sql(query, conn)

    with st.container(border=True):
        st.success("Escolha quantos cantores deseja visualizar")

        top_n = st.slider(
            "",
            min_value=2,
            max_value=min(40, len(df_agrupado)),
            value=10
        )

    top_cantores = df_agrupado.head(top_n)

    # ------------------ GRÁFICO ------------------
    fig = px.bar(
        top_cantores,
        x="artist",
        y="pop",
        color="pop",
        color_continuous_scale=[
        "#16a34a", 
        "#15803d",
        "#166534",
        "#14532d",
        "#0b3d2e" 
    ],
        title=f"Top {top_n} cantores mais populares de 2010 a 2019",
        labels={
            "artist": "Cantor",
            "pop": "Popularidade Média"
        }
    )

    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)

    # Base detalhada
    artistas = top_cantores["artist"].tolist()
    placeholders = ",".join(["%s"] * len(artistas))

    query_detalhes = f"""
    SELECT artist, title, pop
    FROM dados_spotify
    WHERE artist IN ({placeholders})
    """

    df_base = pd.read_sql(
        query_detalhes,
        conn,
        params=artistas
    )

# ==========================================================
# ======================== TABELA ===========================
# ==========================================================

# Música mais popular por artista
musica_mais_famosa = (
    df_base
    .sort_values("pop", ascending=False)
    .drop_duplicates("artist")
    [["artist", "title", "pop"]]
    .rename(columns={
        "title": "Música mais famosa",
        "pop": "Popularidade da música"
    })
)

# Quantidade de músicas
quantidade_musicas = (
    df_base
    .groupby("artist")
    .size()
    .reset_index(name="Quantidade de músicas")
)

# Ranking
top_cantores = top_cantores.reset_index(drop=True)
top_cantores["Ranking"] = top_cantores.index + 1

# Tabela final
tabela_final = (
    top_cantores
    .merge(musica_mais_famosa, on="artist")
    .merge(quantidade_musicas, on="artist")
    .rename(columns={
        "artist": "Cantor",
        "pop": "Popularidade média"
    })
    .sort_values("Ranking")
)

# Mostrar tabela
with st.container(border=True):
    st.title("Detalhe dos cantores")
    cantores_style = (
        tabela_final.style
        .set_table_styles([
          { 'selector': 'th.col_heading', 'props': [('background-color', PERSON["cor_cabecalho_fundo"]), ('color', PERSON["cor_texto_cabecalho"])] },
          { 'selector': 'th.index_name', 'props': [('background-color',  PERSON["cor_cabecalho_fundo"]), ('color', PERSON["cor_texto_cabecalho"])] }
      ])
    )

    tabela = st.table(cantores_style)