import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px

from config.style import PERSON


st.set_page_config(
    "Comparaçoẽs",
    layout="wide"
)
# -----------------------
# Conexão com banco
# -----------------------
conn = psycopg2.connect(
    host="localhost",
    database="Spotify",
    user="postgres",
    password="postgres"
)

st.title(" Comparação de Cantores por Popularidade")

# -----------------------
# Buscar anos
# -----------------------
query_anos = "SELECT DISTINCT year FROM dados_spotify ORDER BY year"
df_anos = pd.read_sql(query_anos, conn)
anos_disponiveis = df_anos["year"].tolist()

# -----------------------
# Layout
# -----------------------
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        ano_selecionado = st.selectbox("Ano", anos_disponiveis)

# -----------------------
# Buscar cantores do ano
# -----------------------
query_cantores = """
SELECT DISTINCT artist 
FROM dados_spotify 
WHERE year = %s
ORDER BY artist
"""

df_cantores = pd.read_sql(query_cantores, conn, params=(ano_selecionado,))

with col2:
    with st.container(border=True):
        cantores = st.multiselect(
            "Cantores",
            df_cantores["artist"].tolist()
        )

# -----------------------
# Se selecionar pelo menos 2
# -----------------------
if len(cantores) >= 2:

    # Criar placeholders para IN (%s, %s, %s...)
    placeholders = ",".join(["%s"] * len(cantores))

    query_dados = f"""
    SELECT artist, AVG(pop) as pop
    FROM dados_spotify
    WHERE year = %s
    AND artist IN ({placeholders})
    GROUP BY artist
    ORDER BY pop DESC
    """

    params = [ano_selecionado] + cantores

    df_agrupado = pd.read_sql(query_dados, conn, params=params)

    # -----------------------
    # Métricas
    # -----------------------
    maior = df_agrupado.loc[df_agrupado["pop"].idxmax()]
    menor = df_agrupado.loc[df_agrupado["pop"].idxmin()]

    col1, col2 = st.columns(2)

    col1.metric(
        "Cantor Mais Popular",
        maior["artist"],
        f"Média: {round(maior['pop'], 1)}"
    )

    col2.metric(
        "Cantor Menos Popular",
        menor["artist"],
        f"Média: {round(menor['pop'], 1)}"
    )

    st.divider()

    # -----------------------
    # Gráfico
    # -----------------------
    fig = px.bar(
        df_agrupado,
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
        title=f"Popularidade Média por Cantor - {ano_selecionado}"
    )

    fig.update_layout(
        xaxis_title="Cantor",
        yaxis_title="",
        title_x=0.3,
        font=dict(family="Arial", size=14),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -----------------------
    # Ranking
    # -----------------------
    st.subheader(" Ranking de Popularidade")

    df_agrupado.index = df_agrupado.index + 1
    df_agrupado.columns = ["Cantor", "Popularidade Média"]

    cantores_style = (
            df_agrupado.style
            .set_table_styles([
            { 'selector': 'th.col_heading', 'props': [('background-color', PERSON["cor_cabecalho_fundo"]), ('color',PERSON["cor_texto_cabecalho"])] },
            { 'selector': 'th.index_name', 'props': [('background-color', PERSON["cor_cabecalho_fundo"]), ('color', PERSON["cor_texto_cabecalho"])] },
            ])
            )
    tabela = st.table(cantores_style)
# -----------------------
# Caso não selecione suficiente
# -----------------------
else:
    st.success("Selecione pelo menos 2 cantores para comparar.")


    









