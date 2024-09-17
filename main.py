import pandas as pd
import streamlit as st
import os
from PIL import Image

# CARREGAMENTO E ETL
@st.cache_data
def load_data():
    df = pd.read_csv(r'C:\Users\mis.adiel\Desktop\Desenvolvimento Py\Aquivos\movies.csv')
    df['date'] = df['date'].fillna(-1).astype(int)
    return df

#CARREGAMENTO DOS POSTERS
posters_dir = r'C:\Users\mis.adiel\Desktop\Desenvolvimento Py\Aquivos\posters'

data_df = load_data()

@st.cache_data
def calculate_general_mean(df):
    return df['rating'].mean()

geral_mean = calculate_general_mean(data_df)

# CRIA A SELECT BOX COM OS NOMES DE FILMES DA COLUNA NAME
if 'selected_name' not in st.session_state:
    st.session_state.selected_name = data_df['name'].iloc[0]

selected_name = st.sidebar.selectbox('Escolha um filme:', data_df['name'], index=data_df['name'].tolist().index(st.session_state.selected_name))
st.session_state.selected_name = selected_name
selected_movie = data_df[data_df['name'] == selected_name]

# Verifica se o filme foi encontrado antes de acessar os valores
if not selected_movie.empty:
    rating = selected_movie['rating'].values[0]
    release_yr = selected_movie['date'].values[0]
    lenght = selected_movie['minute'].values[0]
    movie_id = selected_movie['id'].values[0]

    poster_path = os.path.join(posters_dir, f'{movie_id}.jpg')

    # TEXTOS DE CABEÇA
    st.title('Kino Data')
    st.title(f'Selected movie: {selected_name}')
    st.write(f'The rate of this movie is: {rating}')
    st.write(f'The mean of evaluations at Letterbox is {geral_mean:.2f}')
    st.write(f'{selected_name} was released in {release_yr}')
    st.write(f'Movie length: {lenght} minutes')

    if os.path.exists(poster_path):
        poster_image = Image.open(poster_path)
        st.image(poster_image, caption=f'Poster of {selected_name}', use_column_width = False)
    else:
        st.write("Poster não encontrado!")
else:
    st.write("Filme não encontrado!")


