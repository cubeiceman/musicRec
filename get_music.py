import json
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# call from terminal: python ./get_music.py

clientID = 'XXX'
clientSecret = 'XXX'
redirect_uri = 'https://google.com/callback/'
scope="user-library-read"

def main():
    oauth_object = SpotifyOAuth(client_id=clientID,
                                client_secret=clientSecret,
                                redirect_uri=redirect_uri,
                                scope=scope)
    sp = spotipy.Spotify(auth_manager=oauth_object)
    
    categories = sp.categories()["categories"]
    while categories:
        for item in categories["items"]:
            print(f"Category name:{item["name"]}")
        if categories["next"]:
            categories = sp.next(categories)["categories"]
        else:
            categories = None

if __name__ == "__main__":
    main()
    