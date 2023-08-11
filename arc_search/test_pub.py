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