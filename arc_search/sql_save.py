import mysql.connector

mydb = mysql.connector.connect(
        host="192.168.1.180",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

def process_results(results: dict):
    bestway = results["bestway"]
    booker = results["booker"]
    parfetts = results["parfetts"]

    ean = "-"
    ean_done = False

    bw_desc, bw_price, bw_sp_code, bw_sp_price, bw_sp_size = "-", 0.0, "-", 0.0, "-"
    bk_desc, bk_price, bk_sp_code, bk_sp_price, bk_sp_size = "-", 0.0, "-", 0.0, "-"
    pf_desc, pf_price, pf_sp_code, pf_sp_price, pf_sp_size = "-", 0.0, "-", 0.0, "-"

    if bestway.get("status") is None:
        ean = bestway["ean"]

        bw_desc = bestway["item_name"]
        bw_price = bestway["rsp"] 
        bw_sp_code = bestway["supplier_code"]
        bw_sp_price = bestway["wholesale_price"]
        bw_sp_size = bestway["wholesale_unit_size"]

        bw_price = float(bw_price[1:])
        bw_sp_price = float(bw_sp_price[1:])

    if booker.get("status") is None:
        if ean_done is False:
            ean = booker["ean"]

        bk_desc = booker["item_name"]
        bk_price = booker["rsp"] 
        bk_sp_code = booker["supplier_code"]
        bk_sp_price = booker["wholesale_price"]
        bk_sp_size = booker["wholesale_unit_size"]

        bk_price = float(bk_price[1:])
        bk_sp_price = float(bk_sp_price[1:])

    if parfetts.get("status") is None:
        if ean_done is False:
            ean = parfetts["ean"]

        pf_desc = parfetts["item_name"]
        pf_price = parfetts["rsp"] 
        pf_sp_price = parfetts["wholesale_price"]

        pf_price = float(pf_price[1:])
        pf_sp_price = float(pf_sp_price[1:])

    mycursor = mydb.cursor()

    sql = "INSERT INTO arc_search_results(datetime, stockref, " \
          "bestway_desc, bestway_price, bestway_suppliercode, bestway_supplier_price, bestway_supplier_packsize, " \
          "booker_desc, booker_price, booker_suppliercode, booker_supplier_price, booker_supplier_packsize, " \
          "parfetts_desc, parfetts_price, parfetts_suppliercode, parfetts_supplier_price, parfetts_supplier_packsize) " \
          "VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    vals = (
            ean, 
            bw_desc, bw_price, bw_sp_code, bw_sp_price, bw_sp_size,
            bk_desc, bk_price, bk_sp_code, bk_sp_price, bk_sp_size,
            pf_desc, pf_price, pf_sp_code, pf_sp_price, pf_sp_size
        )

    mycursor.execute(sql, vals)
    mydb.commit()
