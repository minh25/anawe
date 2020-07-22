import queue
import random
import threading
from time import time

import requests
from bs4 import BeautifulSoup

ip_addresses = [
    'http://173.208.43.61:3128',
    'http://173.234.225.185:3128',
    'http://104.140.183.167:3128',
    'http://206.214.82.129:3128',
    'http://173.234.59.109:3128',
    'http://192.161.162.157:3128',
    'http://173.234.59.225:3128',
    'http://91.197.36.66:3128',
    'http://91.197.36.153:3128',
    'http://173.234.59.48:3128',
    'http://206.214.82.97:3128',
    'http://173.208.43.70:3128',
    'http://192.161.162.249:3128',
    'http://192.161.162.226:3128',
    'http://173.234.225.252:3128',
    'http://91.197.36.215:3128',
    'http://173.234.248.17:3128',
    'http://192.161.162.41:3128',
    'http://173.234.225.114:3128',
    'http://173.234.59.115:3128',
    'http://173.234.59.2:3128',
    'http://173.234.225.199:3128',
    'http://192.161.162.23:3128',
    'http://173.208.43.59:3128',
    'http://173.208.43.113:3128',
    'http://173.208.43.146:3128',
    'http://173.208.43.155:3128',
    'http://173.208.43.4:3128',
    'http://104.140.183.205:3128',
    'http://173.234.59.233:3128',
    'http://104.140.183.127:3128',
    'http://173.234.225.145:3128',
    'http://192.126.162.43:3128',
    'http://192.126.162.162:3128',
    'http://91.197.36.173:3128',
    'http://173.234.225.203:3128',
    'http://192.161.162.150:3128',
    'http://91.197.36.108:3128',
    'http://173.208.43.199:3128',
    'http://173.234.59.96:3128',
    'http://173.234.59.137:3128',
    'http://91.197.36.214:3128',
    'http://173.234.59.79:3128',
    'http://91.197.36.19:3128',
    'http://91.197.36.62:3128',
    'http://23.19.97.87:3128',
    'http://91.197.36.9:3128',
    'http://206.214.82.75:3128',
    'http://192.126.162.10:3128',
    'http://173.234.59.162:3128'
]
success = []
fail = []

x = queue.Queue()


def init():
    for _ in ip_addresses:
        success.append(0)
        fail.append(0)


init()


def get_proxy():
    """
    random an ip which be good enough
    :return: ip_i, ip_add
    """
    while True:
        proxy_index = random.randint(0, len(ip_addresses))
        return proxy_index, ip_addresses[proxy_index]
        if success[proxy_index] + fail[proxy_index] < 8:
            return proxy_index, ip_addresses[proxy_index]
        # if success[proxy_index] + fail[proxy_index] >= 5:
        if float(success[proxy_index])/(float(fail[proxy_index]+0.001)) < 0.15:
            success[proxy_index] = success[proxy_index] + 1
            continue
        return proxy_index, ip_addresses[proxy_index]


def soup_of_url(url_name, time_out=20, data=None, proxy_index=0):
    """
    :param url_name:
    :param proxy_index:
    :param data:
    :type time_out: object
    :return: soup of page
    """
    while True:
        try:
            proxy_index, ip_address = get_proxy()
            proxy = {"http": ip_address, "https": ip_address}
            x.put(ip_address)
            data = requests.get(url_name, timeout=time_out, proxies=proxy)
            print("status code", data.status_code)
            success[proxy_index] = success[proxy_index] + 10
            break
        except Exception as error:
            print(error)
            fail[proxy_index] = fail[proxy_index] + 10
            continue

    soup = BeautifulSoup(data.text, features='html.parser')
    print("amount of request: ", x.qsize())
    return soup


def main():
    ts = time()
    for i in range(0, len(ip_addresses), 1):
        soup_of_url("https://www.giftza.co/tags/Holidays%20%26%20Events", time_out=15)
        print(i, time() - ts, len(ip_addresses))
        ts = time()

    print(time() - ts)


if __name__ == '__main__':
    threading.Thread(target=main(), daemon=True).start()
    threading.Thread(target=main(), daemon=True).start()
    threading.Thread(target=main(), daemon=True).start()
    threading.Thread(target=main(), daemon=True).start()
