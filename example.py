from utils import save_images, make_directory
from yandex_images_parser import Parser

parser = Parser(headless=False)

# Find a square, medium-sized image of a cat:
square_cat = parser.query_search(query="cat",
                                 limit=1,
                                 size=parser.size.medium,
                                 orientation=parser.orientation.square)

# Since the query_search method returns a list, we select the first element:
square_cat_url = square_cat[0]

# Find images of similar cats:
similar_cats = parser.image_search(url=square_cat_url,
                                   limit=10)

# Display the results:
print(f"Cat:\n{square_cat_url}\n")

print("Similar cats:")
for cat in similar_cats:
    print(cat)

# Save the images:
output_dir = "./images/cats"
make_directory(output_dir)

save_images(square_cat, dir_path=output_dir, prefix="original_")  # Add prefix to filenames
save_images(similar_cats, dir_path=output_dir, prefix="similar_", number_images=True)  # Add prefix and numbering
