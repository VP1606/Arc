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


def sql_committing(item, cookies, headers, mydb):
    if item.rsp == '':
        pass
    else:
        item.commit_to_sql(mydb)


def build_item(link, cookies, headers):
    item_book = []
    item = get_item.GET_ITEM(link, cookies, headers)
    item_book.append(item)
    return item_book


def generate_ean_list(item):
    try:
        rsp = float(item.rsp[1:])
    except:
        rsp = 0.00
        pass

    pack = [item.ean, item.name, rsp]
    return pack


def do_cat_threaded(href, cookies, headers, mydb, generate_ean_list_called):
    target_urls = build_targets(href, cookies, headers)
    threads = []
    target_book = []
    item_book = []

    ean_list = []

    with alive_bar(len(target_urls), title="Page Scanning", force_tty=True) as bar:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for url in target_urls:
                threads.append(executor.submit(handle_page, url, cookies, headers))
            for task in as_completed(threads):
                target_book = target_book + task.result()
                bar()

    threads = []
    with alive_bar(len(target_book), title="Building Items", force_tty=True) as bar:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for link in target_book:
                threads.append(executor.submit(build_item, link, cookies, headers))
            for task in as_completed(threads):
                item_book = item_book + task.result()
                bar()

    if generate_ean_list_called:
        threads = []
        with alive_bar(len(item_book), title="Generating EAN List", force_tty=True) as bar:
            with ThreadPoolExecutor(max_workers=20) as executor:
                for item in item_book:
                    threads.append(executor.submit(generate_ean_list, item))
                for task in as_completed(threads):
                    ean_list.append(task.result())
                    bar()

    with alive_bar(len(target_book), title="Committing to SQL", force_tty=True) as bar:
        for el in item_book:
            sql_committing(el, cookies, headers, mydb)
            bar()

    return ean_list
