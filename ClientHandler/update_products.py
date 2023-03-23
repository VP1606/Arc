import mysql.connector
import json


def get_all_products(address, period):
    mydb = mysql.connector.connect(
        host=address,
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    mycursor = mydb.cursor()

    # sql = "SELECT * " \
    #       "FROM tbl_products "

    sql = "select * " \
          "from tbl_products t, _lastordery23 p " \
          "where t.StockRef=p.product and p.d > date_add(now(),Interval -{0} day);".format(period)

    mycursor.execute(sql)
    res = mycursor.fetchall()

    book = []
    for index, rec in enumerate(res):
        try:
            look = {
                "stockref": int(rec[0]),
                "description": str(rec[1]),
                "current_rrp": float(rec[4])
            }
            book.append(look)

        except:
            print("ERROR INDEX {0}".format(index))
            # print(rec)

    return json.dumps(book)


def get_all_rrps(address):
    mydb = mysql.connector.connect(
        host=address,
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    mycursor = mydb.cursor()

    sql = "SELECT * " \
          "FROM rrpextractsummary "

    mycursor.execute(sql)
    res = mycursor.fetchall()

    book = []
    for index, rec in enumerate(res):
        try:
            look = {
                "stockref": int(rec[0]),
                "rrp": float(rec[1]),
                "por": float(rec[4]),
                "vat": float(rec[5]),
            }
            book.append(look)

        except:
            print("ERROR INDEX {0}".format(index))
            # print(rec)

    return json.dumps(book)