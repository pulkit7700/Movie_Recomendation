import streamlit as st
import pickle
import pandas as pd 
import requests
import _pickle as cPickle
import bz2

def decompress_pickle(file):
 data = bz2.BZ2File(file, 'rb')
 data = cPickle.load(data)
 return data


movies_list = pickle.load(open('movie_dict.pkl', 'rb'))
#similarity = pickle.load(open('similarity.pkl', 'rb'))
similarity = decompress_pickle('similarity_1.pbz2')

movies = pd.DataFrame(movies_list)

def fetch_poster(id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c84df4a03a7d1ae3c2fd9a0702593375'.format(id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommend_movie = []
    recommend_movie_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_movie_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_movie_poster


st.title('Movie Recommender System')


selected_movie_name = st.selectbox(
    'Select a Movie',
    movies['title'].values)

st.write('You selected:', selected_movie_name)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])