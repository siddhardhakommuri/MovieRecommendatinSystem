import streamlit as st 
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-us'.format(movie_id))
    if response.status_code == 200:
        data = response.json()
        
        return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
    else:
        return False
def recommend(movie_title):
    if movie_title in movies['title'].values: 
        movie_index = movies[movies['title'] == movie_title].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        # st.text(movies_list)
        recommended=[]
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            # st.text(movie_id)
            recommended.append(movies.iloc[i[0]].title)
            result = fetch_poster(movie_id)
            if result !=False:
                recommended_movies_posters.append(result)
        return recommended,recommended_movies_posters
    else:
        return False

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")

selected_movie_name = st.selectbox('enter movie name',movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    col = st.columns(5)  

    for i in range(len(posters)):
        with col[i]:
            st.text(names[i])
            st.image(posters[i])

