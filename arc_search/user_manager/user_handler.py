import pyotp
import mysql.connector

def make_new_user(username, icon, db):
    cursor = db.cursor()
    key = pyotp.random_base32()

    sql = 'INSERT INTO arc_users_details (user, code, icon) VALUES (%s, %s, %s);'
    values = (username, key, icon)

    cursor.execute(sql, values)
    db.commit()

    return key

def fetch_users():
    db = mysql.connector.connect(
        host="192.168.1.180",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    cursor = db.cursor()

    sql = 'SELECT user_id, icon FROM arc_users_details;'
    cursor.execute(sql)

    res = cursor.fetchall()
    cursor.close()
    db.close()

    return res
