import mysql.connector
import get_all_cat_threaded
import get_cats
import time
import get_by_search_threaded
import json
import sys
import os

#https://curlconverter.com
cookies = {
    '_dd_s': 'rum=2&id=3f6033b8-3443-4968-bd2c-bded9f4e3dea&created=1722434687857&expire=1722435856799',
    '.ASPXAUTH': '2A08413FCE9180612097B204333237E52944CDEC723FD2AF79D9E2564DCF2B477CD8A42671F3A4F81975ED06935D7C34D1C1CCB21E4987A9EAC95B4D47347278E48C19DC59C08D0743C673D35090564F15F22B5962E758E3AAAD63FB1F4DBFF6E7A26A0F567A7B407A422EC7E2A825F33762FC1FE1ED07CC40B693C13C0C269BD1EEDC3F41FF66A0E0F36CF1BFF01445A41A1637AEAD8C86ED652C679594B31C',
    'Booker': 'CustomerNumber=HJ9igjKkM9f-8U6wsleIlSQXEnRNCzJF7FuDO9fyLNJfRDES6oglT85EfQvcmM2oO6gil_K0O1433LnGYZwNSA2',
    'QueueITAccepted-SDFrts345E-V3_prodqueue': 'EventId%3Dprodqueue%26QueueId%3D8c5de78d-2f63-4d8e-9d82-57f523dfde1c%26RedirectType%3Dsafetynet%26IssueTime%3D1722434689%26Hash%3D2d7a008d02074b7e01df169d00ef5ddf5db6abee0d40665408d07857c4efcea6',
    'ScannerID': '0f9ac8f1e0db4c72a17a50086fd38f81',
    'Trolley-ClickAndCollect': '5031',
    'activetrolley': 'ClickAndCollect',
    'hasRepOrders': '0',
    'unseenRepOrders': '0',
    'ASP.NET_SessionId': 'x0xzzhi2j52krr5ptvsyb2cd',
    'SC_ANALYTICS_GLOBAL_COOKIE': 'f7d4ffc0f8b742218fcb0b23f7abfe47|False',
    'shell#lang': 'en',
    'CookieConsent': '{stamp:%27n6cuJdYIUNwbjixVQ3kz03HRxlrU67pOZdY/uQEqcseAm7sk15YIDg==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1722434686946%2Cregion:%27gb%27}',
    'X-Mapping-pkbognpo': '9772CA94F76529C66119B65082B41600',
    '__RequestVerificationToken': 'OHpZmI17RgJk6ru-jY0JnAvS-EU7mwztwwwfikMls6jzTcX-z-smQWot0fYE-rx_wmPHAmJ71DA9B6VTlj34wVyoQaY6Jxp7Q4_i7FMMceU1',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    # 'Cookie': '_dd_s=rum=2&id=3f6033b8-3443-4968-bd2c-bded9f4e3dea&created=1722434687857&expire=1722435856799; .ASPXAUTH=2A08413FCE9180612097B204333237E52944CDEC723FD2AF79D9E2564DCF2B477CD8A42671F3A4F81975ED06935D7C34D1C1CCB21E4987A9EAC95B4D47347278E48C19DC59C08D0743C673D35090564F15F22B5962E758E3AAAD63FB1F4DBFF6E7A26A0F567A7B407A422EC7E2A825F33762FC1FE1ED07CC40B693C13C0C269BD1EEDC3F41FF66A0E0F36CF1BFF01445A41A1637AEAD8C86ED652C679594B31C; Booker=CustomerNumber=HJ9igjKkM9f-8U6wsleIlSQXEnRNCzJF7FuDO9fyLNJfRDES6oglT85EfQvcmM2oO6gil_K0O1433LnGYZwNSA2; QueueITAccepted-SDFrts345E-V3_prodqueue=EventId%3Dprodqueue%26QueueId%3D8c5de78d-2f63-4d8e-9d82-57f523dfde1c%26RedirectType%3Dsafetynet%26IssueTime%3D1722434689%26Hash%3D2d7a008d02074b7e01df169d00ef5ddf5db6abee0d40665408d07857c4efcea6; ScannerID=0f9ac8f1e0db4c72a17a50086fd38f81; Trolley-ClickAndCollect=5031; activetrolley=ClickAndCollect; hasRepOrders=0; unseenRepOrders=0; ASP.NET_SessionId=x0xzzhi2j52krr5ptvsyb2cd; SC_ANALYTICS_GLOBAL_COOKIE=f7d4ffc0f8b742218fcb0b23f7abfe47|False; shell#lang=en; CookieConsent={stamp:%27n6cuJdYIUNwbjixVQ3kz03HRxlrU67pOZdY/uQEqcseAm7sk15YIDg==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1722434686946%2Cregion:%27gb%27}; X-Mapping-pkbognpo=9772CA94F76529C66119B65082B41600; __RequestVerificationToken=OHpZmI17RgJk6ru-jY0JnAvS-EU7mwztwwwfikMls6jzTcX-z-smQWot0fYE-rx_wmPHAmJ71DA9B6VTlj34wVyoQaY6Jxp7Q4_i7FMMceU1',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.booker.co.uk/login',
    'Sec-Fetch-Mode': 'navigate',
    'Host': 'www.booker.co.uk',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Connection': 'keep-alive',
}

home_db_address = str(os.environ.get("HOME_SQL"))
mydbs = [mysql.connector.connect(
        host=home_db_address,
        user="mpos",
        password="mpospass",
        database="mpos"
    )]

def RUN():
    print("------BOOKER------")
    start_time = time.time()
    cats = get_cats.get_cats(cookies, headers)
    print("Total Cycles to be executed: {0}".format(len(cats)))
    for index, cat in enumerate(cats):
        print("Cycle No. {0}".format(index + 1))
        get_all_cat_threaded.do_cat_threaded(cat, cookies, headers, mydbs)

    end_time = time.time()
    print("-----------------------")
    print("Duration: {0}".format(end_time - start_time))


def RUN_Test():
    print("------BOOKER------")
    print("-----TESTMODE-----")
    cats = get_cats.get_cats(cookies, headers)
    print("Running Index 1...")
    cat = cats[1]
    get_all_cat_threaded.do_cat_threaded(cat, cookies, headers, mydbs)
    print("-----------------------")


def RUN_by_search():
    print("------BOOKER BY SEARCH------")
    start_time = time.time()
    file = open("../temp/ean_list.json", "r")
    ean_book = json.loads(file.read())
    file.close()

    print("Total Cycles to be executed: {0}".format(len(ean_book)))

    get_by_search_threaded.do_by_search(ean_book, cookies, headers, mydbs)

    end_time = time.time()
    print("-----------------------")
    print("Duration: {0}".format(end_time - start_time))


args = sys.argv
by_search = False

for arg in args:
    if arg == "-bs":
        by_search = True

if by_search:
    RUN_by_search()
else:
    RUN()