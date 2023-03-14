from flask import Flask, request, send_file
import compare_reader as cr
import get_date as gd
import price_submitter as ps
import desc_update as du
import update_products as up

app = Flask(__name__)
pub_id = "iahfiasfdosai2313212**7613"


@app.route("/price_list")
def price_list():
    id = request.args.get("id")
    target = request.args.get("target")
    if pub_id == id:
        result = cr.local_generator(str(target))
        return result


@app.route("/get_update_date")
def get_update_date():
    return gd.get_date("milecross.dyndns.org")


@app.route("/test")
def test():
    return "TEST!"


@app.route("/update_price")
def update_price():
    target = request.args.get("target")
    stockref = request.args.get("stockref")
    price = float(request.args.get("price"))

    ps.price_upload(target, stockref, price)


@app.route("/update_desc")
def update_desc():
    id = request.args.get("id")
    if pub_id == id:
        desc = request.args.get("desc")
        stockref = request.args.get("ean")
        address = request.args.get("address")

        du.update_desc(desc, address, stockref)


@app.route("/get_plist")
def get_plist():
    id = request.args.get("id")
    if pub_id == id:
        target = request.args.get("target")
        result = up.get_all_products(target)
        return result