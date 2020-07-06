from bs4 import BeautifulSoup
import requests

from soup_of_url import  soup_of_url


def extract_product_price(soup, do_print=True):
    div_contain_price = soup.find("span", class_="lg:fs-2xl")
    span_in_div_contain_price = div_contain_price.find("span")

    if do_print == True:
        print(span_in_div_contain_price.contents[0])
        print("product price")

    return span_in_div_contain_price.contents[0]

def extract_image_urls(soup, do_print=True):
    image_urls = []
    for div_contain_img in soup.find_all("div", class_="child-container"):
        image_urls.append(div_contain_img.find_all("img")[0]['src'])

    if do_print == True:
        print("image url")
        for image_url in image_urls:
            print(image_url)
        print()

    return image_urls

def extract_product_name(soup, do_print=True):
    div_contain_name = soup.find("h1", class_="lg:fs-lg")
    spans_in_div_contain_name = div_contain_name.find_all("span")

    if do_print == True:
        print("product name")
        print(spans_in_div_contain_name[0].contents[0])
        print(spans_in_div_contain_name[2].contents[0])
        print()

    return spans_in_div_contain_name[0].contents[0] + ' ' + spans_in_div_contain_name[2].contents[0]

def extract_campaign_details(soup, do_print=True):
    campaign_details = ''
    div_contain_campaign_details = soup.find("div", class_="px-1 pb-1 lg:px-0 bgc-white")
    div_in_div_contain_campaign_details = div_contain_campaign_details.div
    for div in div_in_div_contain_campaign_details.find_all("div"):
        if div.contents[0] != '<br/>':
            campaign_details = campaign_details + ' ' + str(div.contents[0])

    if do_print == True:
        print("campaign details")
        print(campaign_details)

    return campaign_details


def analyze(soup):
    detail = []

    detail.append(extract_product_price(soup))
    detail.append(extract_image_urls(soup))
    detail.append(extract_product_name(soup))
    detail.append(extract_campaign_details(soup))

    return detail


if __name__ == '__main__':
    print(analyze(soup_of_url(
        'https://www.giftza.co/campaigns/-/-/tags/Holidays%20%26%20Events/papa-legend-bad-influence?retailProductCode=DBD375D877A0B6-E8F5D89CE8FA-GS2-TC4-BLK')))
