import os
import random
import shutil
import requests

from tqdm import tqdm
from yandex_images_parser import Parser


def find_images(plant: str, number: int, delay: float = 6.0, **kwargs) -> list:
    """Searches for images on request, returns a list of links"""
    parser = Parser()
    delay = randomize_delay(delay)

    return parser.query_search(query=plant, limit=number, delay=delay, **kwargs)


def find_similar_images(url: str, number: int, delay: float = 6.0, **kwargs) -> list:
    """Searches for similar images, returns a list of links"""
    parser = Parser()
    delay = randomize_delay(delay)

    return parser.image_search(url=url, limit=number, delay=delay, **kwargs)


def make_directory(dir_path: str):
    try:
        os.makedirs(dir_path)
    except FileExistsError:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)


def remove_duplicates(urls: list) -> list:
    """Removes duplicate URL from the list, returns a list of unique links"""

    unique_urls = []
    for url in urls:
        if url not in unique_urls:
            unique_urls.append(url)

    return unique_urls


def save_images(urls: list, dir_path: str, prefix: str = "", number_images: bool = False):
    if not os.path.exists(dir_path):
        print(f"Error: Directory '{dir_path}' does not exist!")

    broken_url_counter = 0
    for i, url in enumerate(tqdm(urls)):
        image_name = prefix + str(url.split('/')[-1])

        if number_images:
            image_name = f"{i}_" + image_name

        path = os.path.join(dir_path, image_name)

        try:
            r = requests.get(url=url, allow_redirects=True, timeout=3.0)
            open(path, 'wb').write(r.content)
        except Exception as e:
            print(e)
            broken_url_counter += 1

    print(f"Saved images: {len(urls) - broken_url_counter}.\tUnsuccessful: {broken_url_counter}.\n")


def randomize_delay(delay: float) -> float:
    """Adds randomness to the delay. Returns the resulting number changed randomly by 15%."""
    return delay * random.uniform(0.85, 1.15)
