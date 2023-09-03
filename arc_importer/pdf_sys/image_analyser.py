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
            remaining_lines.remove(ean)
        else:
            pass
    
    print(og_lines)
    print(lines)
    print(remaining_lines)

    for line in remaining_lines:
        if line.isdigit() is False:
            size = line
            break

    return (name, rrp, ean, plof, size)
