import mysql.connector
import time

def search_by_name(mydb: mysql.connector.MySQLConnection, query: str):
    stime = time.time()

    mycursor = mydb.cursor()
    query_sql = f"SELECT * " \
                f"FROM rrpextract a " \
                f"WHERE DATE(a.datetime) = ( " \
                f"SELECT DATE(MAX(b.datetime)) FROM rrpextractsummary b " \
                f") " \
                f"AND description LIKE '%{query}%';"
    
    mycursor.execute(query_sql)
    rows = mycursor.fetchall()
    mycursor.close()

    pstime = time.time()
    post_rows = new_post(raw=rows)
    pftime = time.time()

    ftime = time.time()
    print(f"Name Search Time: {ftime - stime}")
    print(f"Name Search POST Time: {pftime - pstime}")

    return post_rows

def search_by_ean(mydb: mysql.connector.MySQLConnection, query: str):
    stime = time.time()

    mycursor = mydb.cursor()
    query_sql = f"SELECT * FROM rrpextractsummary WHERE stockref LIKE '%{query}%';"
    mycursor.execute(query_sql)
    rows = mycursor.fetchall()
    mycursor.close()

    pstime = time.time()
    post_rows = post_processor(mydb=mydb, input_list=rows)
    pftime = time.time()

    ftime = time.time()
    print(ftime - stime)

    print(f"EAN Search Time: {ftime - stime}")
    print(f"EAN Search POST Time: {pftime - pstime}")

    return post_rows

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
        myrow[3] = myrow[3].strftime('%Y-%m-%d %H:%M:%S')
        main_result.append(myrow)

    return main_result

# ['3057640100833', 7.65, 'Volvic Natural Mineral Water 6 x 1.5L', '2023-08-14 16:47:22', 31.14, 0.2, {'bestway': True, 'booker': False}]
# '3057640111983': ['Volvic Natural Mineral Water 6 x 500ml', 'BESTWAY', 'BESTWAY']

def new_post(raw: list):
    collated = {}
    for row in raw:
        stockref = row[2]
        desc = row[3]
        source = row[5]

        if stockref in collated:
            collated[stockref].append(source)
        else:
            collated[stockref] = [desc, source]
        
    main_list = list()
    for stockref, values in collated.items():
        frame = [stockref, 0.0, values[0], '', 0.0, 0.0]
        sources = {
            'bestway': False,
            'booker': False
        }

        if 'BESTWAY' in values:
            sources['bestway'] = True
        if 'BOOKER' in values:
            sources['booker'] = True

        frame.append(sources)
        main_list.append(frame)

    return main_list