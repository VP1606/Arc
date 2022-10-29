import mysql.connector

class BookerItem:
    def __init__(self, name, b_price, rsp, por, code, vat_rate, brand_name):
        self.name = name
        self.b_price = b_price
        self.rsp = rsp
        self.por = por
        self.code = code
        self.vat_rate = vat_rate
        self.brand = brand_name

    def commit_to_sql(self, mydb):
        vat_val = int(self.vat_rate[:-1]) / 100
        rsp_formatted = float(self.rsp[1:])
        b_price_formatted = float(self.b_price[1:])

        mycursor = mydb.cursor()

        sql = "INSERT INTO rrpextract (datetime, description, price, source, vat, por, 	" \
              "suppliercode, brand, supplier_price) VALUES (NOW(), %s, " \
              "%s, %s, %s, %s, %s, %s, %s) "

        vals = (self.name, rsp_formatted, "BOOKER", vat_val, self.por, self.code, self.brand, b_price_formatted)

        mycursor.execute(sql, vals)
        mydb.commit()