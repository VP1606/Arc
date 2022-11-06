import mysql.connector

cookies = {
    '.ASPXAUTH': '33CDC131F6B53F37F4CD7574642D835967A51D82D8A6590D9458E4A03B4E7A0865957038CCCDE8C81BF535CF43D10906E2E68CC5C5F753A1FFE61CB700FD9FF078ED772AF4E3BFA0D599EF6E357E59BDDAF20FA62473875654F8F4BABD6C07017C7BACFEFCC502ABC2364A2C04FC31B345A332373010DE4489159EA264C44AFC3FEF3C2B16CD024C200CED0B5908933933E9ACCB12F01ACD090D34668872344C',
    'QueueITAccepted-SDFrts345E-V3_prodqueue': 'EventId%3Dprodqueue%26QueueId%3D88ffb793-eb73-481b-8cfe-b9657295ca6a%26RedirectType%3Dsafetynet%26IssueTime%3D1667054608%26Hash%3D351d8fc58a1d03a30e5b20c3b19b256f4430564d3630c79245120c9cd827534f',
    '_dd_s': 'rum=2&id=98177935-9bbc-4705-94e1-a435824cc2e6&created=1667054607942&expire=1667056491415',
    'Trolley-ClickAndCollect': '4',
    'booker#lang': 'en',
    'Booker': 'CustomerNumber=Phfyvwx2Y4sXKstBV2PQqSKCVVti1OeNQ8Qd-4PozfUVznZRoHoeyx2tJ_NfXkPwMC7hCj4i_XrbP1uJwCf_jA2',
    'SC_ANALYTICS_GLOBAL_COOKIE': '3f4211037cf7465faddbb21ecca56654|False',
    'hasRepOrders': '0',
    'unseenRepOrders': '0',
    'ASP.NET_SessionId': 'bhgld4vdcqqjvjnu4febagnz',
    '_ga': 'GA1.3.63679729.1666875126',
    'CookieConsent': '{stamp:%27oJ35SLjkzW4RaUoGqC9nv0TjIDn9KP4raUYB5i2R9p0pT/40h2LtBg==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cver:1%2Cutc:1666875104776%2Cregion:%27gb%27}',
    'X-Mapping-janbeidc': '47F18F41A1C1358593CEE9E7CB55C663',
    '__RequestVerificationToken': 'XACfJyQWDMVZxFi6SrMR8ivsEpZKptICTqu9PlSglFldZCYGFzHH_JEHuSWM39s82i3kYEbcMjgUHasMcMTHw-QtFHNHUTdVczgVDHiiTF81',
}

headers = {
    # Requests sorts cookies= alphabetically
    # 'Cookie': '.ASPXAUTH=33CDC131F6B53F37F4CD7574642D835967A51D82D8A6590D9458E4A03B4E7A0865957038CCCDE8C81BF535CF43D10906E2E68CC5C5F753A1FFE61CB700FD9FF078ED772AF4E3BFA0D599EF6E357E59BDDAF20FA62473875654F8F4BABD6C07017C7BACFEFCC502ABC2364A2C04FC31B345A332373010DE4489159EA264C44AFC3FEF3C2B16CD024C200CED0B5908933933E9ACCB12F01ACD090D34668872344C; QueueITAccepted-SDFrts345E-V3_prodqueue=EventId%3Dprodqueue%26QueueId%3D88ffb793-eb73-481b-8cfe-b9657295ca6a%26RedirectType%3Dsafetynet%26IssueTime%3D1667054608%26Hash%3D351d8fc58a1d03a30e5b20c3b19b256f4430564d3630c79245120c9cd827534f; _dd_s=rum=2&id=98177935-9bbc-4705-94e1-a435824cc2e6&created=1667054607942&expire=1667056491415; Trolley-ClickAndCollect=4; booker#lang=en; Booker=CustomerNumber=Phfyvwx2Y4sXKstBV2PQqSKCVVti1OeNQ8Qd-4PozfUVznZRoHoeyx2tJ_NfXkPwMC7hCj4i_XrbP1uJwCf_jA2; SC_ANALYTICS_GLOBAL_COOKIE=3f4211037cf7465faddbb21ecca56654|False; hasRepOrders=0; unseenRepOrders=0; ASP.NET_SessionId=bhgld4vdcqqjvjnu4febagnz; _ga=GA1.3.63679729.1666875126; CookieConsent={stamp:%27oJ35SLjkzW4RaUoGqC9nv0TjIDn9KP4raUYB5i2R9p0pT/40h2LtBg==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cver:1%2Cutc:1666875104776%2Cregion:%27gb%27}; X-Mapping-janbeidc=47F18F41A1C1358593CEE9E7CB55C663; __RequestVerificationToken=XACfJyQWDMVZxFi6SrMR8ivsEpZKptICTqu9PlSglFldZCYGFzHH_JEHuSWM39s82i3kYEbcMjgUHasMcMTHw-QtFHNHUTdVczgVDHiiTF81',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.booker.co.uk',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Referer': 'https://www.booker.co.uk/products/product-list?categoryName=CS3_100001',
    'Connection': 'keep-alive',
}

mydb = mysql.connector.connect(
    host="netherly1.dyndns.org",
    user="mpos",
    password="mpospass",
    database="mpos"
)

import requests
from bs4 import BeautifulSoup
import get_item
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed


def search_ean(ean_pack, cookies, headers):
    url = "https://www.booker.co.uk/products/search?keywords={0}".format(ean_pack[0])
    page = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    main = soup.find_all("main", class_="list inner-list pb-md-2 px-0")[0]
    row = main.find_all("div", class_="rowMode")[0]

    row_block = row.find_all("div", class_="p-0 p-sm-0 product-list rowUnGrouped")[0]
    row_elements = row_block.findChildren("div", recursive=False)

    matched_row_el = None
    for row_el in row_elements:
        title = row_el.find_all("p", class_="product-name font-weight-bold mb-0")[0]
        if title.text.strip() == ean_pack[1]:
            matched_row_el = row_el
            break

    if matched_row_el is None:
        return ""

    else:
        rrp_full = ""
        rrp_possibles = matched_row_el.find_all("div", class_="price-row")
        for possible in rrp_possibles:
            span = possible.findChildren("span", recursive=False)[0]
            if "RRP: " in span.text:
                rrp_full = span.text
                break

        if rrp_full == "":
            return ""
        else:
            rsp = rrp_full.replace("RRP: £", "")
            rsp = float(rsp)
            if rsp > ean_pack[2]:
                # KEEP
                coll = matched_row_el.find_all("p", class_="product-name font-weight-bold mb-0")[0]
                link = coll["onclick"]
                link = link[33:]
                link = link[:-1]
                return link
            else:
                # DISCARD
                return ""


pack1 = ["5056025440470", "BrewDog Punk Post Modern Classic IPA 4 x 330ml", 6.49]
res1 = search_ean(pack1, cookies, headers)
#RES

pack2 = ["5000213026816", "Guinness Draught Stout Beer 4x440ml", 5.49]
res2 = search_ean(pack2, cookies, headers)
#NIL

pack3 = ["15099873103224", "Jack Daniel's Tennessee Whiskey & Cola 330 mL", 2.69]
res3 = search_ean(pack3, cookies, headers)
#NIL

pack4 = ["5054073069254", "Ace Cider Crisp & Refreshing Apple Cider 2.5 Litres", 5.19]
res4 = search_ean(pack4, cookies, headers)
#NIL

ress = [res1, res2, res3, res4]
for res in ress:
    if res != "":
        print("RES")
    else:
        print("NIL")