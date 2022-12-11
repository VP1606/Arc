import mysql.connector


class BestwayItem:
    def __init__(self, name, unit_size, b_price, rsp, por, pack_size, code, ean, vat_rate, brand, stock):
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
        self.stock = stock

    def commit_to_sql(self, mydb):

        # print("{0} [{1}, {2}, {3}, {4}]".format(self.name, self.b_price, self.rsp, self.ean, self.vat_rate))

        vat_val = 0.0
        if self.vat_rate == "Exempt":
            vat_val = 0.0
        elif self.vat_rate == "Standard":
            vat_val = 0.2
        elif self.vat_rate == "5%":
            vat_val = 0.05
        else:
            print("VAT RATE ERROR: [{0}]".format(self.vat_rate))

        rsp_formatted = float(self.rsp[1:])
        b_price_formatted = float(self.b_price[1:])

        broken_units = self.unit_size.split(" ")
        broken_units.pop(0)

        no_units = 1
        for num in broken_units:
            try:
                no_units = no_units * int(num)
            except:
                pass

        profit_overhead = (rsp_formatted * no_units) - b_price_formatted

        if profit_overhead == 0.0 or b_price_formatted == 0.0:
            profit_percent = 0.000
        else:
            profit_percent = (profit_overhead / b_price_formatted) * 100

        profit_percent = round(profit_percent, 2)

        por = str(self.por).replace("%", "")
        por = float(por)

        mycursor = mydb.cursor()

        sql = "INSERT INTO rrpextract (datetime, stockref, description, price, source, vat, por, packsize, 	" \
              "suppliercode, brand, in_stock, supplier_price, supplier_packsize, profit_percent) VALUES (NOW(), %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        vals = (self.ean, self.name, rsp_formatted, "BESTWAY", vat_val, por, self.pack_size, int(self.code), self.brand, self.stock, b_price_formatted, self.unit_size, profit_percent)

        mycursor.execute(sql, vals)
        mydb.commit()
