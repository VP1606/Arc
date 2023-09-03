from pdf2image import convert_from_path
from PIL import Image

import image_helper

path = "test_35.pdf"

pdf_images = convert_from_path(path)

book_images = list()

for page_num, image in enumerate(pdf_images):
    print(f"Page {page_num + 1}:")
    book_images = book_images + image_helper.cut_items(image=image)

print(f"Original List: {len(book_images)}")

refined_book = list()
for image in book_images:
    needed = image_helper.check_if_occupied(image=image)
    if needed:
        refined_book.append(image)
    
del book_images

print(f"Refined List: {len(refined_book)}")