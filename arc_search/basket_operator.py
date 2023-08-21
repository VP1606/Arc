# - Get current basket from Bestway. [x]
# - Compose EAN's of the items using Bestway. (19.3s) [x]
# - Whilst doing so, collect prices. [x]
# - Then do a further extract using the EAN on Booker (7.8s) [x]
# & Parfetts [x]
# Verify & Match pack sizes for same overall qty.
# Show ALL in table.
# Highlight best supplier.

# Scanning Bestway... |████████████████████████████████████████| 8/8 [100%] in 18.8s (0.42/s) 
# Scanning Booker... |████████████████████████████████████████| 8/8 [100%] in 7.1s (1.13/s) 
# Scanning Parfetts... |████████████████████████████████████████| 8/8 [100%] in 5.7s (1.41/s) 

import os, sys
from typing import List
from alive_progress import alive_bar

from bestway_handler import bestway_login
from booker_handler import booker_collector
from parfetts_handler import parfetts_collector

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(parent_dir, 'bestway'))

import basket_fetch
import get_item, bway_item

def run(bw_driver, pf_driver):
    # bw_driver = bestway_login()
    basket: List[basket_fetch.BasketItem] = basket_fetch.get_basket(driver=bw_driver)

    with alive_bar(len(basket), title="Scanning Bestway...", force_tty=True) as bar:
        for _, item in enumerate(basket):
            ext = item.bw_extension.split("/")[-1]
            remote_item_bw: bway_item.BestwayItem = get_item.GET_ITEM_selenium(link_code=ext, driver=bw_driver, collect_pricing=True)

            item.ean = remote_item_bw.ean
            item.bw_unit_price = float(remote_item_bw.b_price.replace('£', ''))
            item.bw_total = item.bw_unit_price * item.quantity

            bar()

    with alive_bar(len(basket), title="Scanning Booker...", force_tty=True) as bar:
        for _, item in enumerate(basket):
            try:
                res = booker_collector(ean=item.ean, product_name=item.name)

                item.bk_product_code = res["supplier_code"]
                item.bk_pack_size = res["wholesale_unit_size"]
                item.bk_unit_price = float(res["wholesale_price"].replace('£', ''))
                item.bk_total = item.bk_unit_price * item.quantity

                item.bk_instock = True
            except:
                item.bk_instock = False

            bar()

    with alive_bar(len(basket), title="Scanning Parfetts...", force_tty=True) as bar:
        for _, item in enumerate(basket):
            try:
                res = parfetts_collector(ean=item.ean, name=item.name, driver=pf_driver)

                item.pf_product_code = res["supplier_code"]
                item.pf_pack_size = res["wholesale_unit_size"]
                item.pf_unit_price = float(res["wholesale_price"].replace('£', ''))
                item.pf_total = item.pf_unit_price * item.quantity

                item.pf_instock = True
            except:
                item.pf_instock = False
                
            bar()

    for item in basket:
        item.show_console()
