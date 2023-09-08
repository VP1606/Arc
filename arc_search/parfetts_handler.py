import sys
import os
import time
import cookie_jar, secret_jar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import user_manager.user_handler

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from parfetts.ean_search_sys import search_ean

def generate_parfetts_drivers():
    collection = {}
    users = user_manager.user_handler.fetch_users()
    for user in users:
        user_id = user[0]
        try:
            username, password = user_manager.user_handler.fetch_creds(type="bw", user_id=user_id)
            collection[user_id] = parfetts_login(username=username, password=password)
        except Exception as e:
            print(e)
            print("No BW Login available...")
            collection[user_id] = None

    return collection

def parfetts_login(username=secret_jar.parfetts_username, password=secret_jar.parfetts_password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://online.parfetts.co.uk/login?path=/")

    user_entry = driver.find_element(By.XPATH, cookie_jar.parfetts_user_entry_xpath)
    pass_entry = driver.find_element(By.XPATH, cookie_jar.parfetts_pass_entry_xpath)
    login_button = driver.find_element(By.XPATH, cookie_jar.parfetts_login_button_xpath)

    user_entry.send_keys(username)
    pass_entry.send_keys(password)
    login_button.click()

    _ = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
        By.CLASS_NAME, 'input-group'
    )))

    return driver

def parfetts_collector(ean: str, name: str, driver: webdriver.Chrome):
    # Status (OK, MULTIPLE, NOT_FOUND), name, rrp, ws_price, no_hits
    item_result_block = search_ean(ean=ean, driver=driver)

    if item_result_block[0] == "OK":
        ret_dict = {}

        ret_dict["item_name"] = item_result_block[1]
        ret_dict["ean"] = ean
        ret_dict["rsp"] = item_result_block[2]
        ret_dict["wholesale_price"] = item_result_block[3]
        ret_dict["wholesale_unit_size"] = item_result_block[4]
        ret_dict["supplier_code"] = item_result_block[5]

        return ret_dict
    else:
        ret_msg = cookie_jar.res_unavailable_message  
        ret_msg["no_search_hits"] = item_result_block[6]
        ret_msg["status"] = item_result_block[0]
        return ret_msg
