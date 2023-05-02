import os
from .logging import Logger


def file_exists(file):
    return os.path.exists(os.path.join(os.getcwd(), file))

def find_album_file(file):
    logger = Logger()

    if not file_exists(file):
        logger.log(logger.LogLevel.FATAL, f"Failed to find {file}!")
        exit(1)
    
    # Check the general stats of the file

    if os.stat(os.path.join(os.getcwd(), file)).st_size == 0:
        logger.log(logger.LogLevel.FATAL, f"{file} is empty!")
        exit(1)
    
    urls = _extract_urls(file)

    return urls
    
def _extract_urls(file):
    with open(file, "r") as f:
        urls = f.read().splitlines()
    
    return urls