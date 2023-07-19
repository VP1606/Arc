from fastapi import FastAPI
from fastapi.responses import Response
from bestway_handler import bestway_collector
from booker_handler import booker_collector
import json

app = FastAPI()
pub_id = "iahfiasfdosai2313212**7613"

res_unavailable_message = json.dumps({
    "status": "expected",
    "message": "Item Not Found (from PUB)"
})

# search_bestway?id=iahfiasfdosai2313212**7613&ean=815941-1
# ean_pack = ['5012035962609', 'HARIBO Tangfastics Bag 160g', 2.3]
# /products/product detail?Code=260459&returnUrl=http%3a%2f%2fwww.booker.co.uk%2fproducts%2fsearch%3fkeywords%3d5012035962609

# NOTE: Bestway's Product Code is NOT the EAN.
# NOTE: Booker search requires item name!

@app.get("/test")
async def test():
    return Response(content='TEST AST!', media_type="application/json")

@app.get("/search_bestway")
async def search_bestway(id: str, ean: str):
    if pub_id == id:
        try:
            result = bestway_collector(ean=ean)
            return Response(content=result, media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
    
@app.get("/search_booker")
async def search_booker(id: str, ean: str, product_name: str):
    if pub_id == id:
        try:
            result = booker_collector(ean=ean, product_name=product_name)
            return Response(content=result, media_type="application/json")
        except:
            return Response(content=res_unavailable_message, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")