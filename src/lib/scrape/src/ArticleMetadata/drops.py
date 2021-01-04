import requests
from bs4 import BeautifulSoup

from .handler import add_handler

@add_handler(r'http(s?)://drops.dagstuhl.de/(\w+)')
def download(url):
    metadata = dict()
    metadata['importer'] = 'drops'
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "lxml")

    authortags = soup.find_all("meta", attrs={"name": "citation_author"})
    metadata['authors']  = [i['content'].strip() for i in authortags ]
    metadata['title']    = soup.find_all("meta", attrs={"name": "citation_title"})[0]['content']
    metadata['url']      = soup.find_all("meta", attrs={"name": "citation_pdf_url"})[0]['content']
    metadata['date']     = soup.find_all("meta", attrs={"name": "citation_date"})[0]['content']
    metadata['abstract'] = soup.find(string='Abstract').findParent().findParent().text.replace('\nAbstract\n', '').strip()
    metadata['venue']    = soup.find_all("meta", attrs={"name": "citation_conference_title"})[0]['content']
    metadata['DOI']      = soup.find_all("meta", attrs={"name": "citation_doi"})[0]['content']
    metadata['metaurl']  = url
    metadata['uid']      = metadata['DOI']
    metadata['keywords'] = soup.find("meta", attrs={"name": "DC.Subject", "scheme": "SWD"})['content'].split(',')


    return metadata
