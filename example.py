from yandex_images_parser import Parser

parser = Parser()

# Находим картинку с котом. Квадратную, среднего размера:
square_cat = parser.query_search(query="cat",
                                 limit=1,
                                 size=parser.size.medium,
                                 orientation=parser.orientation.square)

# Поскольку метод query_search возвращает список, выбираем нулевой элемент:
square_cat_url = square_cat[0]

# Находим картинки с похожими котами:
similar_cats = parser.image_search(url=square_cat_url,
                                   limit=10)

# Выводим результат работы:
print(f"Кот:\n{square_cat_url}\n")

print("Похожие коты:")
for cat in similar_cats:
    print(cat)


