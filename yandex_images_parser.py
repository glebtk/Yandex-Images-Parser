import time
import json
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm
from fake_headers import Headers
from requests import PreparedRequest
from selenium import webdriver
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
        Description
        ---------
        Implements the search function by query in Yandex Images.

        Args
        ---------
        **query:** str
                Query text
        **limit:** int
                Required (maximum) number of images
        **delay:** float
                Delay time between requests (sec)
        **size:** Size
                Size (large, small, medium)
        **orientation:** Orientation
                Orientation (horizontal, vertical, square)
        **image_type:** ImageType
                The type of images you are looking for (photos, faces, cliparts, ... )
        **color:** Color
                Color scheme (b/w, colored, orange, blue, ... )
        **image_format:** Format
                Format (jpg, png, gif)
        **site:** str
                The site where the images are located

        Return value
        ---------
        list: A list of URL to images matching the query.
        """



        # Preparing the request parameters:
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

        # Perform a search and return the result:
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
        Description
        ---------
        Implements a function for searching for similar images in Yandex Images.

        Параметры
        ---------
        **url:** str
                URL of the image
        **limit:** int
                Required (maximum) number of images
        **delay:** float
                Delay time between requests (sec)
        **size:** Size
                Size (large, small, medium)
        **orientation:** Orientation
                Orientation (horizontal, vertical, square)
        **color:** Color
                Color scheme (b/w, colored, orange, blue, ... )
        **image_format:** Format
                Format (jpg, png, gif)
        **site:** str
                The site where the images are located

        Return value
        ---------
        list: A list of URL to similar images.
        """

        # Preparing the request parameters:
        params = {"url": url,
                  "isize": size,
                  "iorient": orientation,
                  "icolor": color,
                  "itype": image_format,
                  "site": site,
                  "rpt": "imageview",
                  "cbir_page": "similar",
                  "p": 0}

        # Perform a search and return the result:
        return self.__get_images(params=params, limit=limit, delay=delay)

    def __get_images(self, params: dict, limit: int, delay: float) -> list:
        """
        Description
        ---------
        Returns the specified number of direct URL to
        images corresponding to the request parameters.

        Parameters
        ---------
        **params:** dict
                Request parameters
        **limit:** int
                Required (maximum) number of images
        **delay:** float
                Delay time between requests (sec)

        Return value
        ---------
        list: A list of URL to images.
        """

        request = self.__prepare_request(params)  # Prepare request

        try:
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            driver = webdriver.Firefox(executable_path="geckodriver/geckodriver.exe", options=options)
        except SessionNotCreatedException as e:
            print(f"Ошибка: \033[91mSessionNotCreatedException.\033[0m FireFox may not be installed. \n\n{e.msg}")
            raise SystemExit(1)

        try:
            driver.get(request.url)
        except WebDriverException as e:
            print(f"Error: \033[91mWebDriverException.\033[0m \n\n{e.msg}")
            raise SystemExit(1)

        pbar = tqdm(total=limit)
        while True:
            html = driver.page_source
            images = self.__parse_html(html)  # Direct links extracting from the html code

            if len(images) == 0:
                pbar.set_postfix_str("Something went wrong... no images found.")
                break

            pbar.n = len(images) if len(images) <= limit else limit
            pbar.refresh()

            if len(images) >= limit:
                break
            else:
                old_page_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(delay)
                new_page_height = driver.execute_script("return document.body.scrollHeight")

                if old_page_height == new_page_height:
                    try:
                        driver.find_element_by_xpath(
                            "//div [starts-with(@class, 'more')]//a[starts-with(@class, 'button2')]"
                        ).click()
                    except NoSuchElementException as e:
                        print(f"Ошибка: {e.msg}")
                        break
                    except ElementNotInteractableException:
                        pbar.set_postfix_str("Fewer images found")
                        break
                    except:
                        break

        driver.close()
        driver.quit()

        return images[:limit]

    def __prepare_request(self, params: dict) -> PreparedRequest:
        """
        Description
        ---------
        Prepares a GET request to Yandex Images with the received parameters
        and generated headers.

        Args
        ---------
        **params:** dict
                GET-request parameters.

        Return values
        ---------
        PreparedRequest: Prepared GET-request.
        """

        params = {k: v for k, v in params.items() if v is not None}  # Deleting all unused parameters
        headers = Headers(headers=True).generate()  # Generating headers

        # Receive a prepared request (Prepared Request)
        request = requests.Request(method="GET",
                                   url="https://yandex.ru/images/search",
                                   params=params,
                                   headers=headers).prepare()
        return request

    def __parse_html(self, html: str) -> list:
        """
        Description
        ---------
        Extracts direct links to images from the html code of the page.

        Args
        ---------
        **html:** str
                html code of the page with images.

        Return value
        ---------
        list: A list of direct URL to images from the page.
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
