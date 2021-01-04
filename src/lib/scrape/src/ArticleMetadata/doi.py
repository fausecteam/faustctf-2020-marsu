import requests

from .handler import add_handler, handle

@add_handler(r'http(s?)://doi.org/(\w+)')
@add_handler(r'http(s?)://dx.doi.org/(\w+)')
def download(url):
    data = requests.head(url)
    return handle(data.headers['Location'])
