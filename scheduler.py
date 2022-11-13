import schedule
import time
import os

def operator():
    os.system("./run_main.sh")

schedule.every().monday.at("00:00").do(operator)

while True:
    schedule.run_pending()
    time.sleep(1)