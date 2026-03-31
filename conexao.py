import pandas as pd
from sqlalchemy import create_engine

# ler csv
df = pd.read_csv("data/todas_musicas_limpo.csv")

# conexão postgres
engine = create_engine(
"postgresql+psycopg2://postgres:postgres@localhost:5432/Spotify"
)

# enviar dataframe
df.to_sql("dados_spotify", engine, if_exists="replace", index=False)

print("Dados enviados para o banco!")