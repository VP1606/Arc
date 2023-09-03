from PIL import Image
from pyzbar.pyzbar import decode
import pytesseract

def extract_barcodes(image: Image):
    barcodes = decode(image)
    if len(barcodes) == 1:
        barcode = barcodes[0]
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        block = [barcode_data, barcode_type]

        return (True, block)

    else:
        print("Unexpectedly found more than 1 barcode! Skipping...")
        return (False, [])

def extract_text_tesseract(image: Image):
    text = pytesseract.image_to_string(image)
    return text