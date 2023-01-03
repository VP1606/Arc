import mysql.connector
import get_all_cat_threaded
import get_cats
import json
import sys

cookies_raw = {
    'unbxd_depot': '834',
    'fulfilment_msg_shown': '1',
    'selected_fulfilment': 'C',
    'access_token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5iZXN0d2F5LmNvLnVrLyJ9..JyyZ9YTEzZ3gexXr.usUi1BxPPPjE4CzUfzSSU3L8AevMphTACFXRzjMdHA1qzHGRu9ixn7UbXnXkaH7-fMrTQUPC9rpqm0qihL7l3ZSm8nKtaB4JgTNQf0_Now_Lso56dj_5UCe9eZesPLt-oC441eC4QwRyXrkwwakR-6idNrkTFOd42prfFNo0CNlQzKvwiWOMZjIrZ5YVYgXHixoN9g0KgXDrb3DKVL98DJOrrOVUTYpc4OFGyEydOU2RtfFBufD9JlIkCo-1pHxNkroZbRLKvNMdGHrbhtshO8sjdnIz_lV7.oh5ZYtrJ3Db6fmaeLUdK5A',
    'PHPSESSID': '83qfol103tlcf2nshaiugob4bu',
    'SERVERID': 'web-01',
    'auth0_check': 'Y',
    'sso_token_wholesale': 'c5u2lgs7rw0s40kgoo4g4sk8c',
    'CookieControl': '{"necessaryCookies":["unbxd.visit","unbxd_depot","auth0_check","SERVERID"],"optionalCookies":{},"statement":{},"consentDate":1665689729577,"consentExpiry":365,"interactedWith":true,"user":"52D4A084-DB4A-45B0-9E3F-0C11F860557D"}',
}

headers_raw = {
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'unbxd_depot=834; fulfilment_msg_shown=1; selected_fulfilment=C; access_token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5iZXN0d2F5LmNvLnVrLyJ9..JyyZ9YTEzZ3gexXr.usUi1BxPPPjE4CzUfzSSU3L8AevMphTACFXRzjMdHA1qzHGRu9ixn7UbXnXkaH7-fMrTQUPC9rpqm0qihL7l3ZSm8nKtaB4JgTNQf0_Now_Lso56dj_5UCe9eZesPLt-oC441eC4QwRyXrkwwakR-6idNrkTFOd42prfFNo0CNlQzKvwiWOMZjIrZ5YVYgXHixoN9g0KgXDrb3DKVL98DJOrrOVUTYpc4OFGyEydOU2RtfFBufD9JlIkCo-1pHxNkroZbRLKvNMdGHrbhtshO8sjdnIz_lV7.oh5ZYtrJ3Db6fmaeLUdK5A; PHPSESSID=83qfol103tlcf2nshaiugob4bu; SERVERID=web-01; auth0_check=Y; sso_token_wholesale=c5u2lgs7rw0s40kgoo4g4sk8c; CookieControl={"necessaryCookies":["unbxd.visit","unbxd_depot","auth0_check","SERVERID"],"optionalCookies":{},"statement":{},"consentDate":1665689729577,"consentExpiry":365,"interactedWith":true,"user":"52D4A084-DB4A-45B0-9E3F-0C11F860557D"}',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.bestwaywholesale.co.uk',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Referer': 'https://www.bestwaywholesale.co.uk/shop',
    'Connection': 'keep-alive',
}

mydbs = [mysql.connector.connect(
        host="milecross.dyndns.org",
        user="mpos",
        password="mpospass",
        database="mpos"
    ), mysql.connector.connect(
        host="netherly1.dyndns.org",
        user="mpos",
        password="mpospass",
        database="mpos"
    ), mysql.connector.connect(
        host="runcorn.dyndns.org",
        user="mpos",
        password="mpospass",
        database="mpos"
    ), mysql.connector.connect(
        host="rathbone.dyndns.org",
        user="mpos",
        password="mpospass",
        database="mpos"
    ),
    mysql.connector.connect(
        host="breezehill1.dyndns.org",
        user="mpos",
        password="mpospass",
        database="mpos"
    )]


def RUN(cookies, headers, generate_ean_list=False, collect_pricing=True):
    if generate_ean_list:
        print("--------BESTWAY START EAN--------")
    else:
        print("--------BESTWAY START--------")

    if collect_pricing is False:
        print("Pricing Disabled!")
        cookies = None
        headers = None

    cats = get_cats.get_cats(cookies, headers)
    ean_list = []
    for index, cat in enumerate(cats):
        print(index)
        ean_list = ean_list + get_all_cat_threaded.do_cat_threaded(cat, cookies, headers, mydbs, generate_ean_list, collect_pricing)


    if generate_ean_list is True:
        ean_json = json.dumps(ean_list)
        ean_file = open("../temp/ean_list.json", "w")
        ean_file.write(ean_json)
        ean_file.close()

    print("--------BESTWAY DONE--------")


def RUN_Test(cookies, headers):
    print("--------BESTWAY START--------")
    print("----------TEST MODE----------")
    cats = get_cats.get_cats(cookies, headers)
    cat = cats[2]
    print("Running off Index 2...")
    get_all_cat_threaded.do_cat_threaded(cat, cookies, headers, mydbs, False, False)
    print("--------BESTWAY DONE--------")


args = sys.argv
generate_ean = False
collect_pricing = True

for arg in args:
    if arg == "-ge":
        generate_ean = True
    if arg == "-spd":
        collect_pricing = False

RUN(cookies=cookies_raw, headers=headers_raw, generate_ean_list=generate_ean, collect_pricing=collect_pricing)