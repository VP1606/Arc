from bs4 import BeautifulSoup
from booker_item import *
import requests


def GET_ITEM(link_code, cookies, headers, ean=""):
    url = "https://www.booker.co.uk{0}".format(link_code)
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    code = soup.find_all("h4", class_="product-id font-weight-bold mb-3")[0].text
    name = soup.find_all("h4", class_="d-inline pr-2 font-weight-bold")[0].text
    b_price = soup.find_all("p", class_="font-weight-bold mb-0 price")[0].text

    col4 = soup.find_all("div", class_="col-4")
    for index, el in enumerate(col4):
        if el["class"] != ['col-4']:
            col4.remove(el)

    col4 = col4[0]
    col4_elements = col4.find_all("p", class_="price-breakdown color-grey mb-0")

    rsp = ""
    por = ""
    vat_rate = ""

    for block in col4_elements:
        key = block.find_all("span", class_="font-weight-bold pr-2")[0].text
        val = block.find_all("span", class_="font-weight-bold")[1].text

        if key == "RRP:":
            rsp = val
        elif key == "POR:":
            por = val
        elif key == "VAT:":
            vat_rate = val
        else:
            print("Unknown Key in COL4!")

    fields = soup.find_all("span", class_="font-weight-bold")
    brand_name = ""
    for el in fields:
        if el.text == "Brand ":
            brand_holder = el.find_next_sibling()
            brand_name = brand_holder.text
            break

    parent_pack_supplier = soup.find_all("div", class_="col-4 pl-0")[0]
    unit_size = parent_pack_supplier.find_all("p", class_="font-weight-bold")[0].text
    unit_size = unit_size[11:]

    name = name.strip()

    item = BookerItem(name, b_price, rsp, por, code, vat_rate, brand_name, unit_size, ean)
    return item
