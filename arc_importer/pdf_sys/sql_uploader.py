import mysql.connector

def upload_blocks(blocks: list):
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
          "VALUES (%s,%s,%s,%s,%s,NOW())"

    for block in blocks:
        rrp = float(block[1].replace("£", ""))
        vals = [block[3], block[0], rrp, block[4], block[2]]
        mycursor.execute(sql, vals)
    
    mydb.commit()
    mydb.close()
    return True