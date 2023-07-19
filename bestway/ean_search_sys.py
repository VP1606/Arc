from get_all_cat_threaded import *
from get_item import GET_ITEM

def search_ean(ean: str, cookies, headers, collect_pricing=True):
    url = "https://www.bestwaywholesale.co.uk/search?w={0}".format(ean)
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    main_list = soup.find("ul", {"id":"shop-products"})
    
    found = False
    found_item = None

    li_list = main_list.find_all("li", attrs={'data-ga-product-id': True})
    for li_el in li_list:
        code = li_el['data-ga-product-id']
        item = GET_ITEM(link_code=code, cookies=cookies, headers=headers, collect_pricing=collect_pricing)
        if item.ean == ean:
            found = True
            found_item = item
            break
    
    return (found, found_item)