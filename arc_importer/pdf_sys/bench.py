from pdf2image import convert_from_path
from PIL import Image
from pyzbar.pyzbar import decode
import time

import image_helper, image_analyser
import pytesseract

# export DYLD_LIBRARY_PATH=/opt/homebrew/lib
# Brew Installed: zbar, poppler, tesseract

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

# barcodes_found = list()
# for num, image in enumerate(refined_book):
#     res = image_analyser.extract_barcodes(image=image)
#     if res[0] is False:
#         print(f"Error in Image {num + 1}!")
#     else:
#         barcodes_found.append(res[1])

# for block in barcodes_found:
#     data, type = block[0], block[1]
#     print(data, type)

# print(f"Barcodes Found: {len(barcodes_found)}")

start_time = time.time()
for num, image in enumerate(refined_book):
    text = image_analyser.extract_text_tesseract(image=image)
    print(f"Image N{num + 1}")
    print(f"Text -->")
    print(text)
    print("------")

duration_tesseract = time.time() - start_time
average_time = duration_tesseract / len(refined_book)

print(f"Average Tesseract Time Per Item: {round(average_time, 3)}")