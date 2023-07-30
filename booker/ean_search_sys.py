import requests
from bs4 import BeautifulSoup

def search_ean(ean: str, name: str, cookies, headers):
    url = "https://www.booker.co.uk/products/search?keywords={0}".format(ean)
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    main_group = soup.find_all("div", class_="p-0 p-sm-0 product-list rowUnGrouped")[0]
    search_hits = main_group.findChildren("div", recursive=False)
    
    search_results = []
    for hit in search_hits:
        hit_res = search_div_row_parser(hit=hit)
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
    
def search_div_row_parser(hit):
    _title = hit.find_all("p", class_="product-name font-weight-bold mb-0")[0]
    item_title = _title.text.strip()

    main_rrp = ""
    rrp_possibles = hit.find_all("div", class_="price-row")
    for possible in rrp_possibles:
        span = possible.findChildren("span", recursive=False)[0]
        if "RRP: " in span.text:
            main_rrp = span.text
            break

    ws_price = ""
    price_block = hit.find_all("div", class_="price")[0]
    price_holder = price_block.find_all("p", class_="font-weight-bold mb-0")[0]
    ws_price = price_holder.text

    return (item_title, main_rrp, ws_price)