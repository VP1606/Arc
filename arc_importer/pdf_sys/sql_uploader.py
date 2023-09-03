import mysql.connector

def upload_blocks(blocks: list, date):
    mydb = mysql.connector.connect(
        host="milecross.dyndns.org",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    #                0      1         2    3     4
    # Block Format: [Desc, RRP (STR), EAN, PLOF, SIZE]

    mycursor = mydb.cursor()

    sql = "INSERT INTO bestwayinvoice(pid,description," \
          "price,size,stockref,date_transaction)" \
          "VALUES (%s,%s,%s,%s,%s,%s)"

    for block in blocks:
        print(block)
        rrp = 0.0
        try:
            rrp = float(block[1].replace("£", ""))
        except:
            if block[1] == '':
                rrp = 0.0
            elif '£' in block[1]:
                parts = block[1].split()
                for part in parts:
                    if '£' in part:
                        rrp = float(part.replace("£", ""))
                        break

        vals = [block[3], block[0], rrp, block[4], block[2], date]
        mycursor.execute(sql, vals)
    
    mydb.commit()
    mydb.close()
    return True