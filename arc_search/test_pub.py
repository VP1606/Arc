from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
pub_id = "iahfiasfdosai2313212**7613"

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_main():
    html_file_path = Path("static/mainpage.html")
    return FileResponse(html_file_path)