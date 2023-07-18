from fastapi import FastAPI
from fastapi.responses import Response
from bestway_handler import bestway_collector

app = FastAPI()
pub_id = "iahfiasfdosai2313212**7613"
# search_bestway?id=iahfiasfdosai2313212**7613&ean=815941-1

@app.get("/test")
async def test():
    return Response(content='TEST AST!', media_type="application/json")

@app.get("/search_bestway")
async def search_bestway(id: str, ean: str):
    if pub_id == id:
        result = bestway_collector(product_code=ean)
        return Response(content=result, media_type="application/json")
    else:
        return Response(content='False', media_type="application/json")
