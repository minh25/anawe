# mày có một file get_category nhưng thực chất là get hết tất cả url của các menu
# được xử lí 30 luồng
# trả về 1 queue gồm toàn những menu url full 5 chỉ số chỉ thẳng mặt từng page một
# gon gàng
# bao xịn
#
# menu_urls: queue(links have _tag, _sort, _page, _department, _product)

import threading
import queue
from time import time

import soup_of_url

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

category_without_sort_page = queue.Queue()

menu_urls = queue.Queue()


def amount_of_item_each_category(soup, url):
    """
    :param url: use to warn error
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
        print(error, "in", url)
        # print(soup)
        return int(-1)


def get_category_without_sort_page():
    _tag = 'Holidays%20&%20Events'
    for _department in department:
        for _product in product:
            category_without_sort_page.put((_tag, _department, _product))


# cho gọn
def url3(_tag, _department, _product):
    return "https://www.giftza.co/tags/{}/department/{}/product/{}".format(_tag, _department, _product)


# cho gọn
def url5(_tag, _sort, _page, _department, _product):
    return "https://www.giftza.co/tags/{}/sort/{}/page/{}/department/{}/product/{}".format(_tag, _sort, _page,
                                                                                           _department, _product)


def get_category():
    while True:
        try:
            _tag, _department, _product = category_without_sort_page.get()
            url = url3(_tag, _department, _product)

            while True:
                soup = soup_of_url.soup_of_url(url)
                amount = amount_of_item_each_category(soup, url)
                if amount == -1:
                    continue
                break

            print(amount, url)
            page = int((amount + 35) / 36)

            if page > 0:
                if page <= 25:
                    _sort = sort[0]
                    for _page in range(1, page + 1, 1):
                        menu_url = url5(_tag,_sort,_page,_department,_product)
                        menu_urls.put(menu_url)
                if page > 25:
                    for _sort in sort:
                        for _page in range(1, 26, 1):
                            menu_url = url5(_tag,_sort,_page,_department,_product)
                            menu_urls.put(menu_url)
        # except Exception as error:
        #     print("##########################")
        #     print(error)
        finally:
            category_without_sort_page.task_done()


def main():
    """
    add thread... simply
    :return:
    """
    for _ in range(30):
        threading.Thread(target=get_category, daemon=True).start()

    get_category_without_sort_page()

    category_without_sort_page.join()

    print(menu_urls.qsize())


if __name__ == '__main__':
    ts = time()
    main()
    print(time() - ts)
