import schedule
import time as time_pack
import os
import argparse


def operator():
    os.system("./run_cross.sh")


parser = argparse.ArgumentParser()

parser.add_argument("-day", "--day", help="Specify Run Day in full.", type=str, default="monday")
parser.add_argument("-time", "--time", help="Specify Run Time(24HR; HH:MM)", type=str, default="00:00")

args = parser.parse_args()

day = str.lower(args.day)

time = str.lower(args.time)
if ":" not in time or len(time) != 5:
    print("Invalid Time! Resetting to 12AM...")
    time = "00:00"

if day == "monday" or "mon":
    schedule.every().monday.at(time).do(operator)
elif day == "tuesday" or "tues":
    schedule.every().tuesday.at(time).do(operator)
elif day == "wednesday" or "wed":
    schedule.every().wednesday.at(time).do(operator)
elif day == "thursday" or "thurs":
    schedule.every().thursday.at(time).do(operator)
elif day == "friday" or "fri":
    schedule.every().friday.at(time).do(operator)
elif day == "saturday" or "sat":
    schedule.every().saturday.at(time).do(operator)
elif day == "sunday" or "sun":
    schedule.every().sunday.at(time).do(operator)
else:
    schedule.every().monday.at(time).do(operator)

while True:
    schedule.run_pending()
    time_pack.sleep(1)