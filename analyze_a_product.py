from bs4 import BeautifulSoup
import requests


def read_url(url_name, time_out=10):
    try:
        data = requests.get(url_name, timeout=time_out)
    except:
        print('Err: {}'.format(url_name))

    soup = BeautifulSoup(data.text, features='html.parser')

    return soup


def analyze(soup):
    # product price
    print("product price")
    div_contain_price = soup.find("span", class_="lg:fs-2xl")
    span_in_div_contain_price = div_contain_price.find("span")
    print(span_in_div_contain_price.contents[0])
    print()

    # image url
    print("image url")
    for div_contain_img in soup.find_all("div", class_="child-container"):
        print(div_contain_img.find_all("img")[0]['src'])
    print()

    # product name
    print("product name")
    div_contain_name = soup.find("h1", class_="lg:fs-lg")
    spans_in_div_contain_name = div_contain_name.find_all("span")
    print(spans_in_div_contain_name[0].contents[0])
    print(spans_in_div_contain_name[2].contents[0])
    print()

    # campaign details
    div_contain_campaign_details = soup.find("div", class_="px-1 pb-1 lg:px-0 bgc-white")
    div_in_div_contain_campaign_details = div_contain_campaign_details.div
    for div in div_in_div_contain_campaign_details.find_all("div"):
        if div.contents[0] != '<br/>':
            print(div.contents[0])


if __name__ == '__main__':
    analyze(read_url(
        'https://www.giftza.co/campaigns/-/-/tags/Holidays%20%26%20Events/papa-legend-bad-influence?retailProductCode=DBD375D877A0B6-E8F5D89CE8FA-GS2-TC4-BLK'))
