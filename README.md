# Spotify Embed Generator

A small program which serves a FastAPI webserver to get embeds from Spotify based on a song name, artist, or album.

## Setup

Copy `.config.tmp` to `.config` and enter your Spotify-generated credentials, which [you can generate here.](https://developer.spotify.com/dashboard)

Install packages with `pip install httpx uvicorn fastapi` and you're done! Just run `uvicorn main:app`. You can also fork the code and remove the webserver if you want, this is just how I built it.

## Usage

POST /search

In:
```json
[
    {
        "name": "Misery Business"
    },
    {
        "name": "Into You",
        "artist": "Ariana Grande"
    }
]
```

Out:
```json
[
    {
        "title": "Misery Business",
        "artist": "Paramore",
        "album": "Riot!",
        "embed_url": "https://open.spotify.com/embed/track/6SpLc7EXZIPpy0sVko0aoU"
    },
    {
        "title": "Into You",
        "artist": "Ariana Grande",
        "album": "Dangerous Woman",
        "embed_url": "https://open.spotify.com/embed/track/63y6xWR4gXz7bnUGOk8iI6"
    }
]
```
