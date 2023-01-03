from get_all_cat_threaded import *


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
        return "", False, False, False

    else:
        rrp_full = ""
        rrp_possibles = matched_row_el.find_all("div", class_="price-row")
        for possible in rrp_possibles:
            span = possible.findChildren("span", recursive=False)[0]
            if "RRP: " in span.text:
                rrp_full = span.text
                break

        if rrp_full == "":
            return "", True, False, False
        else:
            rsp = rrp_full.replace("RRP: £", "")
            rsp = float(rsp)
            if rsp > ean_pack[2]:
                # KEEP
                coll = matched_row_el.find_all("p", class_="product-name font-weight-bold mb-0")[0]
                link = coll["onclick"]
                link = link[33:]
                link = link[:-1]
                return link, True, True, True
            else:
                # DISCARD
                return "", True, True, False


def do_by_search(ean_book, cookies, headers, mydbs):
    threads = []
    target_book = []
    item_book = []

    search_stats = [0, 0, 0]

    with alive_bar(len(ean_book), title="Scanning EAN Book", force_tty=True) as bar:
        with ThreadPoolExecutor(max_workers=5) as executor:
            for ean_pack in ean_book:
                if type(ean_pack) == list:
                    threads.append(executor.submit(search_ean, ean_pack, cookies, headers))
                else:
                    bar()
                    pass
            for task in as_completed(threads):

                link, found, found_rrp, better_rrp = task.result()

                if found:
                    search_stats[0] = search_stats[0] + 1
                if found_rrp:
                    search_stats[1] = search_stats[1] + 1
                if better_rrp:
                    search_stats[2] = search_stats[2] + 1

                if link == "":
                    bar()
                else:
                    target_book.append(link)
                    bar()

    threads = []
    with alive_bar(len(target_book), title="Building Items", force_tty=True) as bar:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for link in target_book:
                threads.append(executor.submit(build_item, link, cookies, headers))
            for task in as_completed(threads):
                item_book = item_book + task.result()
                bar()

    with alive_bar(len(target_book), title="Committing to SQL", force_tty=True) as bar:
        for el in item_book:
            for mydb in mydbs:
                sql_committing(el, cookies, headers, mydb)
            bar()

    print("Finish STATS; Found: {0}, Found w/ RRP: {1}, Found w/ Better RRP: {2}.".format(search_stats[0],
                                                                                          search_stats[1],
                                                                                          search_stats[2]))
