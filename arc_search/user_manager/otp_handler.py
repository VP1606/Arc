import pyotp
import mysql.connector

def check_otp(username, code):
    db = mysql.connector.connect(
        host="192.168.1.180",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    cursor = db.cursor()

    sql = 'SELECT code from arc_users_details where user="{0}";'.format(username)
    cursor.execute(sql)
    key = cursor.fetchall()[0][0]

    totp = pyotp.TOTP(key)
    return totp.verify(code)