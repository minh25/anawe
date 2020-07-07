from bs4 import BeautifulSoup
import requests
import threading
import queue
from time import time

from pymongo import MongoClient, UpdateOne

from soup_of_url import soup_of_url

# declare mongodb

client = MongoClient("mongodb+srv://giftza:giftza@cluster0.qquas.mongodb.net/test?retryWrites=true&w=majority")
db = client.test


# product filter
tags = ['family-gift', 'Relationship', 'special-gifts', 'mother-s-day', 'father-s-day', 'Holidays%20&%20Events']
department = ['men', 'women', 'youth', 'assessories', 'housewares']
product = ['shirt', 'hoodie', 'hat', 'case', 'sweatshirt', 'longsleeve', 'tanktop', 'mug', 'poster', 'pillowcase',
           'blanket', 'pillow']
color = ['black', 'grey', 'blue', 'white', 'red', 'green', 'blue-dark', 'pink', 'brown', 'purple', 'green-dark',
         'orange', 'gold', 'yellow', 'maroon']
sort = ['-popularity', '-createdAt', 'price', '-price']

# category queue
category = queue.Queue()

# bulk write
bulk = []


def push_mongo(url_obj):
    """
    :param url_obj: {'url':, 'product_code':}
    """
    # db.product_urls.update_one({'product_code': url_obj['product_code']}, {'$set': url_obj}, upsert=True)
    bulk.append(UpdateOne({'product_code': url_obj['product_code']}, {'$set': url_obj}, upsert=True))

def amount_of_item(soup):
    """
    :param soup: soup of page
    :return: amount of item
    """
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


def analyze(soup):
    """
    :param soup: soup of page
    :return: (True/ False) product in page
    """
    there_are_product_url = False
    # print("product url")
    for div_contain_url in soup.find_all("div", class_="w-1/2 lg:w-1/3 p-p5 lg:p-1"):
        # print('https://www.giftza.co',div_contain_url.div.a['href'], sep='')
        url = 'https://www.giftza.co' + div_contain_url.div.a['href']
        url_obj = {'url': url, 'product_code': url[-39:]}
        push_mongo(url_obj)
        there_are_product_url = True
    return there_are_product_url


def get_url_of_product_from_menu():
    """
    ahihi... i can use thread muahahahaha
    :return:
    """
    while True:
        _tag, _department, _product = category.get()
        print(_tag, _department, _product)
        for _sort in sort:
            for _page in range(1, 26, 1):
                print(_page)
                url = 'https://www.giftza.co/tags/{}/sort/{}/page/{}/department/{}/product/{}'.format(_tag, _sort,
                                                                                                      _page,
                                                                                                      _department,
                                                                                                      _product)
                # if page_has_items == 0, we dont need go to the next _page
                if analyze(soup_of_url(url)) == 0:
                    break
            # if with (_tag, _department, _product), amount of item <= 900, we dont need to sort twice
            url = 'https://www.giftza.co/tags/{}/department/{}/product/{}'.format(_tag, _department, _product)
            if amount_of_item(soup_of_url(url)) <= 900:
                break
        category.task_done()


def list_category_to_queue():
    """
    put tuple(_tag, _department, _product) of category without (page, color, sort) in to queue
    :return:
    """
    _tag = 'Holidays%20&%20Events'
    for _department in department:
        for _product in product:
            category.put((_tag, _department, _product))


def main():
    """

    :return:
    """

    threading.Thread(target=get_url_of_product_from_menu, daemon=True).start()
    threading.Thread(target=get_url_of_product_from_menu, daemon=True).start()
    threading.Thread(target=get_url_of_product_from_menu, daemon=True).start()
    threading.Thread(target=get_url_of_product_from_menu, daemon=True).start()

    list_category_to_queue()

    category.join()

    db.product_urls.bulk_write(bulk)


if __name__ == '__main__':
    ts = time()
    main()
    print(time()-ts)
