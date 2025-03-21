import os
import sys
import glob
import time
import json
import urllib
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_headers import Headers
from requests import PreparedRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
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
    def __init__(self, headless=True, firefox_profile_path=None):

        if not firefox_profile_path:
            firefox_profile_path = self.__find_firefox_profile()

        self.size = Size()
        self.orientation = Orientation()
        self.type = ImageType()
        self.color = Color()
        self.format = Format()
        self.headless = headless
        self.profile_path = firefox_profile_path

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

            if self.headless:
                options.add_argument('--headless')

            if sys.platform.startswith('win'):
                geckodriver_path = "geckodriver/geckodriver.exe"
                service = Service(executable_path=geckodriver_path)
                driver = webdriver.Firefox(service=service, options=options)

            elif sys.platform.startswith('linux'):
                options.add_argument(f"--profile={self.profile_path}")

                geckodriver_paths = [
                    "/usr/bin/geckodriver",
                    "/usr/local/bin/geckodriver",
                    "/snap/bin/geckodriver",
                ]

                driver = None
                for geckodriver_path in geckodriver_paths:
                    try:
                        service = Service(executable_path=geckodriver_path)
                        driver = webdriver.Firefox(service=service, options=options)
                        break  # Если успешно запустили, выходим из цикла
                    except WebDriverException:
                        continue  # Пробуем следующий путь

                if driver is None:
                    raise WebDriverException(
                        "Could not find a valid geckodriver path. Install geckodriver or provide the correct path.")

            else:
                raise NotImplementedError("Your exotic operating system is not supported")

        except SessionNotCreatedException as e:
            print(f"Error: \033[91mSessionNotCreatedException.\033[0m FireFox may not be installed. \n\n{e.msg}")
            raise SystemExit(1)

        try:
            driver.get(request.url)
        except WebDriverException as e:
            print(f"Error: \033[91mWebDriverException.\033[0m \n\n{e.msg}")
            raise SystemExit(1)

        time.sleep(delay)
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
                        driver.find_element(By.XPATH, "//div[starts-with(@class, 'FetchListButton')]//button[starts-with(@class, 'Button2')]").click()
                    except NoSuchElementException as e:
                        print(f"Error: {e.msg}")
                        break
                    except ElementNotInteractableException:
                        pbar.set_postfix_str("Fewer images found")
                        break
                    except Exception as e:
                        print(e)

        driver.close()
        driver.quit()

        return images[:limit]

    def __find_firefox_profile(self):
        profile_paths = [
            "~/snap/firefox/common/.mozilla/firefox/*.default*",
            "~/.mozilla/firefox/*.default*",
            "~/.var/app/org.mozilla.firefox/.mozilla/firefox/*.default*"
        ]

        for path in profile_paths:
            full_path = os.path.expanduser(path)
            profiles = glob.glob(full_path)
            if profiles:
                return profiles[0]

        return "Profile not found"

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
        pictures_place = soup.find("div", {"class": "SerpList"})

        if pictures_place is not None:
            urls = []
            try:
                pictures = pictures_place.find_all("div", {"class": "SerpItem"})

                for pic in pictures:
                    url_soup = BeautifulSoup(str(pic), 'html.parser')
                    image_url = url_soup.find('a', class_='Link ImagesContentImage-Cover')['href']
                    image_url = urllib.parse.parse_qs(urllib.parse.urlparse(image_url).query)['img_url'][0]

                    urls.append(image_url)

                return urls
            except AttributeError:
                return urls

        else:
            pictures_place = soup.find("div", {"class": "cbir-page-layout__main-content"})
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
