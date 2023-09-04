import sys
import os
import json
import cookie_jar

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from booker.ean_search_sys import search_ean

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
    # Status (OK, MULTIPLE, NOT_FOUND), name, rrp, ws_price, supplier_code, unit_size, no_hits
    item_result_block = search_ean(ean=ean, name=product_name, cookies=cookie_jar.booker_cookies, headers=cookie_jar.booker_headers)

    if item_result_block[0] == "OK":
        ret_dict = {}

        rrp = item_result_block[2]
        rrp = rrp.replace("RRP: ", "")

        ret_dict["item_name"] = item_result_block[1]
        ret_dict["ean"] = ean
        ret_dict["rsp"] = rrp
        ret_dict["wholesale_price"] = item_result_block[3]

        ret_dict["supplier_code"] = item_result_block[4]
        ret_dict["wholesale_unit_size"] = item_result_block[5]


        return ret_dict
    else:
        ret_msg = cookie_jar.res_unavailable_message  
        ret_msg["no_search_hits"] = item_result_block[4]
        ret_msg["status"] = item_result_block[0]
        return ret_msg
