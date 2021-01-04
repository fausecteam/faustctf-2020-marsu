import re

import requests
from bs4 import BeautifulSoup

from .handler import add_handler

@add_handler(r'https://www.usenix.org/([\w-]+)')
def download(url):
    metadata = dict()
    metadata['importer'] = 'usenix'
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "lxml")

    authortags = soup.find_all("meta", attrs={"name": "citation_author"})
    metadata['authors']  = [i['content'].strip() for i in authortags ]
    metadata['title']    = soup.find_all("meta", attrs={"name": "citation_title"})[0]['content']
    metadata['url']      = soup.find_all("meta", attrs={"name": "citation_pdf_url"})[0]['content']
    metadata['date']     = soup.find_all("meta", attrs={"name": "citation_publication_date"})[0]['content']
    metadata['abstract'] = soup.find(string=re.compile('Abstract:(.*)')).findParent().findNextSibling().text
    metadata['venue']    = soup.find_all("meta", attrs={"name": "citation_conference_title"})[0]['content']
    metadata['metaurl']  = url
    metadata['uid']      = '/'.join([soup.find_all("meta", attrs={"name": "citation_isbn"})[0]['content'],
                                     soup.find_all("meta", attrs={"name": "citation_firstpage"})[0]['content']])

    return metadata
