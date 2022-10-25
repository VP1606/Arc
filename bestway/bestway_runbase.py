import mysql.connector
import get_all_cat
import get_all_cat_threaded
import get_cats

cookies = {
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

headers = {
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

mydb = mysql.connector.connect(
    host="netherly1.dyndns.org",
    user="mpos",
    password="mpospass",
    database="mpos"
)


def RUN(multi=True):
    cats = get_cats.get_cats(cookies, headers)
    for index, cat in enumerate(cats):
        print(index)
        if multi:
            get_all_cat_threaded.do_cat_threaded(cat, cookies, headers, mydb)
        else:
            get_all_cat.Upload_Category(cat, cookies, headers, mydb)

def test():
    cats = get_cats.get_cats(cookies, headers)
    for index, cat in enumerate(cats):
        print(index)
        get_all_cat_threaded.do_cat_threaded(cat, cookies, headers, mydb)

RUN()