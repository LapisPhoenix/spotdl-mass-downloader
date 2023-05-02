import os
import time
import subprocess
import json
import spotipy
# from lib.logging import Logger, Colorization
from ..lib.logging import Logger, Colorization
from spotipy.oauth2 import SpotifyClientCredentials
from concurrent.futures import ThreadPoolExecutor, as_completed


class SpotifyDownloader:
    def __init__(self) -> None:
        self.logger = Logger()
        self.color = Colorization()
    
    def spotify_setup(self, file: str = "config.json") -> spotipy.Spotify:
        """
        Load settings and create spotify instance.

        ### Arguments
        - file: Path to .env file

        ### Returns
        - A instance of Spotify
        """

        # Check if .env file exists
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} not found")
        
        # Load settings

        with open("config.json", "r") as f:
            data: dict = json.load(f)
            output = data.get('Output', '.\\output')
            spotify = data.get('spotify')
            client_id = spotify.get('clientID')
            client_secret = spotify.get('clientSecret')

            if not all([data, output, spotify, client_id, client_secret]):
                raise ValueError("One of your settings is empty! Please fill it!")
        
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


    def execute(self, command: str, *args: list[str]) -> tuple[str, bool]:
        """
        Execute a command.

        ### Arguments
        - command: Command to execute
        - args: Arguments to pass to command

        ### Returns
        - A tuple containing the output and a boolean indicating success
        """
        try:
            output = subprocess.check_output([command, *args])
            success = True
        except Exception as e:
            output = str(e)
            success = False

        return output, success



    def download_album(self, album_link: str) -> None:
        """
        Download an album.

        ### Arguments
        - album_link: Link to album

        ### Notes
        - This function is multi-threaded.
        """
        spotify = self.spotify_setup()

        start_time = time.time()
        try:
            # Get album name & artist
            album = spotify.album(album_link)
            name = album["name"]
            artist = album["artists"][0]["name"]

            download_path = f"{name} - {artist}"

            # Check if album is already downloaded
            if os.path.exists(os.path.join(os.getcwd(), download_path)):
                self.logger.log(self.logger.LogLevel.INFO, f"{download_path} is already found in directory, ignoring. (From URL {album_link})")
                return

            # Download songs
            self.logger.log(self.logger.LogLevel.INFO, f"Downloading {download_path}")
            output, success = self.execute("spotdl", album_link, "--overwrite", "skip", "--output", download_path)  # Update this line
            end_time = time.time()
            self.logger.log(self.logger.LogLevel.INFO, f"Downloaded {download_path} in {self.logger.colorize(self.logger.Colors.BLUE, str(round(start_time - end_time, 2)))} seconds.")
            
        except Exception as e:
            # If the album link is not an album link
            if str(e) == "http status: 400, code:-1 - Unexpected Spotify URL type., reason: None":
                self.logger.log(self.logger.LogLevel.WARN, f"Invalid album link: {album_link}")
        
        return


    def download_albums(self, urls: list[str]) -> None:
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
        self.logger.log(self.logger.LogLevel.INFO, "Adding albums to queue.")
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.download_album, url) for url in urls]
            self.logger.log(self.logger.LogLevel.INFO, f"{self.color.colorize(self.color.Colors.BLUE, str(len(urls)))} albums in queue.")

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    if str(e) == "cannot access local variable 'download_path' where it is not associated with a value":
                        self.logger.log(self.logger.LogLevel.FATAL, f"Invalid Client ID or Client Secret!")
                        exit(1)
                    else:
                        self.logger.log(self.logger.LogLevel.WARN, f"An error occurred: {self.color.colorize(self.color.Colors.RED, str(e))}")
