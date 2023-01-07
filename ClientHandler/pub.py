from flask import Flask, request, send_file
import compare_reader as cr
import get_date as gd

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
