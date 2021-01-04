import requests
from bs4 import BeautifulSoup

from .handler import add_handler

@add_handler(r'https://link.springer.com/chapter/(\d+.\d+%2F[\w-]+)')
@add_handler(r'https://link.springer.com/article/(\d+.\d+%2F[\w-]+)')
@add_handler(r'https://link.springer.com/chapter/(\d+.\d+/[\w-]+)')
@add_handler(r'https://link.springer.com/article/(\d+.\d+/[\w-]+)')
def download(url):
    metadata = dict()
    metadata['importer'] = 'springer'
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "lxml")

    authortags = soup.find_all("meta", attrs={"name": "citation_author"})
    metadata['authors']  = [i['content'].strip() for i in authortags ]
    metadata['title']    = soup.find_all("meta", attrs={"name": "citation_title"})[0]['content']
    metadata['url']      = soup.find_all("meta", attrs={"name": "citation_pdf_url"})[0]['content']
    metadata['date']     = soup.find_all("meta", attrs={"name": "citation_publication_date"})[0]['content']
    metadata['abstract'] = soup.find_all("meta", attrs={"name": "dc.description"})[0]['content']
    metadata['venue']    = soup.find_all("meta", attrs={"name": "prism.publicationName"})[0]['content']
    metadata['DOI']      = soup.find_all("meta", attrs={"name": "DOI"})[0]['content']
    metadata['metaurl']  = url
    metadata['uid']      = metadata['DOI']
#    metadata['keywords'] = [x['content'] for x in soup.find_all("meta", attrs={"name": "dc.subject"})]
    metadata['keywords'] = [x.text for x in soup.find_all("li", attrs={"class": "c-article-subject-list__subject"})]

    return metadata
