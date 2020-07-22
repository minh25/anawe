import threading
import queue

import soup_of_url

set_of_product_codes = set()

product_urls = queue.Queue()
product_urls_2 = queue.Queue()


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
        product_urls_2.put(url)  # debug
        print("find out: ", product_urls.qsize(), ", remain: ", product_urls_2.qsize())
        return False


def analyze_a_menu(soup, urlx="#"):
    """
    open a menu page and add product code to queue
    :param urlx: use to warn error
    :param soup: soup of menu page
    :return: (True/ False) have product in page
    """
    there_is_error = True
    try:
        for div_contain_url in soup.find_all("div", class_="w-1/2 lg:w-1/3 p-p5 lg:p-1"):
            url = 'https://www.giftza.co' + div_contain_url.div.a['href']

            product_code = url[-39:]

            check_existed_code(product_code, url)

            there_is_error = False
    except Exception as error:
        print("###", error, "in", urlx)
        there_is_error = True

    return there_is_error


def get_url_of_product(menu_urls=queue.Queue()):
    while True:
        try:
            url = menu_urls.get()
            while True:
                soup = soup_of_url.soup_of_url(url)
                there_is_error = analyze_a_menu(soup, url)
                if there_is_error:
                    continue
                break
        finally:
            menu_urls.task_done()


def main():
    q = queue.Queue()

    for _ in range(30):
        q.put("https://www.giftza.co/tags/Holidays%20%26%20Events")

    for _ in range(30):
        threading.Thread(target=get_url_of_product, daemon=True, args=(q,)).start()

    q.join()


if __name__ == '__main__':
    main()
