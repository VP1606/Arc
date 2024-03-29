import requests
from bs4 import BeautifulSoup

def get_cats(cookies, headers):
    cats = []

    url = "https://www.booker.co.uk/products/categories"
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    cat_collection = soup.find_all("div", class_="departments")[0]
    cat_refs = cat_collection.find_all("a", class_="departmentItemx")

    for ref in cat_refs:
        cats.append(ref["href"])

    return cats

