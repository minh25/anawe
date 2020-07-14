from soup_of_url import soup_of_url


def extract_product_price(soup, do_print=True, url='#'):
    try:
        div_contain_price = soup.find("span", class_="lg:fs-2xl")
        span_in_div_contain_price = div_contain_price.find("span")

        if do_print:
            print(span_in_div_contain_price.contents[0])
            print("product price")

        return span_in_div_contain_price.contents[0]
    except Exception as error:
        print(error, "of price", "in", url)
        return "#"


def extract_image_urls(soup, do_print=True, url='#'):
    image_urls = []
    try:
        div_contain_list_of_img = soup.find("div", class_="w-3p5")
        for img_tag in div_contain_list_of_img.find_all("img"):
            image_urls.append((img_tag['src']))

        if do_print:
            print("image url")
            for image_url in image_urls:
                print(image_url)
            print()
    except Exception as error:
        print(error, "of image", "in", url)

    return image_urls


def extract_product_name(soup, do_print=True, url='#'):
    try:
        div_contain_name = soup.find("h1", class_="lg:fs-lg")
        spans_in_div_contain_name = div_contain_name.find_all("span")

        if do_print:
            print("product name")
            print(spans_in_div_contain_name[0].contents[0])
            print(spans_in_div_contain_name[2].contents[0])
            print()

        return spans_in_div_contain_name[0].contents[0] + ' ' + spans_in_div_contain_name[2].contents[0]
    except Exception as error:
        print(error, "of name", "in", url)


def extract_campaign_details(soup, do_print=True, url='#'):
    campaign_details = ''
    try:
        div_contain_campaign_details = soup.find("div", class_="px-1 pb-1 lg:px-0 bgc-white")
        div_in_div_contain_campaign_details = div_contain_campaign_details.div
        for div in div_in_div_contain_campaign_details.find_all("div"):
            if div.contents[0] != '<br/>':
                campaign_details = campaign_details + ' ' + str(div.contents[0])

        if do_print:
            print("campaign details")
            print(campaign_details)
    except Exception as error:
        print(error, "of detail", "in", url)

    return campaign_details


def analyze_soup_of_a_product(soup, urlx):
    detail = [extract_product_price(soup=soup, do_print=False, url=urlx),
              extract_image_urls(soup=soup, do_print=False, url=urlx),
              extract_product_name(soup=soup, do_print=False, url=urlx),
              extract_campaign_details(soup=soup, do_print=False, url=urlx)]

    return detail


def main(url):
    for x in analyze_soup_of_a_product(soup_of_url(url), url):
        print(x)


if __name__ == '__main__':
    main('https://www.giftza.co/campaigns/-/-/tags/Holidays%20%26%20Events/stop-staring-at-my-shamrocks-1?retailProductCode=DBD375D877A0B6-9A280E99A8AE-GS2-TC2-KGR')
