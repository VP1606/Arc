import sys
import os
import json
import cookie_jar

# class BookerItem:
#     def __init__(self, name, b_price, rsp, por, code, vat_rate, brand_name, unit_size, ean):
#         self.name = name
#         self.b_price = b_price
#         self.rsp = rsp
#         self.por = por
#         self.code = code
#         self.vat_rate = vat_rate
#         self.brand = brand_name
#         self.unit_size = unit_size
#         self.ean = ean

def build_item(link_code: str, cookies, headers, ean: str):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(parent_dir)
    from booker.get_item import GET_ITEM as BOOKER_GET_ITEM

    item = BOOKER_GET_ITEM(link_code=link_code, cookies=cookies, headers=headers, ean=ean)
    return item

def do_ean_search(ean: str, item_name: str):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(os.path.join(parent_dir, 'booker'))
    from get_by_search_threaded import search_ean

    ean_pack = [ean, item_name, 0.0]
    search_res = search_ean(ean_pack=ean_pack, cookies=cookie_jar.booker_cookies, headers=cookie_jar.booker_headers)
    return search_res

def booker_collector(ean: str, product_name: str):
    search_res = do_ean_search(ean=ean, item_name=product_name)
    item = build_item(link_code=search_res[0], cookies=cookie_jar.booker_cookies, headers=cookie_jar.booker_headers, ean=ean)
    ret_dict = {}

    ret_dict["item_name"] = item.name
    ret_dict["ean"] = item.ean
    ret_dict["supplier_code"] = item.code
    ret_dict["rsp"] = item.rsp
    ret_dict["wholesale_unit_size"] = item.unit_size
    ret_dict["wholesale_price"] = item.b_price

    return ret_dict