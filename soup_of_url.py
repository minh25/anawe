from bs4 import BeautifulSoup
import requests

def soup_of_url(url_name, time_out=20):
    '''
    :return: soup of page
    '''
    try:
        data = requests.get(url_name, timeout=time_out)
        soup = BeautifulSoup(data.text, features='html.parser')
        return soup
    except Exception as error:
        print(url_name, error)