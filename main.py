# from main.downloader import SpotifyDownloader
# from lib.IO import find_album_file

from src.main.downloader import SpotifyDownloader
from src.lib.IO import find_album_file


def main():
    spot = SpotifyDownloader()
    # album_file = input("Enter Directory to album URLs file: ")
    album_file = "albums.txt"

    urls = find_album_file(album_file)

    spot.download_albums(urls)


if __name__ == "__main__":
    main()