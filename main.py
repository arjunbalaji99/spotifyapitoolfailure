import json
from dotenv import load_dotenv
import os
import requests
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    token_url = "https://accounts.spotify.com/api/token"
    token_params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = post(token_url, data=token_params)
    response.raise_for_status()
    token_data = response.json()
    return token_data["access_token"]

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    jsonresult = json.loads(result.content)["artists"]["items"]
    if len(jsonresult) > 0:
        return jsonresult[0]
    return None

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    params = {
        "market": "US"
    }
    headers = get_auth_header(token)
    response = get(url, headers=headers, params=params)

    jsonresult = json.loads(response.content)["tracks"]
    return jsonresult

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    params = {
        "include_groups": "single",
        "market": "US",
        "limit": 20,
        "offset": 0
    }
    response = requests.get(url, headers=headers, params=params)
    return json.loads(response.content)["items"]
    

token = "BQDrKD0PKdbC_p1nzuVPpyC461pj4t6hbg7RU8RAaxqP6kYIN-gZBqxALvmbwGBb2ySBFglrwIuNQNWvBgly-DUHsBAx3_dXW86fDsjqMRCDszy5j-g"
result = search_for_artist(token, "the weekend")
print(result["name"])
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")
print()
albums = get_albums_by_artist(token, artist_id)
for idx, album in enumerate(albums):
    print(f"{idx + 1}. {album['name']}")