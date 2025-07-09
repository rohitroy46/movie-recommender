import pickle
import requests
import pandas as pd

API_KEY = '04e6c51a12f4aea00a7f7aec3eb5e271'

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movie_df = pd.DataFrame(movies_dict)

poster_cache = {}

for movie_id in movie_df['movie_id']:
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster_path = data.get('poster_path')
        if poster_path:
            poster_cache[movie_id] = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception as e:
        print(f"Failed for movie_id {movie_id}: {e}")

# Save the poster cache
with open('poster_cache.pkl', 'wb') as f:
    pickle.dump(poster_cache, f)

print("✅ poster_cache.pkl created successfully.")
