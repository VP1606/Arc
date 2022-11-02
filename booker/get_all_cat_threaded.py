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

    targets = [url]

    try:
        pagination = soup.find_all("ul", class_="pagination")[0]
        page_box = pagination.find_all("li", class_="page-item d-flex").pop()
        final_box = page_box.find_all("a", class_="page-link font-weight-bold")[0]
        max_index = int(final_box.text)

        link_stem = final_box["href"][:-1]

        for i in range(1, max_index):
            link = "https://www.booker.co.uk{0}{1}".format(link_stem, str(i))
            targets.append(link)

    except:
        pass

    return targets


def sql_committing(item, cookies, headers, mydb):
    if item.rsp == '':
        pass
    else:
        try:
            item.commit_to_sql(mydb)
        except:
            print("SQL ERROR!")
            print("{0} {1} {2}".format(item.name, item.rsp, item.vat_rate))


def build_item(link, cookies, headers):
    item_book = []
    item = get_item.GET_ITEM(link, cookies, headers)
    item_book.append(item)
    return item_book


def do_cat_threaded(href, cookies, headers, mydb):
    target_urls = build_targets(href, cookies, headers)
    threads = []
    target_book = []
    item_book = []

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

    with alive_bar(len(target_book), title="Committing to SQL", force_tty=True) as bar:
        for el in item_book:
            sql_committing(el, cookies, headers, mydb)
            bar()
