from bestway_handler import bestway_login
from parfetts_handler import parfetts_login
import importlib
import os, sys

import basket_operator

def do_op():
    basket_operator.run(bw_driver=bw_driver, pf_driver=pf_driver)

bw_driver = bestway_login()
pf_driver = parfetts_login()
print("ready!")

while True:
    cmd = input("COMMAND: ")
    if cmd == "q":
        break
    else:
        try:
            importlib.reload(basket_operator)
            do_op()

        except Exception as e:
            print("An error occurred:", e)
            import traceback
            traceback.print_exc()

driver.quit()