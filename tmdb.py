import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# TMDB API configuration
API_KEY = "6729c4cad6820ce8cfdfc6ffe135b332"
BASE_URL = "https://api.themoviedb.org/3"

def get_movies(page_limit=3):  
    all_movies = []
    for page in range(1, page_limit + 1):  
        endpoint = f"{BASE_URL}/movie/popular"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "page": page,  
        }
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            movies = response.json().get("results", [])
            all_movies.extend(movies) 
        else:
            print(f"Error fetching page {page}: {response.status_code}")
            break


    genres = get_genres()
    for movie in all_movies:
        movie["genre_names"] = [genres.get(genre_id, "Unknown") for genre_id in movie.get("genre_ids", [])]

    return all_movies

def get_genres():
    endpoint = f"{BASE_URL}/genre/movie/list"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return {genre["id"]: genre["name"] for genre in response.json().get("genres", [])}
    return {}
