import mysql.connector
import os

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

home_db = mysql.connector.connect(
    host="milecross.dyndns.org",
    user="mpos",
    password="mpospass",
    database="mpos"
)


def rrpextractsummary(mydb):
    mycursor = mydb.cursor()

    sql = "DELETE FROM rrpextractsummary"
    mycursor.execute(sql)
    mydb.commit()

    sql = "INSERT INTO rrpextractsummary " \
          "SELECT stockref, max(price) price, description, now() datetime, por from rrpextract " \
          "where datetime>=DATE_ADD(now(), INTERVAL -1 DAY) " \
          "group by stockref, description"

    mycursor.execute(sql)
    mydb.commit()


def dump_original(mydb):
    cmd = "export MYSQL_PWD=mpospass; mysqldump -h milecross.dyndns.org -u mpos mpos rrpextractsummary --no-tablespaces > summrary_temp.sql"
    os.system(cmd)


def extension_pack(mydb):
    rrpextractsummary(mydb)
    dump_original(mydb)


if __name__ == '__main__':
    extension_pack(home_db)
