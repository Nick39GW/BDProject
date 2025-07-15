import os
from dotenv import load_dotenv
import requests

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

url = "https://imdb236.p.rapidapi.com/api/imdb/search/"
headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}
params = {"primaryTitleAutocomplete": "Interstellar"}

res = requests.get(url, headers=headers, params=params)
print(res.status_code)
print(res.text)
