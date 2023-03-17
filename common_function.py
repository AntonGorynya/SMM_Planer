import requests
from urllib.parse import urlparse
import os


def download_image(url, image_name):
    response = requests.get(url)
    response.raise_for_status()
    with open(image_name, 'wb') as file:
        file.write(response.content)


def get_file_extension(url):
    path = urlparse(url).path
    path, extension = os.path.splitext(path)
    return extension