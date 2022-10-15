from utils import save_images
from utils import make_directory
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

# Сохраняем изображения:
output_dir = "./images/cat"

make_directory(dir_path=output_dir)  # Создаём директорию

save_images(square_cat, dir_path=output_dir, prefix="original_")  # Добавляем префикс к названиям
save_images(similar_cats, dir_path=output_dir, prefix="similar_", number_images=True)  # Добавляем префикс и нумерацию
