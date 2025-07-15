import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get API keys and host from environment variables
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
WATCHMODE_API_KEY = os.getenv("WATCHMODE_API_KEY")

# Function to search movies by title using the IMDb API via RapidAPI 
def search_movies(title):
    url = "https://imdb236.p.rapidapi.com/api/imdb/search"
    querystring = {
        "primaryTitleAutocomplete": title,  # Search by title
        "type": "movie",                    # Restrict to movies
        "rows": "25"                        # Limit results
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    # Send request to RapidAPI/IMDb
    response = requests.get(url, headers=headers, params=querystring)

    # Print debug info to console (status and raw response)
    print("Status:", response.status_code)
    print("Content:", response.text)

    # If request failed, return empty list
    if response.status_code != 200:
        return []
    
    # Parse the JSON and extract the 'results' field
    data = response.json()
    results = data.get("results", [])

    # Ensure result is a list
    if not isinstance(results, list):
        return []

    return results

# --- Function to convert IMDb ID to Watchmode title ID ---
def get_watchmode_id_by_imdb(imdb_id):
    url = f"https://api.watchmode.com/v1/search/"
    params = {
        "apiKey": WATCHMODE_API_KEY,
        "search_field": "imdb_id",          # Use IMDb ID as search field
        "search_value": imdb_id             # The actual IMDb ID to look up
    }

    # Send request to Watchmode API
    response = requests.get(url, params=params)

    # Return None if failed
    if response.status_code != 200:
        return None

    # Extract first result's ID if available
    results = response.json().get("title_results", [])
    return results[0].get("id") if results else None

# Function to fetch streaming platforms for a given Watchmode title ID 
def get_streaming_sources(watchmode_id):
    url = f"https://api.watchmode.com/v1/title/{watchmode_id}/sources/"
    params = {"apiKey": WATCHMODE_API_KEY}

    # Send request to Watchmode to get streaming options
    response = requests.get(url, params=params)

    # Return empty list if request failed
    if response.status_code != 200:
        return []

    # Return list of sources (platforms)
    return response.json()
