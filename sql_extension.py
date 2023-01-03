import mysql.connector

# mydbs = [mysql.connector.connect(
#         host="milecross.dyndns.org",
#         user="mpos",
#         password="mpospass",
#         database="mpos"
#     ), mysql.connector.connect(
#         host="netherly1.dyndns.org",
#         user="mpos",
#         password="mpospass",
#         database="mpos"
#     ), mysql.connector.connect(
#         host="runcorn.dyndns.org",
#         user="mpos",
#         password="mpospass",
#         database="mpos"
#     ), mysql.connector.connect(
#         host="rathbone.dyndns.org",
#         user="mpos",
#         password="mpospass",
#         database="mpos"
#     ),
#     mysql.connector.connect(
#         host="breezehill1.dyndns.org",
#         user="mpos",
#         password="mpospass",
#         database="mpos"
#     )]

mydbs = [mysql.connector.connect(
        host="milecross.dyndns.org",
        user="mpos",
        password="mpospass",
        database="mpos"
    ), mysql.connector.connect(
        host="netherly1.dyndns.org",
        user="mpos",
        password="mpospass",
        database="mpos"
    )]


def rrpextractsummary(mydb):
    mycursor = mydb.cursor()

    sql = "DELETE FROM rrpextractsummary"
    mycursor.execute(sql)
    mydb.commit()

    sql = "INSERT INTO rrpextractsummary " \
          "SELECT stockref, max(price) price, description, now() datetime from rrpextract " \
          "where datetime>=DATE_ADD(now(), INTERVAL -1 DAY) " \
          "group by stockref, description"

    mycursor.execute(sql)
    mydb.commit()


def tblpc_rrpsummary(mydb):
    mycursor = mydb.cursor()

    sql = "UPDATE rrpextractsummary r, tbl_products_compaire p " \
          "SET supplierRRP=r.price, supplierdescription=left(r.description, 30) " \
          "WHERE r.stockref=p.stockref and r.price > ifnull(supplierrrp, 0)"

    mycursor.execute(sql)
    mydb.commit()


def notinpctable(mydb):
    mycursor = mydb.cursor()

    sql = "DELETE FROM rrpextractsummary_notinpctable"

    mycursor.execute(sql)
    mydb.commit()

    sql = "INSERT INTO rrpextractsummary_notinpctable " \
          "SELECT distinct stockref from rrpextractsummary " \
          "WHERE stockref not in (select stockref from tbl_products_compaire)"

    mycursor.execute(sql)
    mydb.commit()


def step_six(mydb):
    mycursor = mydb.cursor()

    sql = "INSERT INTO tbl_products_compaire(stockref, supplierrrp, supplierdescription, updatedat, createdat, " \
          "description2) " \
          "SELECT r.stockref, price, left(description, 30), now(), now(), '' " \
          "FROM rrpextractsummary r, rrpextractsummary_notinpctable n " \
          "WHERE r.stockref =n.stockref"

    mycursor.execute(sql)
    mydb.commit()


def extension_pack(mydb):
    rrpextractsummary(mydb)
    tblpc_rrpsummary(mydb)
    notinpctable(mydb)
    step_six(mydb)


if __name__ == '__main__':
    for mydb in mydbs:
        extension_pack(mydb)
