import streamlit as st
import pickle
import pandas as pd
import requests
import time

# TMDB API key
API_KEY = '04e6c51a12f4aea00a7f7aec3eb5e271'

# 🔍 Function to fetch poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            # Optional check to confirm image is reachable
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                return image_url
            else:
                print(f"[WARNING] Invalid poster URL: {image_url}")
        else:
            print(f"[WARNING] No poster path for movie_id: {movie_id}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch movie_id {movie_id}: {e}")

    return "https://via.placeholder.com/300x450?text=No+Image"

# 🔃 Recommendation function
def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        time.sleep(0.2)  # Optional: avoid hitting TMDB too fast
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# 📦 Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🎬 Streamlit UI
st.title('🎥 Movie Recommendation System')
movie_list = movies['title'].values
selected_movie = st.selectbox('Which movie do you want to recommend?', movie_list)

if st.button('Recommend Movie'):
    recommended_movies, recommended_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movies[idx])
            st.image(recommended_posters[idx])
