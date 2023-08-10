import mysql.connector

mydb = mysql.connector.connect(
        host="192.168.1.180",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

def search_by_name(mydb: mysql.connector.MySQLConnection, query: str):
    mycursor = mydb.cursor()
    query_sql = f"SELECT * FROM rrpextractsummary WHERE description LIKE '%{query}%';"
    mycursor.execute(query_sql)

    rows = mycursor.fetchall()
    for row in rows:
        print(row)
    print(len(rows))

    mycursor.close()

def search_by_ean(mydb: mysql.connector.MySQLConnection, query: str):
    mycursor = mydb.cursor()
    query_sql = f"SELECT * FROM rrpextractsummary WHERE stockref LIKE '%{query}%';"
    mycursor.execute(query_sql)

    rows = mycursor.fetchall()
    for row in rows:
        print(row)
    print(len(rows))

    mycursor.close()

mydb.close()
