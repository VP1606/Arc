from bs4 import BeautifulSoup
from bway_item import *
import requests


def GET_ITEM(link_code, cookies, headers, collect_pricing):
    url = 'https://www.bestwaywholesale.co.uk/product/{0}'.format(link_code)
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    right_block = soup.find(id="shop-products")

    name = right_block.find_all("h1", class_="prodname")[0].text
    unit_size = right_block.find_all("p", class_="prodsize")[0].text
    
    stock = 0

    b_price = "£0.00"
    if collect_pricing:
        try:
            b_price = right_block.find_all("p", class_="prodprice")[0].text
            stock = 1
        except:
            pass

    prod_table = right_block.find_all("table", class_="prodtable")[0]
    prod_table_rows = prod_table.find_all("tr")

    rsp, por, pack_size, code, ean, vat_rate, brand = "", "", "", "", "", "", ""

    for row in prod_table_rows:
        value = row.find_all("td")[0].text
        flag = row.find_all("th")[0].text
        if flag == "RSP:":
            rsp = value
        elif flag == "POR:":
            por = value
        elif flag == "Pack Size:":
            pack_size = value
        elif flag == "Product Code:":
            code = value
        elif flag == "Retail EAN:":
            ean = value
        elif flag == "Vat Rate:":
            vat_rate = value
        elif flag == "Brand:":
            brand = value
        else:
            tv = 0.0
            # print("Unexpected ROW PARSE FIELD!")
            # Error Handling? Unexpected Val Detected!

    item = BestwayItem(name, unit_size, b_price, rsp, por, pack_size, code, ean, vat_rate, brand, stock)
    return item
