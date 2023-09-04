import pdf_sys.image_analyser as image_analyser
import pdf_sys.image_helper as image_helper
import pdf_sys.sql_uploader as sql_uploader

from pdf2image import convert_from_path
import time
import os

# V1 STATS ON M1 MAX :::

# Total Time Taken: 2.837
# Average Assumed TPI (14): 0.20263

# Total Time Taken: 5.296
# Average Assumed TPI (35): 0.15132

# Total Time Taken: 16.16
# Average Assumed TPI (119): 0.1358

path = os.path.join('../temp/collected.pdf')

class DataBlock:
    def __init__(self, _image) -> None:
        self.image = _image

        self.barcode = ''
        self.barcode_type = ''

        self.processor_result = None

def handle():
    pdf_images = convert_from_path(path)
    operating_date = None
    for _, image in enumerate(pdf_images):
        operating_date = image_analyser.extract_date(image=image)
        break
    
    book_images = list()
    for page_num, image in enumerate(pdf_images):
        book_images = book_images + image_helper.cut_items(image=image)
    
    main_list: list[DataBlock] = list()
    for image in book_images:
        needed = image_helper.check_if_occupied(image=image)
        if needed:
            main_list.append(DataBlock(_image=image))
    del book_images

    for num, block in enumerate(main_list):
        res = image_analyser.extract_barcodes(image=block.image)
        if res[0] is False:
            print(f"Error in Image {num + 1}!")
        else:
            block.barcode = res[1][0]
            block.barcode_type = res[1][1]
    
    start_time = time.time()
    for num, block in enumerate(main_list):
        text = image_analyser.extract_text_tesseract(image=block.image)
        print(f"Image N{num + 1}")
        print(f"EAN Sending: -->{block.barcode}<--")
        print("PROCESSOR::::")
        processor_res = image_analyser.text_processor(raw=text, ean=block.barcode)
        print(processor_res)
        block.processor_result = processor_res
        print("------")

    duration_tesseract = time.time() - start_time
    average_time = duration_tesseract / len(main_list)
    
    print("-------------------------")
    print(f"Average Tesseract Time Per Item: {round(average_time, 3)}")
    print("-------------------------")
    print("Uploading MySQL...")

    main_result = list()
    for block in main_list:
        main_result.append(block.processor_result)

    sql_uploader.upload_blocks(blocks=main_result, date=operating_date)
    print("DONE")
    return (True, len(main_list))


def handle_wrapper():
    start_time = time.time()
    res = None
    try:
        _res = handle()
        res = (_res[0], '', _res[1])
    except Exception as e:
        print("")
        print(f"Error Occured! ::: {str(e)}")
        res = (False, str(e), 1)

    end_time = time.time()
    print("-------------------------")
    print("-------------------------")
    print(f"Total Time Taken: {round((end_time - start_time), 3)}")
    print(f"Average Assumed TPI ({res[1]}): {round(((end_time - start_time) / res[2]), 5)}")
    print("-------------------------")
    print("-------------------------")
    return res

# handle_wrapper()
