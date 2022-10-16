import mysql.connector
class BestwayItem:
    def __init__(self, name, unit_size, b_price, rsp, por, pack_size, code, ean, vat_rate, brand):
        self.name = name
        self.unit_size = unit_size
        self.b_price = b_price
        self.rsp = rsp
        self.por = por
        self.pack_size = pack_size
        self.code = code
        self.ean = ean
        self.vat_rate = vat_rate
        self.brand = brand

    def commit_to_sql(self, mydb):
        vat_val = 0.0
        if self.vat_rate == "Exempt":
            vat_val = 0.0
        elif self.vat_rate == "Standard":
            vat_val = 0.2
        else:
            print("VAT RATE ERROR")

        rsp_formatted = float(self.rsp[1:])

        mycursor = mydb.cursor()

        sql = "INSERT INTO rrpextract (datetime, stockref, description, price, source, vat) VALUES (NOW(), %s, %s, %s, %s, %s)"
        vals = (self.ean, self.name, rsp_formatted, "BESTWAY", vat_val)

        mycursor.execute(sql, vals)
        mydb.commit()