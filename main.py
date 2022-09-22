import requests
from bs4 import BeautifulSoup
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

format_YYYYMMDD = "%Y-%m-%d"
URL = "https://www.billboard.com/charts/hot-100/"

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]

params = {
    "client_id": SPOTIPY_CLIENT_ID,
    "client_secret": SPOTIPY_CLIENT_SECRET,
    "redirect_uri": SPOTIPY_REDIRECT_URI,
}


while True:
    req_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")
    print(req_date[:4])
    try:
        date = datetime.strptime(req_date, format_YYYYMMDD)
        if int(req_date[:4]) < 1900:
            print("There was no music back there, try again.")
            continue
        else:
            break
    except ValueError:
        print("The string is not a date with format YYYY-MM-DD")

response = requests.get(f"{URL}{req_date}")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

song_name_sc = soup.find_all(name="h3", id="title-of-a-story", class_="a-truncate-ellipsis")

song_names = [song.getText().strip("\n\t") for song in song_name_sc]

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()

for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])
