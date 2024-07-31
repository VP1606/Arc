import mysql.connector
import get_all_cat_threaded
import get_cats
import os
import multiprocessing

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
        host="192.168.1.172",
        user="mpos",
        password="mpospass",
        database="mpos"
    )]

def split_array_in_half(arr):
    midpoint = len(arr) // 2
    first_half = arr[:midpoint]
    second_half = arr[midpoint:]
    return first_half, second_half

def RUN(cats, cookies, headers, generate_ean_list=False, collect_pricing=True):
    print(f"--------BESTWAY START PID {os.getpid()}--------")
    
    ean_list = []
    for index, cat in enumerate(cats):
        print(index)
        ean_list = ean_list + get_all_cat_threaded.do_cat_threaded(cat, cookies, headers, mydbs, generate_ean_list, collect_pricing)

    print(f"--------BESTWAY DONE PID {os.getpid()}--------")
    return

if __name__ == "__main__":
    print("ID of main process: {}".format(os.getpid()))
    
    cats = get_cats.get_cats(cookies_raw, headers_raw)
    cats_p1, cats_p2 = split_array_in_half(cats)
    
    p1 = multiprocessing.Process(target=RUN, args=(cats_p1, cookies_raw, headers_raw, False, True))
    p2 = multiprocessing.Process(target=RUN, args=(cats_p2, cookies_raw, headers_raw, False, True))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print("Main Complete")
