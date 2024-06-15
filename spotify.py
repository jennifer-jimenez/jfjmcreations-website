"""
spotify.py

Module for handling Spotify API calls.
"""

import os
import base64
import json
import string
import random

from dotenv import load_dotenv
from requests import post, get

class ContentItem:
    """Generic representation of one data content item, used e.g. in search results."""
    def __init__(self, content_id, content_type, name, image, artists=None):
        self.content_id = content_id
        self.content_type = content_type
        self.name = name
        self.image = image
        self.artists = artists

    def __repr__(self):
        return f"{self.content_type}: {self.name}"

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/"

def get_token():
    """Get token from Spotify API"""
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def get_auth_header(token):
    """Get auth header"""
    return { "Authorization": "Bearer " + token}

def get_top_content(artist_id):
    """Get content name, image, and artists if any from content id and type"""
    token = get_token()
    header = get_auth_header(token)

    query_url = SPOTIFY_ENDPOINT + f"artists/{artist_id}/top-tracks"

    response = get(query_url, headers=header)
    items = json.loads(response.content)["tracks"]

    content = []
    for item in items:
        content_id = item["id"]
        name = item["name"]

        # index correctly into json based for track or album response, then select first image url
        images_list = item["album"]["images"]
        image = images_list[0]["url"] if images_list else None

        artists = []
        for artist in item["artists"]:
            artists.append(artist["name"])

        # format into content display class
        content_item = ContentItem(content_id, "track", name, image, artists)
        content.append(content_item)

    return content

