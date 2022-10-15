import os
import random
import shutil
import requests


def make_directory(dir_path: str):
    """Создаёт новую директорию. Если директория существует - перезаписывает."""
    try:
        os.makedirs(dir_path)
    except FileExistsError:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)


def remove_duplicates(urls: list) -> list:
    """Удаляет дублирующиеся URL-ссылки из списка, возвращает список уникальных ссылок"""

    unique_urls = []
    for url in urls:
        if url not in unique_urls:
            unique_urls.append(url)

    return unique_urls


def save_images(urls: list, dir_path: str, prefix: str = "", number_images: bool = False, timeout: float = 3.0):
    """
    Сохраняет изображения в заданную директорию

    **urls:** list
            Список URL-ссылок на изображения
    **dir_path:** str
            Путь, по которому будут сохранены изображения
    **prefix:** str
            Префикс к имени каждого изображения
    **number_images:** bool
            Если number_images = True, изображения будут пронумерованы перед сохранением
    **timeout:** float
            Время таймаута при сохранении изображения
    """

    broken_url_counter = 0
    for i, url in enumerate(urls):
        image_name = prefix + str(url.split('/')[-1])

        if number_images:
            image_name = f"{i}_" + image_name

        path = os.path.join(dir_path, image_name)

        try:
            r = requests.get(url=url, allow_redirects=True, timeout=timeout)
            open(path, 'wb').write(r.content)
        except Exception:
            broken_url_counter += 1

    print(f"Сохранено изображений: {len(urls) - broken_url_counter}.\tНеудачно: {broken_url_counter}.\n")


def randomize_delay(delay: float) -> float:
    """Добавляет рандома в задержку. Возвращает полученное число измененное случайным образом на 15%."""
    return delay * random.uniform(0.85, 1.15)
