import schedule
import time as time_pack
import os
import argparse


def operator(db_name):
    if db_name == "nth":
        os.system("./run_main.sh")
    elif db_name == "mlc":
        os.system("./run_cross.sh")
    else:
        os.system("./run_main.sh")


parser = argparse.ArgumentParser()

parser.add_argument("-db", "--database", help="Database Select (nth | mlc)", type=str, default="nth")
parser.add_argument("-day", "--day", help="Specify Run Day in full.", type=str, default="monday")
parser.add_argument("-time", "--time", help="Specify Run Time(24HR; HH:MM)", type=str, default="00:00")

args = parser.parse_args()

db = str.lower(args.database)
if db != "nth" and db != "mlc":
    print("Unknown DB! Defaulting to Netherley...")
    db = "nth"

day = str.lower(args.day)

time = str.lower(args.time)
if ":" not in time or len(time) != 5:
    print("Invalid Time! Resetting to 12AM...")
    time = "00:00"

if day == "monday" or "mon":
    schedule.every().monday.at(time).do(operator, db)
elif day == "tuesday" or "tues":
    schedule.every().tuesday.at(time).do(operator, db)
elif day == "wednesday" or "wed":
    schedule.every().wednesday.at(time).do(operator, db)
elif day == "thursday" or "thurs":
    schedule.every().thursday.at(time).do(operator, db)
elif day == "friday" or "fri":
    schedule.every().friday.at(time).do(operator, db)
elif day == "saturday" or "sat":
    schedule.every().saturday.at(time).do(operator, db)
elif day == "sunday" or "sun":
    schedule.every().sunday.at(time).do(operator, db)
else:
    schedule.every().monday.at(time).do(operator, db)

while True:
    schedule.run_pending()
    time_pack.sleep(1)