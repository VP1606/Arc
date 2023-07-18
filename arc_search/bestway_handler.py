import sys
import os
import json

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
    from get_item import GET_ITEM as GT_GET_ITEM

    item = GT_GET_ITEM(product_code, None, None, True)
    return item

def bestway_collector(product_code: str):
    item = build_item(product_code)
    ret_dict = {}

    ret_dict["item_name"] = item.name
    ret_dict["ean"] = item.ean
    ret_dict["rsp"] = item.rsp
    ret_dict["wholesale_price"] = item.b_price

    return json.dumps(ret_dict)