import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

st.set_page_config(
    page_title="Análise 2010-2019",
    layout="wide"
)

# ========================
# Conexão
# ========================
conn = psycopg2.connect(
    host="localhost",
    database="Spotify",
    user="postgres",
    password="postgres"
)

st.title(" Análise Completa do Spotify (2010-2019)")
st.markdown("### Tendências, artistas e popularidade ao longo dos anos")

st.divider()

# ========================
# MÉTRICAS PRINCIPAIS (SQL)
# ========================

# Música mais popular
query_top_music = """
SELECT title, artist, pop
FROM dados_spotify
ORDER BY pop DESC
LIMIT 1
"""
musica_mais_pop = pd.read_sql(query_top_music, conn).iloc[0]

# Artista mais presente
query_artist = """
SELECT artist, COUNT(*) as total
FROM dados_spotify
GROUP BY artist
ORDER BY total DESC
LIMIT 1
"""
artista_mais = pd.read_sql(query_artist, conn).iloc[0]

# Ano mais popular
query_ano = """
SELECT year, AVG(pop) as media
FROM dados_spotify
GROUP BY year
ORDER BY media DESC
LIMIT 1
"""
ano_mais_pop = pd.read_sql(query_ano, conn).iloc[0]

# Média geral
query_media = "SELECT AVG(pop) as media FROM dados_spotify"
media_geral = round(pd.read_sql(query_media, conn)["media"][0], 1)

# Layout métricas
col1, col2, col3,  = st.columns(3)

col1.metric(
    " Música mais popular",
    musica_mais_pop["title"],
    f"{musica_mais_pop['artist']} ({musica_mais_pop['pop']})"
)

col2.metric(
    " Artista mais presente",
    artista_mais["artist"],
    f"{artista_mais['total']} músicas"
)

col3.metric(
    " Ano mais popular",
    int(ano_mais_pop["year"]),
)



st.divider()

# ========================
# Evolução da popularidade
# ========================
query_pop_ano = """
SELECT year, AVG(pop) as pop
FROM dados_spotify
GROUP BY year
ORDER BY year
"""
df_ano = pd.read_sql(query_pop_ano, conn)

fig_pop = px.line(
    df_ano,
    x="year",
    y="pop",
    markers=True,
    title=" Evolução da Popularidade Média (2010-2019)",
    color_discrete_sequence=["#1DB954"]
)



st.plotly_chart(fig_pop, use_container_width=True)

# ========================
# Número de músicas por ano
# ========================
query_lanc = """
SELECT year, COUNT(*) as total_musicas
FROM dados_spotify
GROUP BY year
ORDER BY year
"""
df_lancamentos = pd.read_sql(query_lanc, conn)

fig_lanc = px.bar(
    df_lancamentos,
    x="year",
    y="total_musicas",
    color="total_musicas",
            color_continuous_scale=[
        "#16a34a", 
        "#15803d",
        "#166534",
        "#14532d",
        "#0b3d2e" 
    ],
    title=" Número de Músicas Lançadas por Ano"
)
st.divider()

st.plotly_chart(fig_lanc, use_container_width=True)

st.divider()

# ========================
# TOP 5 ARTISTAS
# ========================
st.subheader(" Top 5 Artistas Mais Populares (Média Geral)")

query_top5 = """
SELECT artist, AVG(pop) as pop
FROM dados_spotify
GROUP BY artist
ORDER BY pop DESC
LIMIT 5
"""
top5 = pd.read_sql(query_top5, conn)

fig_top5 = px.bar(
    top5,
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
)



st.plotly_chart(fig_top5, use_container_width=True)

st.divider()

# ========================
# DESCRIÇÃO
# ========================
st.success(
    """
     Este dashboard apresenta:
    - Evolução da popularidade ao longo dos anos
    - Quantidade de lançamentos anuais
    - Ranking dos artistas mais populares
    
    Uma visão estratégica completa do Spotify entre 2010 e 2019.
    """
)
