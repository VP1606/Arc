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
    mycursor.close()

    return rows

def search_by_ean(mydb: mysql.connector.MySQLConnection, query: str):
    mycursor = mydb.cursor()
    query_sql = f"SELECT * FROM rrpextractsummary WHERE stockref LIKE '%{query}%';"
    mycursor.execute(query_sql)

    rows = mycursor.fetchall()
    mycursor.close()

    return rows

def check_sources(mydb: mysql.connector.MySQLConnection, row: list):
    mycursor = mydb.cursor()

    query = f"SELECT source FROM rrpextract WHERE stockref = {row[0]} AND DATE(datetime) = '{row[3].date()}'"
    mycursor.execute(query)

    rows = mycursor.fetchall()
    mycursor.close()

    returner = {
        'bestway': False,
        'booker': False
    }

    if ('BESTWAY', ) in rows:
        returner['bestway'] = True
    if ('BOOKER', ) in rows:
        returner['booker'] = True

    return returner


def post_processor(mydb: mysql.connector.MySQLConnection, input_list: list):

    # Remove Duplicate EAN's.
    unique_lists = {}
    
    for sublist in input_list:
        first_element = sublist[0]
        if first_element not in unique_lists:
            unique_lists[first_element] = sublist
    
    result = list(unique_lists.values())
    main_result = list()

    for row in result:
        sources = check_sources(mydb=mydb, row=row)
        myrow = list(row)
        myrow.append(sources)
        main_result.append(myrow)

    return main_result


mydb.close()
