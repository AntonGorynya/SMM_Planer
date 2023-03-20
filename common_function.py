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


def format_text(text):
    text = text.replace('-', '–')
    formated_text = []
    for word in text.split():
        if word[0] == '\"' and word[-1] == '\"':
            word = word.replace('\"', '«', 1)
            word = word.replace('\"', '»', 1)
        formated_text.append(word)
    return ' '.join(formated_text)


if __name__ == '__main__':
    pass