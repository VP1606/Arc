import mysql.connector
import user_handler, otp_handler

mydb = mysql.connector.connect(
        host="192.168.1.180",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

# user_handler.make_new_user("demo", mydb)

while True:
    code = int(input())
    print(otp_handler.check_otp(username='demo', code=code, db=mydb))