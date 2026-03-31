import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

from config.style import PERSON


# ========================
# Configuração da página
# ========================
st.set_page_config(
    page_title="Spotify Top Músicas",
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

# ========================
# Título
# ========================
st.title("Veja o top 15 de músicas mais escutadas de cada ano")

# ========================
# Buscar anos (SQL)
# ========================
df_anos = pd.read_sql(
    "SELECT DISTINCT year FROM dados_spotify ORDER BY year",
    conn
)

anos_disponiveis = df_anos["year"].tolist()

# ========================
# Seleção do ano
# ========================
with st.container(border=True):
    st.success("Escolha o ano logo abaixo")
    ano_selecionado = st.selectbox("", anos_disponiveis)

# ========================
# Contar músicas do ano
# ========================
ano_selecionado = int(ano_selecionado)
query_count = """
SELECT COUNT(*) as total
FROM dados_spotify
WHERE year = %s
"""

total_musicas_ano = pd.read_sql(
    query_count,
    conn,
    params=(ano_selecionado,)
)["total"][0]

# ========================
# Slider
# ========================
max_top = min(30, total_musicas_ano)

with st.container(border=True):
    st.success(f"Quantidade de músicas a exibir (1 a {max_top})")
    top_n = st.slider("", 1, max_top, min(10, max_top))

# ========================
# Buscar TOP músicas direto do banco
# ========================
query_top = """
SELECT title, artist, pop
FROM dados_spotify
WHERE year = %s
ORDER BY pop DESC
LIMIT %s
"""

top = pd.read_sql(
    query_top,
    conn,
    params=(ano_selecionado, top_n)
)

# Criar coluna combinada
top["musica_artista"] = top["title"] + " — " + top["artist"]

# ========================
# Gráfico
# ========================
fig = px.bar(
    top,
    x="pop",
    y="musica_artista",
    orientation="h",
    color="pop",
            color_continuous_scale=[
        "#16a34a",
        "#15803d",
        "#166534",
        "#14532d",
        "#0b3d2e"
    ],
    title=f"Top {top_n} músicas mais populares de {ano_selecionado}"
)

fig.update_layout(
    height=500,

    yaxis=dict(
        title="",
        autorange="reversed",
        tickfont=dict(family="Poppins", size=13, color="#000000"),
        title_font=dict(family="Poppins", size=14, color="#000000")
    ),

    xaxis=dict(
        title="Popularidade",
        tickfont=dict(family="Poppins", size=12, color="#000000"),
        title_font=dict(family="Poppins", size=14, color="#000000")
    ),

    title_font=dict(
        family="Poppins",
        size=22,
        color="#000000"
    ),

    font=dict(
        family="Poppins",
        size=12,
        color="#000000"
    )
)

st.subheader("Gráfico de popularidade")
st.plotly_chart(fig, use_container_width=True)


with st.container(border=True):
    mostrar_tabela = st.checkbox("Mostrar tabela com detalhes das músicas")

    if mostrar_tabela:
        top_exibir = top[["title", "artist", "pop"]].copy()
        top_exibir.columns = ["Música", "Artista", "Popularidade"]

        st.markdown(f"### Lista de Top {top_n} músicas - {ano_selecionado}")

        musicas_style = (
            top_exibir.style
            .set_table_styles([
            { 'selector': 'th.col_heading', 'props': [('background-color', PERSON["cor_cabecalho_fundo"]), ('color',PERSON["cor_texto_cabecalho"])] },
            { 'selector': 'th.index_name', 'props': [('background-color', PERSON["cor_cabecalho_fundo"]), ('color', PERSON["cor_texto_cabecalho"])] },
            ])
            )
        tabela = st.table(musicas_style)










