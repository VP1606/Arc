import mysql.connector


def update_desc(desc, address, ean):
    mydb = mysql.connector.connect(
        host=address,
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    mycursor = mydb.cursor()

    sql = "UPDATE tbl_products " \
          "SET description = %s " \
          "WHERE stockref = %s"

    values = (desc, ean)

    mycursor.execute(sql, values)
    mydb.commit()
    mydb.close()
