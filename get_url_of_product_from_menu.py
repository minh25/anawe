from bs4 import BeautifulSoup
import requests


def read_url(url_name, time_out=10):
    data = requests.get(url_name, timeout=time_out)

    soup = BeautifulSoup(data.text, features='html.parser')

    return soup


def analyze(soup):
    # product url
    print("product url")
    for div_contain_url in soup.find_all("div", class_="w-1/2 lg:w-1/3 p-p5 lg:p-1"):
        print('https://www.giftza.co',div_contain_url.div.a['href'], sep='')

if __name__ == '__main__':
	url = "https://www.giftza.co/tags/Holidays%20%26%20Events/sort/-createdAt"
	analyze(read_url(url))
	# read_url(url)
