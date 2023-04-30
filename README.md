# spotdl-mass-downloader
Basically a wrapper around spotdl to download songs in mass quanitites.


# Installation
Inside your terminal perform the following command


```
python -m pip install requirements.txt
```

1. Goto [The Spotify Dashboard](https://developer.spotify.com/)
2. Create an application
3. Grab both the client ID and client secret
4. Back inside the files, rename `renametodotenv` to `.env`
5. Inside `.env` fill out the params

# Usage
Run the following command
1. Create a `albums.txt` file
2. Inside the `albums.txt` file enter each album URL with a new line between each URL
3. Run the command: `python main.py`
