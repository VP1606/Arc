from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from extract_search import extract_search_main
import mysql.connector
import json
import basket_operator
import time
import user_manager.otp_handler as otp_handler
import user_manager.user_handler

# NAME TIME: 0.030276060104370117

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
    # html_file_path = Path("static/mainpage.html")
    html_file_path = Path("static/UI2/homepage.html")
    # html_file_path = Path("static/basket_mode/basket_element.html")
    # html_file_path = Path("static/barcode_scan/scan_interface.html")
    # html_file_path = Path("static/login/login_page.html")
    return FileResponse(html_file_path)

@app.get("/login/verify_otp")
async def verify_otp(user_id: str, otp: str):
    res = otp_handler.check_otp(user_id=int(user_id), code=int(otp))
    return Response(content=json.dumps(res), media_type="application/json")

@app.get("/login/get_users")
async def get_users():
    res = user_manager.user_handler.fetch_users()
    return Response(content=json.dumps(res), media_type="application/json") 

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
    
@app.get("/search_name")
async def search_name(id: str, query: str):
    if pub_id == id:
        try:
            start = time.time()
            res = extract_search_main(query=query, mode="name")
            end = time.time()
            print(f"NAME TIME (NS): {end - start}")
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
    # mydb.close()
    pass