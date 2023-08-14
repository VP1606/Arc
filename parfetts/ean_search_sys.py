from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_ean(ean: str, driver: webdriver.Chrome):
    search_bar = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[3]/div/div[2]/div/div[3]/div/div/div[1]/input')
    search_bar.send_keys(ean)

    enter_btn = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[3]/div/div[2]/div/div[3]/div/div/div[1]/div/button')
    enter_btn.click()

    main_list = WebDriverWait(driver, 3).until(EC.presence_of_element_located((
            By.CLASS_NAME, 'infinite-scroll-pagination'
    )))
    search_hits = main_list.find_elements(By.CLASS_NAME, 'product-card ')

    search_results = []
    for hit in search_hits:
        hit_res = search_div_parser(hit=hit)
        search_results.append(hit_res)
    
    if len(search_results) == 0:
        return ("NOT_FOUND", "", "", "", 0)
    elif len(search_results) > 1:
        return ("MULTIPLE", "", "", "", len(search_hits))
    elif len(search_results) == 1:
        res = search_results[0]
        return ("OK", res[0], res[1], res[2], len(search_hits))
    else:
        return ("UNKNOWN", "", "", "", 0)

def search_div_parser(hit):
    title_card = hit.find_element(By.CLASS_NAME, 'product-card--title')
    info_card = hit.find_element(By.CLASS_NAME, 'product-card--container')
    price_card = hit.find_element(By.CLASS_NAME, 'product-card--price')

    item_title = title_card.find_element(By.XPATH, '/html/body/div/div[2]/div[5]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/a/h5').text
    ws_price = price_card.find_element(By.XPATH, '/html/body/div/div[2]/div[5]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/div/span').text
    rrp_block = info_card.find_element(By.CLASS_NAME, 'product-card--vat-rrp')
    containers = rrp_block.find_elements(By.CLASS_NAME, 'sub-container')

    main_rrp = ''
    for container in containers:
        if 'RRP:' in container.text:
            main_rrp = container.text
            break
    main_rrp = main_rrp.replace('RRP: ', '')

    return (item_title, main_rrp, ws_price)
