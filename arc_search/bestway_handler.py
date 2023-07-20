import sys
import os
import json
import cookie_jar

# class BestwayItem(
#     name: Any,
#     unit_size: Any,
#     b_price: Any | str,
#     rsp: Any | str,
#     por: Any | str,
#     pack_size: Any | str,
#     code: Any | str,
#     ean: Any | str,
#     vat_rate: Any | str

def build_item(product_code):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(os.path.join(parent_dir, 'bestway'))
    from get_item import GET_ITEM

    item = GET_ITEM(product_code, cookies=cookie_jar.bestway_cookies, headers=cookie_jar.bestway_headers, collect_pricing=True)
    return item

def bestway_collector(ean: str):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(os.path.join(parent_dir, 'bestway'))
    from ean_search_sys import search_ean

    search_res = search_ean(ean=ean, cookies=cookie_jar.bestway_cookies, headers=cookie_jar.bestway_headers)

    if search_res[0] is True:
        item = search_res[1]
        ret_dict = {}

        ret_dict["item_name"] = item.name
        ret_dict["ean"] = item.ean
        ret_dict["supplier_code"] = item.code
        ret_dict["rsp"] = item.rsp
        ret_dict["wholesale_unit_size"] = item.unit_size
        ret_dict["wholesale_price"] = item.b_price

        return ret_dict

    else:
        return cookie_jar.res_unavailable_message