from bestway_handler import bestway_login
import importlib
import os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(parent_dir, 'bestway'))
import basket_fetch

def do_op():
    basket_fetch.get_basket(driver=driver)

driver = bestway_login()
print("ready!")

while True:
    cmd = input("COMMAND: ")
    if cmd == "q":
        break
    else:
        try:
            importlib.reload(basket_fetch)
            do_op()

        except Exception as e:
            print("An error occurred:", e)
            import traceback
            traceback.print_exc()

driver.quit()