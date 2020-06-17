import requests

tags = ['family-gift', 'Relationship', 'special-gifts', 'mother-s-day', 'father-s-day', 'Holidays%20&%20Events']
department = ['men', 'women', 'youth', 'assessories', 'housewares']
product = ['shirt', 'hoodie', 'hat', 'case', 'sweatshirt', 'longsleeve', 'tanktop', 'mug', 'poster', 'pillowcase', 'blanket', 'pillow']
color = ['black', 'grey', 'blue', 'white', 'red', 'green', 'blue-dark', 'pink', 'brown', 'purple', 'green-dark', 'orange', 'gold', 'yellow', 'maroon']
sort = ['-popularity', '-createdAt', 'price', '-price']

def read_url(url_name, time_out=1):
    try:
        data = requests.get(url_name, timeout=time_out)
    except:
        return

    print(url_name)

def url_of_menu_pages():
    # _color
    _tag = 'Holidays%20&%20Events'
    for _department in department:
        for _product in product:
            for _sort in sort:
                for _page in range(1, 25, 1):
                    url = 'https://www.giftza.co/tags/{}/sort/{}/page/{}/department/{}/product/{}'.format(_tag, _sort, _page, _department, _product)
                    # read_url(url_name=url)
                    print(url)

if __name__ == '__main__':
    url_of_menu_pages()
