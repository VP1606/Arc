import requests
from bs4 import BeautifulSoup
import get_item
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed


def handle_page(url, cookies, headers):
    local_book = []
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    main = soup.find_all("main", class_="list inner-list pb-md-2 px-0")[0]
    row = main.find_all("div", class_="rowMode")[0]

    coll = row.find_all("p", class_="product-name font-weight-bold mb-0")
    for el in coll:
        link = el["onclick"]
        link = link[33:]
        link = link[:-1]

        local_book.append(link)

    return local_book


def build_targets(href, cookies, headers):
    url = "https://www.booker.co.uk{0}".format(href)
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    pagination = soup.find_all("ul", class_="pagination")[0]
    page_box = pagination.find_all("li", class_="page-item d-flex").pop()
    final_box = page_box.find_all("a", class_="page-link font-weight-bold")[0]
    max_index = int(final_box.text)

    link_stem = final_box["href"][:-1]

    targets = [url]
    for i in range(1, max_index):
        link = "https://www.booker.co.uk{0}{1}".format(link_stem, str(i))
        targets.append(link)

    return targets


def sql_committing(el, cookies, headers, mydb):
    item = get_item.GET_ITEM(el, cookies, headers)
    if item.rsp == '':
        pass
    else:
        item.commit_to_sql(mydb)


def do_cat_threaded(href, cookies, headers, mydb):
    target_urls = build_targets(href, cookies, headers)
    threads = []
    sql_threads = []
    target_book = []

    with alive_bar(len(target_urls), title="Page Scanning", force_tty=True) as bar:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for url in target_urls:
                threads.append(executor.submit(handle_page, url, cookies, headers))
            for task in as_completed(threads):
                target_book = target_book + task.result()
                bar()

    with alive_bar(len(target_book), title="Committing to SQL", force_tty=True) as bar:
        for el in target_book:
            sql_committing(el, cookies, headers, mydb)
            bar()
