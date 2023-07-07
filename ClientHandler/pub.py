import compare_reader as cr
import get_date as gd
import price_submitter as ps
import desc_update as du
import update_products as up

from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()
pub_id = "iahfiasfdosai2313212**7613"


@app.get("/price_list")
async def price_list(id: str, target: str):
    if pub_id == id:
        result = cr.local_generator(str(target))
        return Response(content=result, media_type="application/json")


@app.get("/get_update_date")
async def get_update_date():
    ret = gd.get_date("milecross.dyndns.org")
    return Response(content=ret, media_type="application/json")


@app.get("/test")
async def test():
    return Response(content='TEST!', media_type="application/json")


@app.get("/update_price")
async def update_price(id: str, target: str, stockref: str, price: str):
    if pub_id == id:
        _price = float(price)
        ps.price_upload(target, stockref, _price)
    return Response(content='True', media_type="application/json")


@app.get("/update_desc")
async def update_desc(id: str, desc: str, stockref: str, address: str):
    if pub_id == id:
        du.update_desc(desc, address, stockref)
        return Response(content='True', media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")


@app.get("/get_plist")
async def get_plist(id: str, target: str, period: str):
    if pub_id == id:
        if period is None or period == "":
            period = "100"
        result = up.get_all_products(target, period)
        return Response(content=result, media_type="application/json")


@app.get("/get_rrplist")
async def get_rrp_list(id: str, target: str):
    if pub_id == id:
        result = up.get_all_rrps(target)
        return Response(content=result, media_type="application/json")
