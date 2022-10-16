import requests
from bs4 import BeautifulSoup


def get_cats(cookies, headers):
    cats = []

    url = 'https://www.bestwaywholesale.co.uk'
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    main_bar = soup.find(id="mainmenu")
    main_ul = main_bar.find_all("ul")[0]

    main_lis = main_ul.find_all("li", recursive=False)
    for li in main_lis:
        a_targ = li.find_all("a")[0]
        link = a_targ["href"]
        cats.append(link[1:])

    return cats
