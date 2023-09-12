import pyotp
import mysql.connector

def check_otp(user_id, code):
    db = mysql.connector.connect(
        host="192.168.1.180",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    cursor = db.cursor()

    sql = 'SELECT code from arc_users_details where user_id="{0}";'.format(user_id)
    cursor.execute(sql)
    key = cursor.fetchall()[0][0]

    cursor.close()
    db.close()

    totp = pyotp.TOTP(key)
    return totp.verify(code)