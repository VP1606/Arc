import mysql.connector


class BookerItem:
    def __init__(self, name, b_price, rsp, por, code, vat_rate, brand_name, unit_size, ean):
        self.name = name
        self.b_price = b_price
        self.rsp = rsp
        self.por = por
        self.code = code
        self.vat_rate = vat_rate
        self.brand = brand_name
        self.unit_size = unit_size
        self.ean = ean
    def commit_to_sql(self, mydb):

        vat_val = 0.0
        if self.vat_rate != "":
            vat_val = int(self.vat_rate[:-1]) / 100

        rsp_formatted = float(self.rsp[1:])
        b_price_formatted = float(self.b_price[1:])

        por = str(self.por).replace("%", "")
        por = float(por)

        mycursor = mydb.cursor()

        sql = "INSERT INTO rrpextract (datetime, stockref, description, price, source, vat, por, 	" \
              "suppliercode, brand, supplier_price, supplier_packsize) VALUES (NOW(), %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s) "

        vals = (self.ean, self.name, rsp_formatted, "BOOKER", vat_val, por, self.code, self.brand, b_price_formatted, self.unit_size)

        mycursor.execute(sql, vals)
        mydb.commit()
