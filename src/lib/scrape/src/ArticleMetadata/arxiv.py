import requests
from bs4 import BeautifulSoup

from .handler import add_handler

@add_handler(r'https://arxiv.org/abs/(\d+.\d+)')
def download(url):
    metadata = dict()
    metadata['importer'] = 'arxiv'
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "lxml")

    authortags = soup.find_all("meta", attrs={"name": "citation_author"})
    metadata['authors']  = [i['content'].strip() for i in authortags ]
    metadata['title']    = soup.find_all("meta", attrs={"name": "citation_title"})[0]['content']
    metadata['url']      = soup.find_all("meta", attrs={"name": "citation_pdf_url"})[0]['content']
    metadata['date']     = soup.find_all("meta", attrs={"name": "citation_date"})[0]['content']
    metadata['abstract'] = soup.find_all("meta", attrs={"property": "og:description"})[0]['content']

    metadata['arxiv_id'] = soup.find_all("meta", attrs={"name": "citation_arxiv_id"})[0]['content']
    metadata['metaurl']  = url

    return metadata
