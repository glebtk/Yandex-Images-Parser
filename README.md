# Yandex Images Parser
Реализует собой **простой парсер изображений с сервиса Яндекс.Картинки**.
Есть возможность поиска по текстовому запросу и по изображению.

При поиске можно задать параметры поиска, такие как:
- **размер**
- **ориентация** 
- **количество изображений**
- **тип** (фото, клипарт, ~~демотиватор~~ и т. д.)
- **цвет** (цветные, ч/б, красные, оранжевые и т. д.)
- **формат** (jpg, png, gif)
- **сайт**

Задержки между запросами автоматически рандомизируются в 
диапазоне +-15%.

Также, поскольку при поиске используется **Selenium**, в данном 
парсере отсутствует ограничение в 30 и 300 изображений.

**Требует установки браузера
[Mozilla Firefox](https://www.mozilla.org) !**


## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Примеры использования](#примеры-использования)
- [Источники](#источники)
- [Способы связи](#способы-связи)

---

## Технологии
- [Python 3.9](https://www.python.org)
- [Selenium](https://www.selenium.dev)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/)

## Начало работы
1. Клонируйте репозиторий:
```sh
$ git clone https://gitlab.com/gleb_tk/yandex_images_parser.git
```

2. Перед использованием необходимо установить зависимости проекта:
```sh
$ pip install -r requirements.txt
```

3. Убедитесь, что все зависимости успешно установлены.

4. Убедитесь, что установлен браузер
[Mozilla Firefox](https://www.mozilla.org).

5. Чтобы проверить работоспособность, можно запустить **example.py**.


## Примеры использования

Для начала создадим экземпляр класса парсера:

```python
from yandex_images_parser import Parser

parser = Parser()
```

### Поиск

1. Допустим, что мы хотим найти одно изображение кота.
Сделаем это!

```python
# Вызовем функцию "query_search" - поиск по запросу:
#   параметр "query" содержит текст запроса
#   параметр "limit" определяет требуемое количество изображений

one_cat = parser.query_search(query="cat", limit=1)

# Так как функция query_search возвращает список, вытащим нулевой элемент:
one_cat_url = one_cat[0]
```
Готово! Вот результат:

![Действительно кот](https://i.imgur.com/b8AZPgK.jpg)

2. Найдем 10 похожих изображений котов через функцию **image_search**:

```python
# Вызовем функцию "image_search" - поиск по картинке:
#   через параметр "url" передадим ссылку на найденное изображение
#   limit установим равным 10-ти

similar_cats = parser.image_search(url=one_cat_url, limit=10)
```
Результат поиска - список url на похожих котов:

![Еще коты](https://i.imgur.com/lZKuyKg.png)

3. Кроме параметра limit можно использовать такие параметры как:

- delay - время задержки между запросами (сек)
- size - размер изображений
- orientation - ориентация
- image_type - тип
- color - цвет
- image_format - формат (jpg, png, gif)
- site - сайт, на котором расположены изображения

Например, если необходимо найти 128 картин известных художников
в формате png, следует использовать вот этот код:

```python
paintings = parser.query_search(query="картины известных художников",
                                limit=128,
                                image_format=parser.format.png)
```

А этот код находит 30 черно-белых изображений лиц. Вертикальной ориентации,
среднего размера, в формате jpg.

```python
faces = parser.query_search(query="лицо",
                            limit=30,
                            size=parser.size.medium,
                            color=parser.color.gray,
                            image_type=parser.image_type.face,
                            image_format=parser.format.jpg,
                            orientation=parser.orientation.vertical)
```

### Очистка результатов
Иногда бывает так, что в процессе сложного поиска в результат могут попасть 
одинаковые изображения (имеющие одинаковый url). Для предварительного удаления 
таких url в **utils.py** есть специальная функция **remove_duplicates()**.

Импортируем её из utils:

```python
from utils import remove_duplicates
```

Удалим одинаковые url из списка paintings:
```python
paintings = remove_duplicates(paintings)
```

### Сохранение изображений
Импортируем функцию **save_images()** из utils:

```python
from utils import save_images
```

Передадим в функцию список url и путь, по которому мы хотим сохранить изображения:

```python
save_images(urls=paintings, dir_path="./images/paintings")
```

Готово!

## Источники
- [Похожий парсер на GitHub](https://github.com/Ulbwaa/YandexImagesParser)
- [Python Selenium Tutorials (плейлист, eng)](https://youtube.com/playlist?list=PLzMcBGfZo4-n40rB1XaJ0ak1bemvlqumQ)
- [Документация к Selenium (eng)](https://selenium-python.readthedocs.io)

## Способы связи
Если у вас есть предложения или пожелания, можно связаться со мной по 
почте или через телеграм:

[![Mail](https://i.imgur.com/HILZFT2.png)](mailto:tutikgv@gmail.com)
**E-mail:**
[tutikgv@gmail.com](mailto:tutikgv@gmail.com) <br>

[![Telegram](https://i.imgur.com/IMICyTA.png)](https://t.me/glebtutik)
**Telegram:**
https://t.me/glebtutik <br>
