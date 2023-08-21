from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List

def tester():
    print("y")

class BasketItem:
    def __init__(self, name, product_code, pack_size, quantity, extension, instock) -> None:
        self.name = name
        self.quantity = int(quantity)
        self.ean = ''

        self.bw_product_code = product_code
        self.bw_extension = extension
        self.bw_pack_size = pack_size
        self.bw_instock = instock

        self.bw_unit_price = 0.0
        self.bw_total = 0.0

        self.bk_instock = None
        self.bk_product_code = ''
        self.bk_pack_size = ''

        self.bk_unit_price = 0.0
        self.bk_total = 0.0

        self.pf_instock = None
        self.pf_product_code = ''
        self.pf_pack_size = ''

        self.pf_unit_price = 0.0
        self.pf_total = 0.0

    def show_console(self):
        attributes = vars(self)
        print("------------------------")
        for attr, value in attributes.items():
            print(f"{attr}: {value}")
        print("------------------------")

def get_basket(driver: webdriver.Chrome):
    print("----------------")
    url = "https://www.bestwaywholesale.co.uk/trolley"
    driver.get(url)

    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((
        By.ID, 'fulltrolley'
    )))

    item_table = driver.find_element(By.ID, 'fulltrolley').find_element(By.TAG_NAME, 'tbody')
    rows = item_table.find_elements(By.XPATH, ".//tr[not(@*)]")

    items: List[BasketItem] = []

    for _, row in enumerate(rows):

        name_block = row.find_element(By.CLASS_NAME, 'trol-name')

        name_a = name = name_block.find_element(By.TAG_NAME, 'a')
        name = name_a.text
        extension = name_a.get_attribute('href')

        code_details = name_block.text.split(" • ")
        product_code = code_details[0].replace(name, '')
        pack_size = code_details[1]

        quantity = row.find_element(By.TAG_NAME, 'input').get_attribute('value')

        instock = True
        outstock_elements = row.find_elements(By.CSS_SELECTOR, '.outstock')
        if outstock_elements:
            instock = False
        else:
            instock = True

        item = BasketItem(name, product_code, pack_size, quantity, extension, instock)
        items.append(item)

    return items