import os
from dotenv import load_dotenv
import requests

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
WATCHMODE_API_KEY = os.getenv("WATCHMODE_API_KEY")

def search_movies(title):
    url = "https://imdb236.p.rapidapi.com/api/imdb/search"
    querystring = {
        "primaryTitleAutocomplete": title,
        "type": "movie",
        "rows": "25"
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
        
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        return {"error": True, "message": "API request failed"}

    return response.json().get("results", [])


def get_watchmode_id_by_imdb(imdb_id):
    url = f"https://api.watchmode.com/v1/search/"
    params = {
        "apiKey": WATCHMODE_API_KEY,
        "search_field": "imdb_id",
        "search_value": imdb_id
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    results = response.json().get("title_results", [])
    return results[0].get("id") if results else None


def get_streaming_sources(watchmode_id):
    url = f"https://api.watchmode.com/v1/title/{watchmode_id}/sources/"
    params = {"apiKey": WATCHMODE_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []
    return response.json()

