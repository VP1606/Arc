import requests
from bs4 import BeautifulSoup
import get_item
from alive_progress import alive_bar
import math

def Upload_Category(href, cookies, headers, mydb):
    target_book = []

    url = 'https://www.bestwaywholesale.co.uk/{0}'.format(href)
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    max_span_text = soup.find_all("span", class_="desktop")[0].text
    max_val = int(max_span_text.split(" ").pop())
    max_pages = math.ceil(max_val / 20)

    incrament_count = 0
    nextable_flag = True

    with alive_bar(max_pages, title="Page Scanning", force_tty=True) as bar:
        while nextable_flag:
            extension = ""
            if incrament_count != 0:
                extension = "?s={0}".format(str(incrament_count))

            url = 'https://www.bestwaywholesale.co.uk/{0}{1}'.format(href, extension)
            page = requests.get(url, cookies=cookies, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")

            the_list = soup.find(id="shop-products")
            list_elements = the_list.find_all("li")
            valids = 0
            for el in list_elements:
                try:
                    target_book.append(el["data-ga-product-id"])
                    valids += 1
                except:
                    pass

            if valids < 20:
                nextable_flag = False
            else:
                incrament_count += 20

            bar()

    print(len(target_book))

    # for target_link in target_book:
    #     item = get_item.GET_ITEM(target_link, cookies, headers)
    #     item.commit_to_sql(mydb)