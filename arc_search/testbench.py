from bestway_handler import bestway_login
from parfetts_handler import parfetts_login
import importlib
import os, sys

import basket_operator

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(parent_dir, 'bestway'))

import basket_fetch

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
            importlib.reload(basket_fetch)
            importlib.reload(basket_operator)
            do_op()

        except Exception as e:
            print("An error occurred:", e)
            import traceback
            traceback.print_exc()

bw_driver.quit()
pf_driver.quit()