import mysql.connector
import json


def local_generator(address):
    mydb = mysql.connector.connect(
        host=address,
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    mycursor = mydb.cursor()

    # print("Dropping Table23...")

    sql = "drop table if exists _lastordery23"
    mycursor.execute(sql)
    mydb.commit()

    # print("Done.")
    # print("Creating Table23...")

    sql = "create table _lastordery23 " \
          "SELECT max(t.datetime) d , product " \
          "FROM tbl_transactions t, tbl_transaction_details td " \
          "Where t.id = td.transactionid " \
          "group by product"

    mycursor.execute(sql)
    mydb.commit()
    # print(mycursor.fetchall())

    # print("Done.")
    # print("Fetching RAW List...")

    mycursor = mydb.cursor(buffered=True)

    sql = "select t.stockref, t.description,r.description as supplierdescr, t.retailprice as ourprice ,  r.price as rrp , p.d  as lastsolddate, por, vat " \
          "from tbl_products t, _lastordery23 p , rrpextractsummary r " \
          "where t.stockref= p.product and r.stockref=t.stockref " \
          "and r.price>t.retailprice and p.d > date_add(now(),Interval -100 day )"

    mycursor.execute(sql)
    mydb.commit()

    records = mycursor.fetchall()

    book = []
    for rec in records:
        res = {
            "stockref": int(rec[0]),
            "description": str(rec[2]),
            "current": float(rec[3]),
            "rrp": float(rec[4]),
            "por": float(rec[6]),
            "vat": float(rec[7]),
            "local_description": str(rec[1])
        }

        book.append(res)

    # print(len(book))
    print("DONE {0}".format(address))

    return json.dumps(book)
