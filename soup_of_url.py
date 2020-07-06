from bs4 import BeautifulSoup
import requests

def soup_of_url(url_name, time_out=10):
    '''
    :return: soup of page
    '''
    data = requests.get(url_name, timeout=time_out)
    soup = BeautifulSoup(data.text, features='html.parser')
    return soup