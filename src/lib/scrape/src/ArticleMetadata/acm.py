import re

import requests
from bs4 import BeautifulSoup

from .handler import add_handler

@add_handler(r'https://dl.acm.org/doi/(\d+.\d+/\d+.\d+)')
@add_handler(r'https://dl.acm.org/doi/abs/(\d+.\d+/\d+.\d+)')
def download(url):
    metadata = dict()
    metadata['importer'] = 'acm'
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "lxml")

    authortags = soup.find_all("a", "author-name")
    metadata['authors']  = [i['title'].strip() for i in authortags ]
    metadata['title']    = soup.find("h1", "citation__title").text
    metadata['date']     = soup.find("span", "epub-section__date").text
    metadata['abstract'] = soup.find("div", "abstractSection").text
    metadata['venue']    = soup.find("span", "epub-section__title").text
    metadata['metaurl']  = soup.find_all("meta", attrs={"property": "og:url"})[0]['content']
    metadata['DOI']      = re.match(r'https://dl.acm.org/doi/abs/(\d+.\d+/\d+.\d+)', metadata['metaurl']).group(1)
    metadata['url']      = metadata['metaurl'].replace('abs', 'pdf')
    metadata['uid']      = metadata['DOI']
    metadata['keywords'] = soup.find("meta", attrs={"name": "keywords"})['content'].split(',')

    return metadata
