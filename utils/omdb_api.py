import requests
import dotenv
import os


dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')

def fetch_movie_details(movie_title):
    """
    Loads movie data from OMDb API using the movie title.
    Returns dictionary with movie data or None if error.
    """
    api_url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_title}"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data["Response"] == "True":
            return data
        else:
            print("Movie not found!")
            return None
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)
        return None
