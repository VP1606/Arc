from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List
import re
import json

def tester():
    print("y")

class BasketItem:
    def __init__(self, name, product_code, pack_size, quantity, extension, instock) -> None:
        self.name = name
        self.quantity = int(quantity)
        self.ean = ''

        self.bw_product_code = product_code.replace('\n', '')
        self.bw_extension = extension
        self.bw_pack_size = pack_size
        self.bw_pack_qty = 0
        self.bw_instock = instock

        self.bw_unit_price = 0.0
        self.bw_total = 0.0

        self.bk_instock = None
        self.bk_product_code = ''
        self.bk_pack_size = ''
        self.bk_pack_qty = 0

        self.bk_unit_price = 0.0
        self.bk_total = 0.0

        self.pf_instock = None
        self.pf_product_code = ''
        self.pf_pack_size = ''
        self.pf_pack_qty = 0

        self.pf_unit_price = 0.0
        self.pf_total = 0.0

        self.form_bw_pack_qty()

        self.best_supplier = ''
        self.best_price = 0.0
        self.delta_to_bw = 0.0

    def form_bw_pack_qty(self):
        raw = self.bw_pack_size
        parts = raw.split('×', 1)

        result = parts[1].strip()
        if '\n' in result:
            result = result.split('\n', 1)[0]

        parts = result.split('×')
        cleaned_parts = [part.strip() for part in parts]

        total_qty = 1
        for part in cleaned_parts:
            total_qty = total_qty * int(part)
        
        self.bw_pack_qty = total_qty
        return total_qty
    
    def form_bk_pack_qty(self):
        input_string = self.bk_pack_size
        try:
            match = re.search(r'\d+', input_string)
            if match:
                number = int(match.group())
                self.bk_pack_qty = number
            else:
                self.bk_pack_qty = 1
        except:
            self.bk_pack_qty = 1
    
    def form_pf_pack_qty(self):
        raw = self.pf_pack_size
        parts = raw.split('x')
        cleaned_parts = [part.strip() for part in parts]

        total_qty = 1
        for part in cleaned_parts:
            total_qty = total_qty * int(part)

        self.pf_pack_qty = total_qty
        return total_qty
    
    def find_best_supplier(self):
        _best_sup = 'bestway'
        _best_price = self.bw_total
        
        if self.bk_instock:
            if self.bk_total < _best_price:
                _best_price = self.bk_total
                _best_sup = 'booker'
        
        if self.pf_instock:
            if self.pf_total < _best_price:
                _best_price = self.pf_total
                _best_sup = 'parfetts'
        
        self.best_price = _best_price
        self.best_supplier = _best_sup
        self.delta_to_bw = round((self.bw_total - _best_price), 2)

    def show_console(self):
        attributes = vars(self)
        print("------------------------")
        for attr, value in attributes.items():
            print(f"{attr}: {value}")
        print("------------------------")

    def to_dict(self):
        return self.__dict__

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