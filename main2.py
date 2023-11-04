from dotenv import load_dotenv
import os
import requests
from requests import post, get
from urllib.parse import quote

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:3000"

auth_url = "https://accounts.spotify.com/authorize"
auth_params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": "user-top-read"
}

authorization_url = requests.Request("GET", auth_url, params = auth_params).prepare().url
print("Please authorize the application by visiting the following URL:")
print(authorization_url)
authorization_code = input("Enter the authorization code from the redirect URI: ")

token_url = "https://accounts.spotify.com/api/token"
token_params = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "client_secret": client_secret,
}

# Exchange the authorization code for an access token
token_response = requests.post(token_url, data=token_params)
token_data = token_response.json()

# Extract the access token from the response
access_token = token_data.get("access_token")
refresh_token = token_data.get("refresh_token")

# Print the access token (you can store it securely for future use)
print("Access Token:", access_token)
print("Refresh Token:", refresh_token)