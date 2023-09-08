from fastapi import FastAPI, Depends
from fastapi.responses import Response, FileResponse
from bestway_handler import bestway_collector, bestway_login, generate_bestway_drivers
from booker_handler import booker_collector
from parfetts_handler import parfetts_collector, parfetts_login, generate_parfetts_drivers
import json
import cookie_jar
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sql_save import process_results as sql_process
from extract_search import extract_search_main
import basket_operator
from user_manager import otp_handler
import user_manager.user_handler

app = FastAPI()
pub_id = "iahfiasfdosai2313212**7613"

app.mount("/static", StaticFiles(directory="static"), name="static")

res_unavailable_message = json.dumps({
    "status": "expected",
    "message": "Item Not Found (from PUB)"
})

# search_bestway?id=iahfiasfdosai2313212**7613&ean=815941-1
# ean_pack = ['5012035962609', 'HARIBO Tangfastics Bag 160g', 2.3]
# /products/product detail?Code=260459&returnUrl=http%3a%2f%2fwww.booker.co.uk%2fproducts%2fsearch%3fkeywords%3d5012035962609

# NOTE: Booker search requires item name!

bestway_drivers = generate_bestway_drivers()
def get_bestway_drivers():
    return bestway_drivers

parfetts_drivers = generate_parfetts_drivers()
def get_parfetts_drivers():
    return parfetts_drivers

def quit_drivers(collection: dict):
    for key in collection:
        if collection[key] is not None:
            collection[key].quit()

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(Path("static/favicon.ico"))

@app.get("/")
async def read_main():
    html_file_path = Path("static/login/login_page.html")
    return FileResponse(html_file_path)

@app.get("/test")
async def test():
    return Response(content='TEST AST!', media_type="application/json")

@app.get("/search_bestway")
async def search_bestway(id: str, ean: str):
    if pub_id == id:
        try:
            result = bestway_collector(ean=ean)
            return Response(content=json.dumps(result), media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
    
@app.get("/search_booker")
async def search_booker(id: str, ean: str, product_name: str):
    if pub_id == id:
        try:
            result = booker_collector(ean=ean, product_name=product_name)
            return Response(content=json.dumps(result), media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
    
@app.get("/search_parfetts")
async def search_parfetts(id: str, ean: str, product_name: str=""):
    if pub_id == id:
        try:
            result = parfetts_collector(ean=ean, name=product_name)
            return Response(content=json.dumps(result), media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
    
@app.get("/search_all")
async def search_all(id: str, ean: str, product_name: str, key_id: str, bw_drivers = Depends(get_bestway_drivers), p_drivers = Depends(get_parfetts_drivers)):
    if pub_id == id:
        search_name = product_name
        main_res = {}

        keyID = int(key_id)

        try:
            bestway_result = bestway_collector(ean=ean, driver=bw_drivers[keyID])
            search_name = bestway_result["item_name"]
            main_res["bestway"] = bestway_result
        except:
            main_res["bestway"] = cookie_jar.res_unavailable_message
        
        try:
            booker_result = booker_collector(ean=ean, product_name=search_name)
            main_res["booker"] = booker_result
        except:
            main_res["booker"] = cookie_jar.res_unavailable_message

        try:
            parfetts_result = parfetts_collector(ean=ean, name=search_name, driver=p_drivers[keyID])
            main_res["parfetts"] = parfetts_result
        except:
            main_res["parfetts"] = cookie_jar.res_unavailable_message

        sql_process(results=main_res)
        return Response(content=json.dumps(main_res), media_type="application/json")

    else:
        return Response(content='False', media_type="application/json")
    
@app.get("/search_name")
async def search_name(id: str, query: str):
    if pub_id == id:
        try:
            res = extract_search_main(query=query, mode="name")
            return Response(content=json.dumps(res), media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
    
@app.get("/search_ean")
async def search_ean(id: str, query: str):
    if pub_id == id:
        try:
            res = extract_search_main(query=query, mode="ean")
            return Response(content=json.dumps(res), media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
    
@app.get("/operate_basket")
async def operate_basket(id: str, key: str):
    if key == "keyword" and id == pub_id:
        try:
            res = basket_operator.run_wrapper()
            return Response(content=json.dumps(res), media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content=json.dumps(False), media_type="application/json")
    
@app.get("/login/verify_otp")
async def verify_otp(user_id: str, otp: str):
    res = otp_handler.check_otp(user_id=int(user_id), code=int(otp))
    return Response(content=json.dumps(res), media_type="application/json")

@app.get("/login/get_users")
async def get_users():
    res = user_manager.user_handler.fetch_users()
    return Response(content=json.dumps(res), media_type="application/json") 

@app.on_event("shutdown")
async def shutdown_event():
    quit_drivers(bestway_drivers)
    quit_drivers(parfetts_drivers)
