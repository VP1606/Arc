import mysql.connector
import json


def get_date(address):
    mydb = mysql.connector.connect(
        host=address,
        user="mpos",
        password="mpospass",
        database="mpos"
    )
    mycursor = mydb.cursor(buffered=True)

    sql = "select DATE(datetime) " \
          "from rrpextractsummary " \
          "order by datetime desc"

    mycursor.execute(sql)
    mydb.commit()

    records = mycursor.fetchall()
    date = records[0][0]

    date_str = "{0}/{1}/{2}".format(date.strftime("%d"), date.strftime("%m"), date.strftime("%Y"))
    return date_str
