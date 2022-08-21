import time
import json
import requests

from bs4 import BeautifulSoup
from fake_headers import Headers
from requests import PreparedRequest
from selenium import webdriver
from parameter_classes import Size, Orientation, ImageType, Color, Format

from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import WebDriverException


class Parser:
    def __init__(self):
        self.size = Size()
        self.orientation = Orientation()
        self.type = ImageType()
        self.color = Color()
        self.format = Format()

    def query_search(self,
                     query: str,
                     limit: int = 100,
                     delay: float = 5.0,
                     size: Size = None,
                     orientation: Orientation = None,
                     image_type: ImageType = None,
                     color: Color = None,
                     image_format: Format = None,
                     site: str = None) -> list:
        """
        Описание
        ---------
        Реализует функцию поиска по запросу в Яндекс Картинках.

        Параметры
        ---------
        **query:** str
                Текст запроса
        **limit:** int
                Требуемое (максимальное) количество изображений
        **delay:** float
                Время задержки между запросами (сек)
        **size:** Size
                Размер (большие, маленькие, средние)
        **orientation:** Orientation
                Ориентация (горизонтальная, вертикальная, квадрат)
        **image_type:** ImageType
                Тип искомых изображений (фото, лица, с белым фоном, ... )
        **color:** Color
                Цветовая гамма (ч/б, цветные, оранжевые, синие, ... )
        **image_format:** Format
                Формат изображений (jpg, png, gif)
        **site:** str
                Сайт, на котором расположены изображения

        Возвращаемое значение
        ---------
        list: Список URL-ссылок на изображения соответствующие запросу.
        """

        # Подготавливаем параметры запроса:
        params = {"text": query,
                  "isize": size,
                  "iorient": orientation,
                  "type": image_type,
                  "icolor": color,
                  "itype": image_format,
                  "site": site,
                  "nomisspell": 1,
                  "noreask": 1,
                  "p": 0}

        # Выполняем поиск и возвращаем результат:
        return self.__get_images(params=params, limit=limit, delay=delay)

    def image_search(self,
                     url: str,
                     limit: int = 100,
                     delay: float = 5.0,
                     size: Size = None,
                     orientation: Orientation = None,
                     color: Color = None,
                     image_format: Format = None,
                     site: str = None) -> list:
        """
        Описание
        ---------
        Реализует функцию поиска по изображению в Яндекс Картинках.

        Параметры
        ---------
        **url:** str
                URL-ссылка на изображение
        **limit:** int
                Требуемое (максимальное) количество изображений
        **delay:** float
                Время задержки между запросами (сек)
        **size:** Size
                Размер (большие, маленькие, средние)
        **orientation:** Orientation
                Ориентация (горизонтальная, вертикальная, квадрат)
        **color:** Color
                Цветовая гамма (ч/б, цветные, оранжевые, синие, ... )
        **image_format:** Format
                Формат изображений (jpg, png, gif, ... )
        **site:** str
                Сайт, на котором расположены изображения

        Возвращаемое значение
        ---------
        list: Список URL-ссылок на похожие изображения.
        """

        # Подготавливаем параметры запроса:
        params = {"url": url,
                  "isize": size,
                  "iorient": orientation,
                  "icolor": color,
                  "itype": image_format,
                  "site": site,
                  "rpt": "imageview",
                  "cbir_page": "similar",
                  "p": 0}

        # Выполняем поиск и возвращаем результат:
        return self.__get_images(params=params, limit=limit, delay=delay)

    def __get_images(self, params: dict, limit: int, delay: float) -> list:
        """
        Описание
        ---------
        Возвращает заданное количество прямых URL-ссылок на
        изображения, соответствующие параметрам запроса.

        Параметры
        ---------
        **params:** dict
                Параметры запроса
        **limit:** int
                Требуемое (максимальное) количество изображений
        **delay:** float
                Время задержки между запросами (сек)

        Возвращаемое значение
        ---------
        list: Список URL-ссылок на изображения.
        """

        request = self.__prepare_request(params)  # Подготавливаем запрос

        time.sleep(delay)  # Задержка перед запросом

        images = []
        while True:
            html = self.__get_html(request=request)  # Получаем html-код страницы с изображениями

            new_images = self.__parse_html(html)  # Вытаскиваем из html-кода прямые ссылки на изображения
            images += new_images

            print(f"Найдено изображений\t[\033[37m{len(images)} / {limit}\033[0m]")

            # Если изображения закончились, или мы достигли необходимого количества,
            if len(new_images) == 0 or len(images) >= limit:
                return images[:limit]  # возвращаем изображения.

            # Иначе, отправляем еще один запрос:
            else:
                params["p"] += 1  # Переходим к следующей странице
                request = self.__prepare_request(params)  # Подготавливаем новый запрос с учетом изменений
                time.sleep(delay)

    def __prepare_request(self, params: dict) -> PreparedRequest:
        """
        Описание
        ---------
        Подготавливает GET-запрос к Яндекс Картинкам с полученными параметрами
        и сгенерированными заголовками.

        Параметры
        ---------
        **params:** dict
                Параметры GET-запроса.

        Возвращаемое значение
        ---------
        PreparedRequest: Подготовленный GET-запрос.
        """

        params = {k: v for k, v in params.items() if v is not None}  # Удаляем все неиспользуемые параметры
        headers = Headers(headers=True).generate()  # Генерируем заголовки

        # Получаем подготовленный запрос (PreparedRequest)
        request = requests.Request(method="GET",
                                   url="https://yandex.ru/images/search",
                                   params=params,
                                   headers=headers).prepare()
        return request

    def __get_html(self, request: PreparedRequest) -> str:
        """
        Описание
        ---------
        Получает запрос, возвращает html-код страницы.

        Параметры
        ---------
        **request:** PreparedRequest
                Запрос

        Возвращаемое значение
        ---------
        str: html-код страницы.
        """

        try:
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            driver = webdriver.Firefox(executable_path="./geckodriver/geckodriver.exe", options=options)
        except SessionNotCreatedException as e:
            print(f"Ошибка: \033[91mSessionNotCreatedException.\033[0m Возможно, не установлен FireFox. \n\n{e.msg}")
            raise SystemExit(1)

        try:
            driver.get(request.url)
            html = driver.page_source

            return html
        except WebDriverException as e:
            print(f"Ошибка: \033[91mWebDriverException.\033[0m \n\n{e.msg}")
            raise SystemExit(1)
        finally:
            driver.close()
            driver.quit()

    def __parse_html(self, html: str) -> list:
        """
        Описание
        ---------
        Достаёт из html-кода страницы прямые ссылки на изображения.

        Параметры
        ---------
        **html:** str
                html-код страницы с изображениями.

        Возвращаемое значение
        ---------
        list: Список прямых URL-ссылок на изображения со страницы.
        """

        soup = BeautifulSoup(html, "lxml")
        pictures_place = soup.find("div", {"class": "serp-list"})

        urls = []
        try:
            pictures = pictures_place.find_all("div", {"class": "serp-item"})
        except AttributeError:
            print("Что-то пошло не так... Вы точно не робот?")
            return urls

        for pic in pictures:
            data = json.loads(pic.get("data-bem"))
            image = data['serp-item']['img_href']
            urls.append(image)

        return urls
