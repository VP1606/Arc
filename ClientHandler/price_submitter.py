import mysql.connector


def price_upload(address, stockref, price):
    mydb = mysql.connector.connect(
        host=address,
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    mycursor = mydb.cursor()

    sql = "UPDATE tbl_products " \
          "SET RetailPrice = %s " \
          "WHERE StockRef = %s "

    vals = (price, stockref)

    mycursor.execute(sql, vals)
    mydb.commit()
    mydb.close()