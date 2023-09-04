from bestway_handler import bestway_login
from parfetts_handler import parfetts_login
import importlib
import os, sys
import time

import basket_operator

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(parent_dir, 'bestway'))

import basket_fetch

def do_op():
    basket_operator.run(bw_driver=bw_driver, bw_two_driver=bw_two_driver, pf_driver=pf_driver)

def do_driver_gen():
    start = time.time()
    bw_driver, bw_two_future, pf_driver = basket_operator.driver_gen()
    finish = time.time()

    bw_driver.quit()
    bw_two_future.quit()
    pf_driver.quit()

    print(f"Driver Gen: {finish - start}")

bw_driver, bw_two_driver, pf_driver = basket_operator.driver_gen()
print("ready!")

while True:
    cmd = input("COMMAND: ")
    if cmd == "q":
        break

    elif cmd == "d":
        print("Driver Gen")
        try:
            importlib.reload(basket_fetch)
            importlib.reload(basket_operator)
            do_driver_gen()

        except Exception as e:
            print("An error occurred:", e)
            import traceback
            traceback.print_exc()

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