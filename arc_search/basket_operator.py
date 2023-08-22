# - Get current basket from Bestway. [x]
# - Compose EAN's of the items using Bestway. (19.3s) [x]
# - Whilst doing so, collect prices. [x]
# - Then do a further extract using the EAN on Booker (7.8s) [x]
# & Parfetts [x]
# Form pack quantities. [x]
# Show ALL in table. [x]
# Verify & Match/Adjust pack quantities for same overall qty. [?]; passed.
# Highlight best supplier. [x]

# Scanning Bestway... |████████████████████████████████████████| 8/8 [100%] in 18.8s (0.42/s) 
# Scanning Booker... |████████████████████████████████████████| 8/8 [100%] in 7.1s (1.13/s) 
# Scanning Parfetts... |████████████████████████████████████████| 8/8 [100%] in 5.7s (1.41/s) 

# On test pub: 44.50s from Postman.

import os, sys, json
from typing import List
from alive_progress import alive_bar
from tabulate import tabulate

from bestway_handler import bestway_login
from booker_handler import booker_collector
from parfetts_handler import parfetts_collector, parfetts_login

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(parent_dir, 'bestway'))

import basket_fetch
import get_item, bway_item

import time
import concurrent.futures

def run_wrapper():
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        bw_future = executor.submit(bestway_login)
        pf_future = executor.submit(parfetts_login)

        bw_driver = bw_future.result()
        pf_driver = pf_future.result()

    finish = time.time()
    print(f"Driver Gen: {finish - start}")

    start = time.time()
    res = run(bw_driver=bw_driver, pf_driver=pf_driver)
    finish = time.time()
    print(f"RES Wrapper Time: {finish - start}")
    return res

def run(bw_driver, pf_driver):
    # bw_driver = bestway_login()
    basket: List[basket_fetch.BasketItem] = basket_fetch.get_basket(driver=bw_driver)

    start = time.time()

    with alive_bar(len(basket), title="Scanning Bestway...", force_tty=True) as bar:
        for _, item in enumerate(basket):
            ext = item.bw_extension.split("/")[-1]
            remote_item_bw: bway_item.BestwayItem = get_item.GET_ITEM_selenium(link_code=ext, driver=bw_driver, collect_pricing=True)

            item.ean = remote_item_bw.ean
            item.bw_unit_price = float(remote_item_bw.b_price.replace('£', ''))
            item.bw_total = item.bw_unit_price * item.quantity

            bar()

    finish = time.time()
    print(f"Bestway Time: {finish - start}")

    start = time.time()

    with alive_bar(len(basket), title="Scanning Booker...", force_tty=True) as bar:
        for _, item in enumerate(basket):
            try:
                res = booker_collector(ean=item.ean, product_name=item.name)

                item.bk_product_code = res["supplier_code"]
                item.bk_pack_size = res["wholesale_unit_size"]
                item.bk_unit_price = float(res["wholesale_price"].replace('£', ''))
                item.bk_total = item.bk_unit_price * item.quantity
                item.form_bk_pack_qty()
                item.bk_instock = True
            except:
                item.bk_instock = False

            bar()
    
    finish = time.time()
    print(f"Booker Time: {finish - start}")

    start = time.time()

    with alive_bar(len(basket), title="Scanning Parfetts...", force_tty=True) as bar:
        for _, item in enumerate(basket):
            try:
                res = parfetts_collector(ean=item.ean, name=item.name, driver=pf_driver)

                item.pf_product_code = res["supplier_code"]
                item.pf_pack_size = res["wholesale_unit_size"]
                item.pf_unit_price = float(res["wholesale_price"].replace('£', ''))
                item.pf_total = item.pf_unit_price * item.quantity
                item.form_pf_pack_qty()
                item.pf_instock = True
            except:
                item.pf_instock = False
                
            bar()

    finish = time.time()
    print(f"Parfetts Time: {finish - start}")

    # table = [
    #     ['Supplier', 'Name', 'EAN', 'qty', 'formed_qty', 'Unit Price', 'Total Price', 'Delta to BW']
    # ]

    # for item in basket:
    #     table.append(['Bestway', item.name, item.ean, item.quantity, item.bw_pack_qty, item.bw_unit_price, item.bw_total, 0.0])
        
    #     if item.bk_instock:
    #         table.append(['Booker', '', '', '', item.bk_pack_qty, item.bk_unit_price, item.bk_total, round((item.bk_total - item.bw_total), 2)])

    #     if item.pf_instock:
    #         table.append(['Parfetts', '', '', '', item.pf_pack_qty, item.pf_unit_price, item.pf_total, round((item.pf_total - item.bw_total), 2)])

    #     table.append(['- - - - - -', '- - - - - -', '- - - - - -', '- - - - - -', '- - - - - -', '- - - - - -', '- - - - - -', '- - - - - -'])
    #     table.append(['Best Supplier:', item.best_supplier, '', '', '', '', '', ''])
    #     table.append(['Best Price:', item.best_price, '', '', '', '', '', ''])
    #     table.append(['Delta to BW:', item.delta_to_bw, '', '', '', '', '', ''])
    #     table.append(['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----'])

    # form_table = tabulate(table[1:], headers=table[0], tablefmt="pretty")
    # print(form_table)

    start = time.time()

    dump_array = []
    for item in basket:
        item.find_best_supplier()
        dump_array.append(item.to_dict())

    finish = time.time()
    print(f"Cleanup Prep Time: {finish - start}")
    
    # print(json.dumps(dump_array))
    return dump_array
