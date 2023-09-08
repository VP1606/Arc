import sys
import os
import cookie_jar, secret_jar
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# class BestwayItem(
#     name: Any,
#     unit_size: Any,
#     b_price: Any | str,
#     rsp: Any | str,
#     por: Any | str,
#     pack_size: Any | str,
#     code: Any | str,
#     ean: Any | str,
#     vat_rate: Any | str

def bestway_login(account_number=secret_jar.bestway_acc_num, password=secret_jar.bestway_acc_pass):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.bestwaywholesale.co.uk/login-auth")

    _ = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
        By.ID, 'account_number'
    )))

    time.sleep(1)
    try:
        cookie_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="ccc-notify-accept"]'
        )))

        cookie_button.click()
        print("Cookie Button!")

    except TimeoutException:
        print("No Cookie Button!")

    account_num_entry = driver.find_element(By.XPATH, cookie_jar.bestway_account_numer_entry_xpath)
    acc_enter_button = driver.find_element(By.XPATH, cookie_jar.bestway_acc_next_button)

    account_num_entry.send_keys(account_number)
    acc_enter_button.click()
    
    _ = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
        By.ID, 'btn-login'
    )))

    acc_password_entry = driver.find_element(By.XPATH, cookie_jar.bestway_acc_password_xpath)
    acc_login_button = driver.find_element(By.XPATH, cookie_jar.bestway_login_button_xpath)

    acc_password_entry.send_keys(password)
    acc_login_button.click()
    
    _ = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
        By.ID, 'main'
    )))

    return driver

def build_item(product_code):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(os.path.join(parent_dir, 'bestway'))
    from get_item import GET_ITEM

    item = GET_ITEM(product_code, cookies=cookie_jar.bestway_cookies, headers=cookie_jar.bestway_headers, collect_pricing=True)
    return item

def bestway_collector(ean: str, driver: webdriver.Chrome):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(os.path.join(parent_dir, 'bestway'))
    from ean_search_sys import search_ean_selenium

    search_res = search_ean_selenium(ean=ean, cookies=cookie_jar.bestway_cookies, headers=cookie_jar.bestway_headers, driver=driver)

    if search_res[0] is True:
        item = search_res[1]
        ret_dict = {}

        ret_dict["item_name"] = item.name
        ret_dict["ean"] = item.ean
        ret_dict["supplier_code"] = item.code
        ret_dict["rsp"] = item.rsp
        ret_dict["wholesale_unit_size"] = item.unit_size
        ret_dict["wholesale_price"] = item.b_price

        return ret_dict

    else:
        return cookie_jar.res_unavailable_message