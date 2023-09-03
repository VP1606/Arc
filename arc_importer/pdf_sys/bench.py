from pdf2image import convert_from_path
from PIL import Image
from pyzbar.pyzbar import decode

import image_helper

# export DYLD_LIBRARY_PATH=/opt/homebrew/lib
# Brew Installed: zbar, poppler

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

barcodes_found = list()
for image in refined_book:
    barcodes = decode(image)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type

        block = [barcode_data, barcode_type]
        barcodes_found.append(block)
        del block

print(f"Barcodes Found: {len(barcodes_found)}")

for block in barcodes_found:
    data, type = block[0], block[1]
    print(data, type)