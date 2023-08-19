import mysql.connector

# ['3057640100833', 7.65, 'Volvic Natural Mineral Water 6 x 1.5L', '2023-08-14 16:47:22', 31.14, 0.2, {'bestway': True, 'booker': False}]
# '3057640111983': ['Volvic Natural Mineral Water 6 x 500ml', 'BESTWAY', 'BESTWAY']

def extract_search_main(mydb: mysql.connector.MySQLConnection, query: str, mode: str):

    search_key = "description"
    if mode == "ean":
        search_key = "stockref"
    elif mode == "name":
        search_key = "description"
    else:
        pass

    query = query.replace("'", "''")

    mycursor = mydb.cursor()
    query_sql = f"SELECT * " \
                f"FROM rrpextractsummary " \
                f"WHERE {search_key} LIKE '%{query}%';"
    
    mycursor.execute(query_sql)
    rows = mycursor.fetchall()
    mycursor.close()

    post_rows = new_post(raw=rows)
    return post_rows

def new_post(raw: list):
    collated = {}
    for row in raw:
        stockref = row[0]
        desc = row[2]

        if stockref in collated:
            pass
        else:
            collated[stockref] = [desc]
        
    main_list = list()
    for stockref, values in collated.items():
        frame = [stockref, 0.0, values[0], '', 0.0, 0.0]
        main_list.append(frame)

    return main_list