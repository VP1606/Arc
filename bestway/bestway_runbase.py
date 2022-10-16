import mysql.connector
import get_all_cat

cookies = {
    'unbxd_depot': '834',
    'fulfilment_msg_shown': '1',
    'selected_fulfilment': 'C',
    'access_token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5iZXN0d2F5LmNvLnVrLyJ9..c5nZdBspBB3LA2LG.K2TuhACUbxtEZzMcZBDc8Aw1e2nJse7z_bhH1cdmKrCx2vuFoEIgGp6ByBE055DXE27TaEcTW-xASaezF6cWHMqsbf693L8rgd-VRAI-TLs10Zrycz01mUlQMcKvYTkA5rSRna-6-xcX6_ByIHGHNiblBbcC53Ens4Pc3lwCgAlz_oeMvN5D0-PFQyX_C6y13Ml1eL7YhuEI3qh8bJuIJF97-hOMkurS0E-a_oNGEuRHBCnJQT1fqiD7sjhqaHyK2t7AwuVI2Z14RO2bQLe-FktsBo-1eele.umtBx525ldtQCwEAsRiEfg',
    'PHPSESSID': 'bjicls9m42h4101ffmi1b5vj3j',
    'SERVERID': 'web-01',
    'CookieControl': '{"necessaryCookies":["unbxd.visit","unbxd_depot","auth0_check","SERVERID"],"optionalCookies":{},"statement":{},"consentDate":1665689729577,"consentExpiry":365,"interactedWith":true,"user":"52D4A084-DB4A-45B0-9E3F-0C11F860557D"}',
}

headers = {
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'unbxd_depot=834; fulfilment_msg_shown=1; selected_fulfilment=C; access_token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5iZXN0d2F5LmNvLnVrLyJ9..c5nZdBspBB3LA2LG.K2TuhACUbxtEZzMcZBDc8Aw1e2nJse7z_bhH1cdmKrCx2vuFoEIgGp6ByBE055DXE27TaEcTW-xASaezF6cWHMqsbf693L8rgd-VRAI-TLs10Zrycz01mUlQMcKvYTkA5rSRna-6-xcX6_ByIHGHNiblBbcC53Ens4Pc3lwCgAlz_oeMvN5D0-PFQyX_C6y13Ml1eL7YhuEI3qh8bJuIJF97-hOMkurS0E-a_oNGEuRHBCnJQT1fqiD7sjhqaHyK2t7AwuVI2Z14RO2bQLe-FktsBo-1eele.umtBx525ldtQCwEAsRiEfg; PHPSESSID=bjicls9m42h4101ffmi1b5vj3j; SERVERID=web-01; CookieControl={"necessaryCookies":["unbxd.visit","unbxd_depot","auth0_check","SERVERID"],"optionalCookies":{},"statement":{},"consentDate":1665689729577,"consentExpiry":365,"interactedWith":true,"user":"52D4A084-DB4A-45B0-9E3F-0C11F860557D"}',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.bestwaywholesale.co.uk',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Referer': 'https://www.bestwaywholesale.co.uk/product/656016-1',
    'Connection': 'keep-alive',
}

mydb = mysql.connector.connect(
    host="netherly1.dyndns.org",
    user="mpos",
    password="mpospass",
    database="mpos"
)

import time
import get_all_cat_threaded

# start_1 = time.time()
# get_all_cat.Upload_Category("soft-drinks", cookies, headers, mydb)
# finish_1 = time.time()

start_2 = time.time()
get_all_cat_threaded.do_cat_threaded("soft-drinks", cookies, headers, mydb)
finish_2 = time.time()


# print("SINGLE THREAD: {0}".format(str(finish_1 - start_1)))
print("MULTI 20 THREAD: {0}".format(str(finish_2 - start_2)))