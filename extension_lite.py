import mysql.connector
import os

home_db_address = str(os.environ.get("HOME_SQL"))
home_db = mysql.connector.connect(
    host=home_db_address,
    user="mpos",
    password="mpospass",
    database="mpos"
)

target_dbs = [
    "netherly1.dyndns.org",
    "runcorn.dyndns.org",
    "rathbone.dyndns.org",
    "breezehill1.dyndns.org"
]


def rrpextractsummary(mydb):
    mycursor = mydb.cursor()

    sql = "DELETE FROM rrpextractsummary"
    mycursor.execute(sql)
    mydb.commit()

    sql = "INSERT INTO rrpextractsummary " \
          "SELECT stockref, max(price) price, description, now() datetime, por, vat from rrpextract " \
          "where datetime>=DATE_ADD(now(), INTERVAL -1 DAY) " \
          "group by stockref, description, por, vat"

    mycursor.execute(sql)
    mydb.commit()


def dump_original(mydb):
    cmd = "export MYSQL_PWD=mpospass; mysqldump -h milecross.dyndns.org -u mpos mpos rrpextractsummary --no-tablespaces > summary_temp.sql"
    os.system(cmd)
    cmd = "sed -i 's/utf8mb4_0900_ai_ci/utf8mb4_unicode_ci/' summary_temp.sql"
    os.system(cmd)


def export_to_all(targets):
    for target in targets:
        cmd = "export MYSQL_PWD=mpospass; mysql -h {0} -u mpos mpos < summary_temp.sql".format(str(target))
        os.system(cmd)


def extension_pack(mydb, targets):
    rrpextractsummary(mydb)
    dump_original(mydb)
    export_to_all(targets)


if __name__ == '__main__':
    extension_pack(home_db, target_dbs)
