from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from extract_search import search_by_name, search_by_ean
import mysql.connector
import json

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

@app.get("/")
async def read_main():
    html_file_path = Path("static/mainpage.html")
    return FileResponse(html_file_path)

@app.get("/search_ean")
async def search_ean(id: str, query: str):
    if pub_id == id:
        try:
            res = search_by_ean(mydb=mydb, query=query)
            return Response(content=json.dumps(res), media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
    
@app.get("/search_name")
async def search_name(id: str, query: str):
    if pub_id == id:
        try:
            res = search_by_name(mydb=mydb, query=query)
            return Response(content=json.dumps(res), media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
    
@app.on_event("shutdown")
async def shutdown_event():
    mydb.close()