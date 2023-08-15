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
    query_sql = f"SELECT * " \
                f"FROM rrpextract a " \
                f"WHERE DATE(a.datetime) = ( " \
                f"SELECT DATE(MAX(b.datetime)) FROM rrpextractsummary b " \
                f") " \
                f"AND stockref LIKE '%{query}%';"
    
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