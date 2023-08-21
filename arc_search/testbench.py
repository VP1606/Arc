from bestway_handler import bestway_login
import importlib
import os, sys

import basket_operator

def do_op():
    basket_operator.run(bw_driver=driver)

driver = bestway_login()
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