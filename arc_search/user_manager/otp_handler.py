import pyotp

def check_otp(username, code, db):
    cursor = db.cursor()

    sql = 'SELECT code from arc_users_details where user="{0}";'.format(username)
    cursor.execute(sql)
    key = cursor.fetchall()[0][0]

    totp = pyotp.TOTP(key)
    return totp.verify(code)