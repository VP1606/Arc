from flask import Flask, request, send_file
import compare_reader as cr
import get_date as gd
import price_submitter as ps

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