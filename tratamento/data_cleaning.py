
import pandas as pd 
import numpy as np


df = pd.read_csv("archive/top50.csv")
df_spotify = df




df_spotify.head()


df.rename(columns={'Trace.Name': 'novo1', 'velho2': 'novo2'}, inplace=True)



df_spotify.rename(columns={
    'Unnamed: 0': 'id',
    'Track.Name': 'nome_musica',
    'Artist.Name': 'nome_artista',
    'Genre': 'genero',
    'Beats.Per.Minute': 'batidas_por_minuto',
    'Energy': 'energia',
    'Danceability': 'dancabilidade',
    'Loudness..dB.': 'volume_db',
    'Liveness': 'ao_vivo',
    'Valence.': 'valencia',
    'Length.': 'duracao_segundos',
    'Acousticness..': 'acustica',
    'Speechiness.': 'fala',
    'Popularity': 'popularidade'
}, inplace=True)



df_spotify.head()






df_spotify.loc[50,'nome_musica'] = 'Cross Me (feat. Chance the Rapper e PnB Rock'


df_spotify.loc[39, 'nome_musica'] = 'fuck, i m lonely (with Anne-Marie) - from.13'


df_spotify.loc[7,'nome_musica'] = 'How Do You Sleep'


df_spotify.loc[32,'nome_musica'] = 'Maluma'


df_spotify.loc[44,'nome_artista'] ='ROSALA'


df_spotify.drop(index=50, inplace=True)

df_spotify = df_spotify.drop(columns=["id"])

df_spotify.to_csv('spotify_limpo.csv')
