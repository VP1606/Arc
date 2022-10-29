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

import requests
from bs4 import BeautifulSoup

link = "https://www.booker.co.uk/products/product%20detail?Code=275138&returnUrl=http%3a%2f%2fwww.booker.co.uk" \
       "%2fproducts%2fproduct-list%3fcategoryName%3dCS3_100001%26view%3dUnGrouped%26sortField%3dPromotion" \
       "%26SortDirection%3dAscending%26sortOrder%3d%26multi%3dFalse%26pageIndex%3d0 "

code = "/products/product%20detail?Code=275138&returnUrl=http%3a%2f%2fwww.booker.co.uk" \
       "%2fproducts%2fproduct-list%3fcategoryName%3dCS3_100001%26view%3dUnGrouped%26sortField%3dPromotion" \
       "%26SortDirection%3dAscending%26sortOrder%3d%26multi%3dFalse%26pageIndex%3d0"

page = requests.get(link, cookies=cookies, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

# fields = soup.find_all("span", class_="font-weight-bold")
# brand = ""
# for el in fields:
#     if el.text == "Brand ":
#         neext = el.find_next_sibling()
#         brand = neext.text
#         break
# print(brand)

import get_item
get_item.GET_ITEM(code, cookies, headers)