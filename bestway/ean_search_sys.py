from get_all_cat_threaded import *
from get_item import GET_ITEM, GET_ITEM_selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def search_ean(ean: str, cookies, headers, collect_pricing=True):
    url = "https://www.bestwaywholesale.co.uk/search?w={0}".format(ean)
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    main_list = soup.find("ul", {"id":"shop-products"})
    
    found = False
    found_item = None

    li_list = main_list.find_all("li", attrs={'data-ga-product-id': True})
    for li_el in li_list:
        code = li_el['data-ga-product-id']
        item = GET_ITEM(link_code=code, cookies=cookies, headers=headers, collect_pricing=collect_pricing)
        if item.ean == ean:
            found = True
            found_item = item
            break
    
    return (found, found_item)

def search_ean_selenium(ean: str, cookies, headers, driver: webdriver.Chrome):
    print("HI")
    stime = time.time()

    url = "https://www.bestwaywholesale.co.uk/search?w={0}".format(ean)
    driver.get(url)
    
    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((
        By.CLASS_NAME, 'shop-products-column'
    )))

    try:
        collect_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="fulf-select-C"]'
        )))

        print("Collect Button!")
        collect_button.click()

    except TimeoutException:
        print("No Collect Button!")

    try:
        collect_xmark = WebDriverWait(driver, 1).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="ccmin-modal"]/button'
        )))

        print("Collect X Mark")
        collect_xmark.click()

    except TimeoutException:
        print("No Collect XMark!")

    driver.get(url)
    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((
        By.CLASS_NAME, 'shop-products-column'
    )))

    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")
    main_list = soup.find("ul", {"id":"shop-products"})
    
    found = False
    found_item = None

    li_list = main_list.find_all("li", attrs={'data-ga-product-id': True})
    for li_el in li_list:
        code = li_el['data-ga-product-id']
        item = GET_ITEM_selenium(link_code=code, driver=driver, collect_pricing=True)
        if item.ean == ean:
            found = True
            found_item = item
            break
    
    ftime = time.time()
    print("HH ::: {0}".format(ftime - stime))

    return (found, found_item)