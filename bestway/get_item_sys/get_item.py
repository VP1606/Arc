import requests
from bs4 import BeautifulSoup
from bway_item import *

cookies = {
    'unbxd_depot': '834',
    'fulfilment_msg_shown': '1',
    'selected_fulfilment': 'C',
    'access_token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5iZXN0d2F5LmNvLnVrLyJ9..p-ip6AppEtaVzV6j.LVNbKkb9SD3I3sVrJupFFYA_8dhMjaX3Egx8V8W_InqVYrjoKxWajEjEfO0kkSdyRqRMiYxaT-RAyYoFRZgfVgKsuhQX3wz8OV7zS4-RbJ3-iOFXpVL0BWuAH6fOkOpGuGLzO3tEoml_T14FNuKJoWQp4sDQidUmeVxvOy4bAyefAKFXxOxOBTAZbgDnHBV97K9-unfqAV1QHN_AJ41ppWnC4EsORIVBqAzYhpenHeqF3ahA0HBOG89GCLNTDwN2h3Fn0d5mpPamZoaOz8kSlU62lkmsYDRh.jt-aS2jixJ5tkCRoxFWOHw',
    'PHPSESSID': 'db1m2j2jilirie1miah1fesptd',
    'auth0_check': 'Y',
    'SERVERID': 'web-02',
    'CookieControl': '{"necessaryCookies":["unbxd.visit","unbxd_depot","auth0_check","SERVERID"],"optionalCookies":{},"statement":{},"consentDate":1665689729577,"consentExpiry":365,"interactedWith":true,"user":"52D4A084-DB4A-45B0-9E3F-0C11F860557D"}',
    'sso_token_wholesale': '94z0ahoazps8gw0884wk848ww',
}

headers = {
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'unbxd_depot=834; fulfilment_msg_shown=1; selected_fulfilment=C; access_token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5iZXN0d2F5LmNvLnVrLyJ9..p-ip6AppEtaVzV6j.LVNbKkb9SD3I3sVrJupFFYA_8dhMjaX3Egx8V8W_InqVYrjoKxWajEjEfO0kkSdyRqRMiYxaT-RAyYoFRZgfVgKsuhQX3wz8OV7zS4-RbJ3-iOFXpVL0BWuAH6fOkOpGuGLzO3tEoml_T14FNuKJoWQp4sDQidUmeVxvOy4bAyefAKFXxOxOBTAZbgDnHBV97K9-unfqAV1QHN_AJ41ppWnC4EsORIVBqAzYhpenHeqF3ahA0HBOG89GCLNTDwN2h3Fn0d5mpPamZoaOz8kSlU62lkmsYDRh.jt-aS2jixJ5tkCRoxFWOHw; PHPSESSID=db1m2j2jilirie1miah1fesptd; auth0_check=Y; SERVERID=web-02; CookieControl={"necessaryCookies":["unbxd.visit","unbxd_depot","auth0_check","SERVERID"],"optionalCookies":{},"statement":{},"consentDate":1665689729577,"consentExpiry":365,"interactedWith":true,"user":"52D4A084-DB4A-45B0-9E3F-0C11F860557D"}; sso_token_wholesale=94z0ahoazps8gw0884wk848ww',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.bestwaywholesale.co.uk',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Referer': 'https://www.bestwaywholesale.co.uk/search?w=comfort%20sunshiny&go=Search',
    'Connection': 'keep-alive',
}

page = requests.get('https://www.bestwaywholesale.co.uk/product/656016-1', cookies=cookies, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
right_block = soup.find(id="shop-products")

name = right_block.find_all("h1", class_="prodname")[0].text
unit_size = right_block.find_all("p", class_="prodsize")[0].text
b_price = right_block.find_all("p", class_="prodprice")[0].text

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
        print("Unexpected ROW PARSE FIELD!")
        # Error Handling? Unexpected Val Detected!

item = BestwayItem(name, unit_size, b_price, rsp, por, pack_size, code, ean, vat_rate, brand)

