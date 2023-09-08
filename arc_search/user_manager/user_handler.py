import pyotp

def make_new_user(username, db):
    cursor = db.cursor()
    key = pyotp.random_base32()

    sql = 'INSERT INTO arc_users_details (user, code) VALUES (%s, %s);'
    values = (username, key)

    cursor.execute(sql, values)
    db.commit()

    return key