import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import ast

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

TMDB_API_KEY ="3d28d52800d347b1afba0c87a208f9bb"

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#FF4B4B;
}
.movie-card {
    background-color:#1e1e1e;
    padding:15px;
    border-radius:12px;
    margin-bottom:15px;
}
.rating {
    color:gold;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("movies_metadata.csv", low_memory=False)
    df = df[['title','overview','genres','vote_average']]
    df.dropna(inplace=True)
    
    # Reduce dataset size to prevent memory issues
    df = df.head(10000)
    
    return df

movies = load_data()

# -----------------------------
# GENRE CLEANING
# -----------------------------
def extract_genres(x):
    try:
        genres = ast.literal_eval(x)
        return [i['name'] for i in genres]
    except:
        return []

movies['genre_list'] = movies['genres'].apply(extract_genres)

# Get unique genres
all_genres = sorted(list(set(g for sublist in movies['genre_list'] for g in sublist)))

# -----------------------------
# TF-IDF MODEL
# -----------------------------
@st.cache_resource
def create_tfidf_matrix(data):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['overview'])
    return tfidf_matrix

tfidf_matrix = create_tfidf_matrix(movies)

# Create title index mapping
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# -----------------------------
# RECOMMEND FUNCTION
# -----------------------------
def get_recommendations(title, num_recommendations=6):
    if title not in indices:
        return pd.DataFrame()

    idx = indices[title]

    # Compute similarity only for selected movie
    cosine_sim = linear_kernel(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()

    sim_scores = list(enumerate(cosine_sim))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Skip first (same movie)
    sim_scores = sim_scores[1:num_recommendations+1]

    movie_indices = [i[0] for i in sim_scores]

    return movies.iloc[movie_indices]

# -----------------------------
# TMDB POSTER FUNCTION
# Uses The Movie Database API
# -----------------------------
def fetch_poster(movie_title):
    if not TMDB_API_KEY:
        return "https://via.placeholder.com/300x450?text=No+Image"

    search_url = "https://api.themoviedb.org/3/search/movie"
    
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }

    try:
        response = requests.get(search_url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("results"):
            poster_path = data["results"][0].get("poster_path")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except Exception as e:
        print("Poster Fetch Error:", e)

    return "https://via.placeholder.com/300x450?text=No+Image"
# -----------------------------
# UI START
# -----------------------------
st.markdown('<div class="main-title"> AI Movie Recommendation System</div>', unsafe_allow_html=True)
st.write("Find movies with Posters, Ratings & Genre Filter")

# Genre Filter
selected_genre = st.selectbox(" Select Genre", ["All"] + all_genres)

filtered_movies = movies.copy()

if selected_genre != "All":
    filtered_movies = movies[movies['genre_list'].apply(lambda x: selected_genre in x)]

# Movie Selection
selected_movie = st.selectbox(" Select Movie", filtered_movies['title'].values)

# Recommendation Button
if st.button("Recommend"):
    recommendations = get_recommendations(selected_movie)

    if recommendations.empty:
        st.error("Movie not found.")
    else:
        st.subheader(" Recommended Movies")

        cols = st.columns(3)

        for i, (_, row) in enumerate(recommendations.iterrows()):
            poster = fetch_poster(row['title'])
            rating = row['vote_average']

            with cols[i % 3]:
                st.image(poster, use_container_width=True)
                st.markdown(f"**{row['title']}**")
                st.markdown(f"<div class='rating'> {rating}</div>", unsafe_allow_html=True)