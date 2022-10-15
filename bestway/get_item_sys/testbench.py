import mysql.connector

mydb = mysql.connector.connect(
    host="netherly1.dyndns.org",
    user="mpos",
    password="mpospass",
    database="mpos"
)

mycursor = mydb.cursor()

sql = "INSERT INTO rrpextract (datetime, stockref, description, price, source, vat) VALUES (NOW(), %s, %s, %s, %s, %s)"
vals = ("HHTESTREF", "1234567890123456789012345678901234567890123456", 1.99, "dsa", 0.2)

mycursor.execute(sql, vals)
mydb.commit()

print(mycursor.rowcount, "record inserted.")