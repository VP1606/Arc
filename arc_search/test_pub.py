from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from extract_search import extract_search_main
import mysql.connector
import json
import basket_operator

mydb = mysql.connector.connect(
        host="192.168.1.180",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

app = FastAPI()
pub_id = "iahfiasfdosai2313212**7613"

app.mount("/static", StaticFiles(directory="static"), name="static")

res_unavailable_message = json.dumps({
    "status": "expected",
    "message": "Item Not Found (from PUB)"
})

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(Path("static/favicon.ico"))

@app.get("/")
async def read_main():
    html_file_path = Path("static/mainpage.html")
    return FileResponse(html_file_path)

@app.get("/search_ean")
async def search_ean(id: str, query: str):
    if pub_id == id:
        try:
            res = extract_search_main(mydb=mydb, query=query, mode="ean")
            return Response(content=json.dumps(res), media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
    
@app.get("/search_name")
async def search_name(id: str, query: str):
    if pub_id == id:
        try:
            res = extract_search_main(mydb=mydb, query=query, mode="name")
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

@app.on_event("shutdown")
async def shutdown_event():
    mydb.close()