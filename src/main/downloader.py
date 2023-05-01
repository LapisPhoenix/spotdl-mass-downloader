import os
import sys
import time
import subprocess
import dotenv
import spotipy
from lib.logging import Logger
from spotipy.oauth2 import SpotifyClientCredentials
from concurrent.futures import ThreadPoolExecutor, as_completed


class SpotifyDownloader:
    def __init__(self) -> None:
        self.logger = Logger()


def spotify_setup(file: str = ".env") -> spotipy.Spotify:
    """
    Load environment variables from .env file.

    ### Arguments
    - file: Path to .env file

    ### Returns
    - A instance of Spotify
    """

    # Check if .env file exists
    if not os.path.exists(file):
        raise FileNotFoundError(f"{file} not found")
    
    # Load environment variables

    dotenv.load_dotenv(file)

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # Check if client id and client secret are set

    if client_id is None or client_secret is None:
        raise ValueError(
            "SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set in .env file"
        )
    
    # Check if client id and client secret are valid

    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
    except Exception:
        raise ValueError(
            "SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be valid"
        )
    
    # Return Spotify instance

    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def execute(command: str, *args: list[str]) -> str:
    """
    Execute a command.

    ### Arguments
    - command: Command to execute
    - args: Arguments to pass to command
    """

    return subprocess.check_output([command, *args])


def download_album(album_link: str) -> None:
    """
    Download an album.

    ### Arguments
    - album_link: Link to album

    ### Notes
    - This function is multi-threaded.
    """
    spotify = spotify_setup()

    start = time.time()
    try:
        # Get album name & artist
        album = spotify.album(album_link)
        name = album["name"]
        artist = album["artists"][0]["name"]

        download_path = f"{name} - {artist}"

        # Check if album is already downloaded

        if os.path.exists(os.path.join(os.getcwd(), download_path)):
            print(f"{colorama.Fore.RED}{download_path} already downloaded.{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.YELLOW}Ignoring {download_path} as it has already been found within the directory. (From URL {album_link}) {colorama.Style.RESET_ALL}")

            return


        # Download songs
        print(f"{colorama.Fore.YELLOW}Downloading {download_path}{colorama.Style.RESET_ALL}")
        execute("spotdl", album_link, "--overwrite", "skip", "--output", download_path)
        print(f"{colorama.Fore.GREEN}Downloaded  {download_path} in {colorama.Style.BRIGHT}{round(time.time() - start, 2)}{colorama.Style.NORMAL} seconds.{colorama.Style.RESET_ALL}")
    except Exception as e:
        # If the album link is not an album link
        if str(e) == "http status: 400, code:-1 - Unexpected Spotify URL type., reason: None":
            print(f"{colorama.Fore.RED}Invalid album link: {album_link}{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.RED}Failed to download in {colorama.Style.BRIGHT}{round(time.time() - start, 2)}{colorama.Style.NORMAL} seconds.{colorama.Style.RESET_ALL}")
        else:
            print(f"{colorama.Fore.RED}Failed to download album from {album_link}. Error: {e}{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.RED}Failed to download in {colorama.Style.BRIGHT}{round(time.time() - start, 2)}{colorama.Style.NORMAL} seconds.{colorama.Style.RESET_ALL}")

        return


def download_albums(urls: list[str]) -> None:
    """
    Download a list of albums.
    
    ### Arguments
    - urls: List of album links
    
    ### Notes
    - This function is multi-threaded.
    
    ### Example
    ```py
    download_albums([
        "https://open.spotify.com/album/6QPkyl04rXwTGlGlcYaRoW",
        "https://open.spotify.com/album/6QPkyl04rXwTGlGlcYaRoW",
        ])
    ```
    """
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_album, url) for url in urls]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"{colorama.Fore.RED}An error occurred: {e}{colorama.Style.RESET_ALL}")
