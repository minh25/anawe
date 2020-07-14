import threading
import queue
from time import time

from pymongo import MongoClient, UpdateOne

from soup_of_url import soup_of_url
import analyze_a_product

# declare mongodb
db = MongoClient("mongodb+srv://giftza:giftza@cluster0.qquas.mongodb.net/test?retryWrites=true&w=majority").test

# product filter
tags = ['family-gift',
        'Relationship',
        'special-gifts',
        'mother-s-day',
        'father-s-day',
        'Holidays%20&%20Events']
department = ['men',
              'women',
              'youth',
              'assessories',
              'housewares']
product = ['shirt',
           'hoodie',
           'hat',
           'case',
           'sweatshirt',
           'longsleeve',
           'tanktop',
           'mug',
           'poster',
           'pillowcase',
           'blanket',
           'pillow']
color = ['black',
         'grey',
         'blue',
         'white',
         'red',
         'green',
         'blue-dark',
         'pink',
         'brown',
         'purple',
         'green-dark',
         'orange',
         'gold',
         'yellow',
         'maroon']
sort = ['-popularity',
        '-createdAt',
        'price',
        '-price']

# category queue
category = queue.Queue()

# bulk write
bulk = []

# set of products
set_of_product_codes = set()
# queue of products
product_urls = queue.Queue()


def push_to_bulk_to_push_mongo(url_obj):
    """
    :param url_obj: {'url':, 'product_code':}
    """
    bulk.append(UpdateOne({'product_code': url_obj['product_code']}, {'$set': url_obj}, upsert=True))


def check_existed_code(product_code, url):
    """
    if code not existed:
        put url
        return F
    else
        return T
    :param product_code:
    :param url:
    :return: existed code?
    """
    if product_code in set_of_product_codes:
        return True
    else:
        set_of_product_codes.add(product_code)
        product_urls.put(url)
        print(product_urls.qsize())
        return False


def analyze_a_menu(soup):
    """
    open a menu page and add product code to queue
    :param soup: soup of menu page
    :return: (True/ False) have product in page
    """
    there_are_product_url = False
    # print("product url")
    try:
        for div_contain_url in soup.find_all("div", class_="w-1/2 lg:w-1/3 p-p5 lg:p-1"):
            url = 'https://www.giftza.co' + div_contain_url.div.a['href']

            product_code = url[-39:]
            # print(product_code)

            if not check_existed_code(product_code, url):
                there_are_product_url = True
    except Exception as error:
        print(error)
    return there_are_product_url


def amount_of_item_each_category(soup):
    """
    :param soup: soup of page
    :return: amount of item
    """
    try:
        div_contain_amount = soup.find("div", class_="w-full lg:w-3/4 lg:pl-p5")
        div_contain_amount = div_contain_amount.find("div", class_="flex-grow ta-center")
        span_in_div_contain_amount = div_contain_amount.find("span")
        str_item = span_in_div_contain_amount.contents[0]

        # if '1 item', it will return ''
        if str_item == '1 item':
            return int(1)

        str_item = str_item.replace(',', '')

        cnt_item = int(str_item[:-6])

        # print(cnt_item)
        return cnt_item
    except Exception as error:
        print(error)
        return int(0)



def get_url_menus():
    """
    open menus one by one with (_tag, _department, _product, _page, _sort)
    :return: nothing
    """
    while True:
        _tag, _department, _product = category.get()
        # print(_tag, _department, _product)
        for _sort in sort:
            for _page in range(1, 26, 1):
                # print(_page)
                url = 'https://www.giftza.co/tags/{}/sort/{}/page/{}/department/{}/product/{}'.format(_tag, _sort,
                                                                                                      _page,
                                                                                                      _department,
                                                                                                      _product)
                # if page_has_items == 0, we dont need go to the next _page
                if not analyze_a_menu(soup_of_url(url)):
                    break
            # if with (_tag, _department, _product), amount of item <= 900, we dont need to sort twice
            url = 'https://www.giftza.co/tags/{}/department/{}/product/{}'.format(_tag, _department, _product)
            if amount_of_item_each_category(soup_of_url(url)) <= 900:
                break
        category.task_done()


def list_category_to_queue():
    """
    put (_tag, _department, _product) without (page, color, sort) in to category
    :return: nothing
    """
    _tag = 'Holidays%20&%20Events'
    for _department in department:
        for _product in product:
            category.put((_tag, _department, _product))


def xxx():
    while True:
        try:
            url = product_urls.get()
            print(product_urls.qsize())
            soup = soup_of_url(url)
            details = analyze_a_product.analyze_soup_of_a_product(soup)
            product_code = url[-39:]

            url_obj = {'url': url, 'product_code': product_code,
                       'product_price': details[0],
                       'image_urls': details[1],
                       'product_name': details[2],
                       'campaign_details': details[3]}
            push_to_bulk_to_push_mongo(url_obj)
        finally:
            product_urls.task_done()


def main():
    """
    spawn 4 threads to run get_url_of_product_from_menu()
    collected data is written in bulk to push to mongo
    category is a queue which get_url_of_product_from_menu() points to
    :return: nothing
    """
    for x in range(30):
        threading.Thread(target=xxx, daemon=True).start()
    for x in range(30):
        threading.Thread(target=get_url_menus, daemon=True).start()

    list_category_to_queue()

    category.join()
    product_urls.join()

    db.product_urls.bulk_write(bulk)


if __name__ == '__main__':
    ts = time()
    main()
    print(time() - ts)
