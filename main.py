import threading
from time import time

from get_category import create_category_without_sort_page, get_category
from get_category import category_without_sort_page, menu_urls

from get_url_of_product import get_url_of_product
from get_url_of_product import product_urls

from analyze_a_product import get_detail_of_product
from analyze_a_product import detail_products

from push_mongo import push_mongo


def main():
    create_category_without_sort_page()

    for _ in range(30):
        threading.Thread(target=get_category, daemon=True).start()
    for _ in range(30):
        threading.Thread(target=get_url_of_product, daemon=True, args=(menu_urls,)).start()
    for _ in range(30):
        threading.Thread(target=get_detail_of_product, daemon=True, args=(product_urls,)).start()

    category_without_sort_page.join()
    menu_urls.join()
    product_urls.join()

    push_mongo(detail_products)


if __name__ == '__main__':
    ts = time()
    main()
    print(time() - ts)
