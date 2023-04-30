import os
import sys
import time
import subprocess
import dotenv
import spotipy
import colorama
from spotipy.oauth2 import SpotifyClientCredentials
from concurrent.futures import ThreadPoolExecutor



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
    except:
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

        # Download songs
        execute("spotdl", album_link, "--overwrite", "skip", "--output", download_path)
        print(f"{colorama.Fore.GREEN}Downloaded {name} - {artist} in {round(time.time() - start, 2)} seconds.{colorama.Style.RESET_ALL}")
    except Exception as e:
        print(f"{colorama.Fore.RED}Failed to download album from {album_link}. Error: {e}{colorama.Style.RESET_ALL}")


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
        executor.map(lambda url: download_album(url), urls)


def main():
    """
    Main function.
    """

    colorama.init()

    # Check if albums.txt exists

    if not os.path.exists("albums.txt"):
        print(f"{colorama.Fore.RED}albums.txt not found.{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Creating albums.txt...{colorama.Style.RESET_ALL}")
        
        # Create albums.txt
        with open("albums.txt", "w") as file:
            file.close()
        print(f"{colorama.Fore.GREEN}Created albums.txt.{colorama.Style.RESET_ALL}")

        return sys.exit(1)

    # Check if albums.txt is empty
    if os.stat("albums.txt").st_size == 0:
        print(f"{colorama.Fore.RED}albums.txt is empty.{colorama.Style.RESET_ALL}")
        return sys.exit(1)

    # Read albums.txt

    with open("albums.txt", "r") as file:
        albums = file.read().split("\n")
    
    # Download albums

    print(f"{colorama.Fore.YELLOW}Downloading {colorama.Style.BRIGHT}{len(albums)}{colorama.Style.NORMAL} albums...{colorama.Style.RESET_ALL}")

    start_time = time.time()

    download_albums(albums)

    print(f"{colorama.Fore.GREEN}Downloaded {colorama.Style.BRIGHT}{len(albums)}{colorama.Style.NORMAL} albums in {round(time.time() - start_time, 2)} seconds.{colorama.Style.RESET_ALL}")


if __name__ == "__main__":
    main()
