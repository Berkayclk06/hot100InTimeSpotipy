import requests
from bs4 import BeautifulSoup
from datetime import datetime
import spotipy
import os

format_YYYYMMDD = "%Y-%m-%d"
URL = "https://www.billboard.com/charts/hot-100/"

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]

#################### INPUT CHECK #######################

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

##################### WEB SCRAPING #########################

response = requests.get(f"{URL}{req_date}")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

song_name_sc = soup.find_all(name="h3", id="title-of-a-story", class_="a-truncate-ellipsis")

song_names = [song.getText().strip("\n\t") for song in song_name_sc]

################### SPOTIFY API ##########################

scope = "playlist-modify-private"

spotify_auth = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                           client_secret=SPOTIPY_CLIENT_SECRET,
                                           redirect_uri=SPOTIPY_REDIRECT_URI,
                                           scope=scope,
                                           cache_path=".cache")

################### SEARCH SONGS ######################
song_uris = []
year = req_date[:4]
sp = spotipy.Spotify(oauth_manager=spotify_auth)

################## BEFORE RUNNING THE CODE UNCOMMENT CODE AND GET A .cache FILE ################
################## AFTER GETTING THE FILE YOU MUST COMMENT OUT THE CODE LINE AGAIN. ################

# access_token = spotify_auth.get_access_token()

user_id = sp.current_user()["id"]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

################# CREATE & ADD SONGS TO PLAYLIST ################

playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{req_date} Billboard 100",
                                   public=False)

sp.playlist_add_items(playlist["id"], song_uris)
