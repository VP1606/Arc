import requests
from bs4 import BeautifulSoup
import get_item
from alive_progress import alive_bar
import math
from concurrent.futures import ThreadPoolExecutor, as_completed


def handle_page(url, cookies, headers):
    local_book = []

    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    the_list = soup.find(id="shop-products")
    list_elements = the_list.find_all("li")

    for el in list_elements:
        try:
            local_book.append(el["data-ga-product-id"])
        except:
            pass

    return local_book


def build_targets(href, cookies, headers):
    url = 'https://www.bestwaywholesale.co.uk/{0}'.format(href)
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    max_span_text = soup.find_all("span", class_="desktop")[0].text
    max_val = int(max_span_text.split(" ").pop())
    max_pages = math.ceil(max_val / 20)
    max_increment = (max_pages * 20)

    targets = [url]

    for i in range(20, max_increment, 20):
        new_url = 'https://www.bestwaywholesale.co.uk/{0}?s={1}'.format(href, str(i))
        targets.append(new_url)

    return targets


def do_cat_threaded(href, cookies, headers, mydb):
    target_urls = build_targets(href, cookies, headers)
    threads = []
    target_book = []

    with alive_bar(len(target_urls), title="Page Scanning", force_tty=True) as bar:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for url in target_urls:
                threads.append(executor.submit(handle_page, url, cookies, headers))
            for task in as_completed(threads):
                target_book = target_book + task.result()
                bar()