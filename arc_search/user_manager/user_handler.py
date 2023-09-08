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

def fetch_creds(type, user_id):
    db = mysql.connector.connect(
        host="192.168.1.180",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    cursor = db.cursor()

    if type == "bw":
        sql = f'SELECT account_number, pw FROM arc_users_bw_details WHERE user_id = {user_id};'
    elif type == "pf":
        sql = f'SELECT username, pw FROM arc_users_pf_details WHERE user_id = {user_id};'
    else:
        print("UNKNOWN!!!")
        return
    
    cursor.execute(sql)

    res = cursor.fetchall()[0]
    cursor.close()
    db.close()

    return res

# print(fetch_creds("pf", 2))
# upload_login_creds("pf", 3, "manove@gmail.com", "aRiOq58h")