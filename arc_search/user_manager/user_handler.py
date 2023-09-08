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


def upload_login_creds(type, user_id, username, password):
    db = mysql.connector.connect(
        host="192.168.1.180",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    cursor = db.cursor()

    sql = ""
    if type == "bw":
        sql = 'INSERT INTO arc_users_bw_details (user_id, account_number, pw) VALUES (%s, %s, %s);'
    elif type == "pf":
        sql = 'INSERT INTO arc_users_pf_details (user_id, username, pw) VALUES (%s, %s, %s);'
    else:
        print("UNKNOWN!!!")
        return

    values = (user_id, username, password)

    cursor.execute(sql, values)
    db.commit()

    cursor.close()
    db.close()
    return
