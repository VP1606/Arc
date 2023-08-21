from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def tester():
    print("y")

class BasketItem:
    def __init__(self, name, product_code, pack_size, quantity) -> None:
        self.name = name
        self.loc_product_code = product_code
        self.pack_size = pack_size
        self.quantity = quantity

    def show_console(self):
        print(self.name, self.loc_product_code, self.pack_size, self.quantity)

def get_basket(driver: webdriver.Chrome):
    print("----------------")
    url = "https://www.bestwaywholesale.co.uk/trolley"
    driver.get(url)

    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((
        By.ID, 'fulltrolley'
    )))

    item_table = driver.find_element(By.ID, 'fulltrolley').find_element(By.TAG_NAME, 'tbody')
    rows = item_table.find_elements(By.XPATH, ".//tr[not(@*)]")

    items = []

    for _, row in enumerate(rows):

        name_block = row.find_element(By.CLASS_NAME, 'trol-name')
        name = name_block.find_element(By.TAG_NAME, 'a').text
        code_details = name_block.text.split(" • ")
        product_code = code_details[0].replace(name, '')
        pack_size = code_details[1]

        quantity = row.find_element(By.TAG_NAME, 'input').get_attribute('value')

        item = BasketItem(name, product_code, pack_size, quantity)
        items.append(item)

    for item in items:
        item.show_console()