import time
import json
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm
from fake_headers import Headers
from requests import PreparedRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException


class Size:
    def __init__(self):
        self.large = "large"
        self.medium = "medium"
        self.small = "small"


class Orientation:
    def __init__(self):
        self.horizontal = "horizontal"
        self.vertical = "vertical"
        self.square = "square"


class ImageType:
    def __init__(self):
        self.photo = "photo"
        self.clipart = "clipart"
        self.lineart = "lineart"
        self.face = "face"
        self.demotivator = "demotivator"


class Color:
    def __init__(self):
        self.color = "color"
        self.gray = "gray"
        self.red = "red"
        self.orange = "orange"
        self.yellow = "yellow"
        self.cyan = "cyan"
        self.green = "green"
        self.blue = "blue"
        self.violet = "violet"
        self.white = "white"
        self.black = "black"


class Format:
    def __init__(self):
        self.jpg = "jpg"
        self.png = "png"
        self.gif = "gifan"


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
                     delay: float = 6.0,
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
                     delay: float = 6.0,
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

        # Запускаем веб-драйвер:
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')  # Запускать в фоновом режиме

            driver = webdriver.Firefox(executable_path="geckodriver/geckodriver.exe", options=options)
        except SessionNotCreatedException as e:
            print(f"Ошибка: \033[91mSessionNotCreatedException.\033[0m Возможно, не установлен FireFox. \n\n{e.msg}")
            raise SystemExit(1)

        # Выполняем подготовленный запрос:
        try:
            driver.get(request.url)
        except WebDriverException as e:
            print(f"Ошибка: \033[91mWebDriverException.\033[0m \n\n{e.msg}")
            raise SystemExit(1)

        pbar = tqdm(total=limit)
        while True:
            html = driver.page_source  # Получаем html-код страницы в виде строки
            images = self.__parse_html(html)  # Вытаскиваем из html-кода прямые ссылки на изображения

            # Проверяем, найдены ли изображения:
            if len(images) == 0:
                pbar.set_postfix_str("Что-то пошло не так... Найдено 0 изображений.")
                break

            pbar.n = len(images) if len(images) <= limit else limit
            pbar.refresh()

            # Если нашли достаточно изображений, выходим:
            if len(images) >= limit:
                break

            # Иначе, нажимаем на кнопку "Ещё картинки" и продолжаем:
            else:
                old_page_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(delay)
                new_page_height = driver.execute_script("return document.body.scrollHeight")

                if old_page_height == new_page_height:
                    try:
                        driver.find_element(
                            By.XPATH,
                            "//div [starts-with(@class, 'more')]//a[starts-with(@class, 'button2')]"
                        ).click()
                    except NoSuchElementException as e:
                        print(f"Ошибка: {e.msg}")
                        break
                    except ElementNotInteractableException:
                        pbar.set_postfix_str("Найдено меньше изображений")
                        break
                    except:
                        break

        driver.close()
        driver.quit()

        return images[:limit]

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

            for pic in pictures:
                data = json.loads(pic.get("data-bem"))
                image = data['serp-item']['img_href']
                urls.append(image)

            return urls
        except AttributeError:
            return urls
