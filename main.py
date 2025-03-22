# pyxfluff 2025

from pydantic import BaseModel
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse, PlainTextResponse

import os
import httpx
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    name: str
    artist: Optional[str] = None
    album: Optional[str] = None

def load_config():
    config = {}
    if not os.path.exists(".config"):
        print(
            f"Config file not found. Please create one from the .config.template file."
        )
        return None

    with open(".config", "r") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            config[key] = value
    return config

def fetch_token():
    config = load_config()
    if not config:
        return None

    if not config.get("CLIENT_ID") or not config.get("CLIENT_SECRET"):
        print("bad configuration data, please refer to the example")
        return None

    response = httpx.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": "Basic "
            + base64.b64encode(
                f"{config.get('CLIENT_ID')}:{config.get('CLIENT_SECRET')}".encode()
            ).decode(),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
    )

    return response.json().get("access_token")


def search(song_name, artist=None, album=None):
    token = fetch_token()
    if not token:
        print("Failed to get token, please ensure your configuration file is correct")
        return None

    query = f"{song_name}"
    if artist:
        query += f" artist:{artist}"
    if album:
        query += f" album:{album}"

    data = httpx.get(
        f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1",
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    tracks = data.get("tracks", {}).get("items", [])
    if not tracks:
        print("No song found")
        return None

    track_id = tracks[0]["id"]
    song_title = tracks[0]["name"]
    song_artist = tracks[0]["artists"][0]["name"]
    album_name = tracks[0]["album"]["name"]

    embed_url = f"https://open.spotify.com/embed/track/{track_id}"

    return {
        "title": song_title,
        "artist": song_artist,
        "album": album_name,
        "embed_url": embed_url,
    }

@app.get("/")
def root():
    return RedirectResponse("https://github.com/pyxfluff/spotify_embedpy")

@app.get("/status")
def status():
    return PlainTextResponse("OK")

@app.post("/search")
def search_route(data: List[SearchRequest]):
    results = []
    for query in data:
        results.append(search(query.name, query.artist, query.album))

    return JSONResponse(results)

