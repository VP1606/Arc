from PIL import Image
from pyzbar.pyzbar import decode
import pytesseract
from datetime import datetime

def extract_date(image: Image):
    cropped = image.crop((0, 80, 1000, 170))
    text = pytesseract.image_to_string(cropped)

    words = text.split(' ')
    date = ''
    for word in words:
        if '/' in word:
            date = word
            break
    
    day, month, year = map(int, date.split('/'))
    month_str = f'{month:02d}'
    day_str = f'{day:02d}'

    date_object = datetime.strptime(f'{day_str}/{month_str}/{str(year)}', '%d/%m/%y').date()
    return date_object

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

def text_processor(raw: str, ean: str):
    name = rrp = plof = size = _ean = ''

    lines = raw.splitlines()
    og_lines = lines.copy()
    name = lines[0] + lines[1]
    lines = lines[2:]
    remaining_lines = lines.copy()

    for line in lines:
        if '£' in line:
            rrp = line
            remaining_lines.remove(line)
        elif 'PLOF' in line:
            plof = line.replace('PLOF-', '')
            remaining_lines.remove(line)
        elif line == '':
            remaining_lines.remove(line)
        elif ean in line:
            remaining_lines.remove(line)
        else:
            pass
    
    # print("-->")
    # print(raw)
    # print(og_lines)
    # print(lines)
    # print(remaining_lines)
    # print("<--")

    for line in remaining_lines:
        if line.isdigit() is False:
            size = line
            break

    return (name, rrp, ean, plof, size)
