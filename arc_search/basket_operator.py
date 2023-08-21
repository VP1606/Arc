# - Get current basket from Bestway.
# - Compose EAN's of the items using Bestway.
# - Whilst doing so, collect prices.
# - Then do a further extract using the EAN on Booker & Parfetts

import os, sys
from bestway_handler import bestway_login

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(parent_dir, 'bestway'))

import basket_fetch
import get_item, bway_item

def run(bw_driver):
    # bw_driver = bestway_login()
    basket: list = basket_fetch.get_basket(driver=bw_driver)

    for _, item in enumerate(basket):
        ext = item.bw_extension.split("/")[-1]
        remote_item_bw: bway_item.BestwayItem = get_item.GET_ITEM_selenium(link_code=ext, driver=bw_driver, collect_pricing=True)

        item.ean = remote_item_bw.ean
        item.bw_unit_price = float(remote_item_bw.b_price.replace('£', ''))
        item.bw_total = item.bw_unit_price * item.quantity

    for item in basket:
        item.show_console()
