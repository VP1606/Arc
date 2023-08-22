from fastapi import FastAPI, Depends
from fastapi.responses import Response, FileResponse
from bestway_handler import bestway_collector, bestway_login
from booker_handler import booker_collector
from parfetts_handler import parfetts_collector, parfetts_login
import json
import cookie_jar
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sql_save import process_results as sql_process
from extract_search import extract_search_main

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

bestway_driver = bestway_login()
def get_bestway_driver():
    return bestway_driver

parfetts_driver = parfetts_login()
def get_parfetts_driver():
    return parfetts_driver

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(Path("static/favicon.ico"))

@app.get("/")
async def read_main():
    html_file_path = Path("static/mainpage.html")
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
async def search_all(id: str, ean: str, product_name: str, bw_driver = Depends(get_bestway_driver), p_driver = Depends(get_parfetts_driver)):
    if pub_id == id:
        search_name = product_name
        main_res = {}

        try:
            bestway_result = bestway_collector(ean=ean, driver=bw_driver)
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
            parfetts_result = parfetts_collector(ean=ean, name=search_name, driver=p_driver)
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

@app.on_event("shutdown")
async def shutdown_event():
    bestway_driver.quit()
    parfetts_driver.quit()
