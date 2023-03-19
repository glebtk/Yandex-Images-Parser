# Yandex Images Parser
This is a **simple parser for Yandex Images**. 
It allows searching by text query or image. 

When searching, you can specify parameters such as:
- **Size**
- **Orientation** 
- **Number of images**
- **Type** (photo, clipart, etc.)
- **Color** (colorful, b/w, red, orange, etc.)
- **Format** (jpg, png, gif)
- **Site**

Delays between requests are automatically randomized in a range of +-15%.

Since **Selenium** is used for searching, there is no limit of 30 
or 300 images in this parser.

**It requires installation of the
[Mozilla Firefox](https://www.mozilla.org) browser!**


## Contents
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
- [Sources](#sources)
- [Contact Information](#contact-information)

---

## Technologies
- [Python 3.9](https://www.python.org)
- [Selenium](https://www.selenium.dev)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/)

## Getting Started
1. Clone the repository:
```sh
$ git clone https://github.com/glebtk/yandex_images_parser.git
```

2. Before using, you need to install the project requirements:
```sh
$ pip install -r requirements.txt
```

3. Ensure that all requirements are successfully installed.

4. Ensure that [Mozilla Firefox](https://www.mozilla.org) is installed.

5. To test the functionality, you can run **example.py**.


## Usage Examples

Let's start by creating an instance of the parser class:

```python
from yandex_images_parser import Parser

parser = Parser()
```

### Search

1. Let's say we want to find one cat image. Let's do it!

```python
# Call the "query_search" function - search by query:
#   the "query" parameter contains the text query
#   the "limit" parameter defines the desired number of images

one_cat = parser.query_search(query="cat", limit=1)

# Since the query_search function returns a list, we will extract the zero-th element:
one_cat_url = one_cat[0]

```
Done! Cat is here:

![Really a cat](https://i.imgur.com/b8AZPgK.jpg)

2. Let's find 10 similar cat images using the **image_search** function:

```python
# Call the "image_search" function - search by image:
#   pass the link to the found image through the "url" parameter
#   set limit to 10

similar_cats = parser.image_search(url=one_cat_url, limit=10)

```
The search result is a list of url to similar cats:

![Еще коты](https://i.imgur.com/lZKuyKg.png)

3. In addition to the limit parameter, you can use parameters such as:

- delay - the delay time between requests (in seconds)
- size - the size of the images
- orientation - the orientation of the images
- image_type - the type of the images (photo, illustration, etc.)
- color - color
- image_format - the format of the images (jpg, png, gif)
- site -  the site where the images are located

For example, if you need to find 128 paintings of famous
painters in png format, use this code:

```python
paintings = parser.query_search(query="paintings of famous painters",
                                limit=128,
                                image_format=parser.format.png)

```

And this code finds 30 b/w face images, with a
vertical orientation, medium size, and jpg format.

```python
faces = parser.query_search(query="face",
                            limit=30,
                            size=parser.size.medium,
                            color=parser.color.gray,
                            image_type=parser.image_type.face,
                            image_format=parser.format.jpg,
                            orientation=parser.orientation.vertical)
```

### Cleaning Results
Sometimes, during a complex search, the results may
contain duplicate images (with the same URL).
To remove such URLs in advance, there is a special 
function called `remove_duplicates()` in **utils.py**.

Import it from utils:

```python
from utils import remove_duplicates
```

Remove duplicate URLs from the `paintings` list:
```python
paintings = remove_duplicates(paintings)
```

### Saving Images
Import the `save_images()` function from utils:

```python
from utils import save_images
```

We will pass to the function a list
of urls and the path by which we want to save the images:
```python
save_images(urls=paintings, dir_path="./images/paintings")
```

Done!

## Sources
- [A similar parser on GitHub](https://github.com/Ulbwaa/YandexImagesParser)
- [Python Selenium Tutorials](https://youtube.com/playlist?list=PLzMcBGfZo4-n40rB1XaJ0ak1bemvlqumQ)
- [Selenium documentation](https://selenium-python.readthedocs.io)

## Contact Information
If you have any suggestions or feedback, feel free to contact me by
email or via telegram!

[![Mail](https://i.imgur.com/HILZFT2.png)](mailto:tutikgv@gmail.com)
**E-mail:**
[tutikgv@gmail.com](mailto:tutikgv@gmail.com) <br>

[![Telegram](https://i.imgur.com/IMICyTA.png)](https://t.me/glebtutik)
**Telegram:**
https://t.me/glebtutik <br>
