import html
import re

import requests
from bs4 import BeautifulSoup

from .handler import add_handler

@add_handler(r'https://ia.cr/(\d+/\d+)')
@add_handler(r'https://eprint.iacr.org/(\d+/\d+)')
def download(url):
    metadata = dict()
    metadata['importer'] = 'eprint'
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "lxml")

    metadata['title']    = soup.b.string
    metadata['authors']  = [i.strip() for i in soup.i.string.split('and') ]
    metadata['abstract'] = html.unescape(data.text.split('</b>', 2)[2].split('<b>', 1)[0].replace('<P>', '').replace('<p />', ''))
    metadata['metaurl']  = url.replace('ia.cr', 'eprint.iacr.org')
    metadata['url']      = metadata['metaurl'] +  '.pdf'
    metadata['uid']      = re.match(r'https://eprint.iacr.org/(\d+/\d+)', metadata['metaurl']).group(1)

    for piece in data.text.split('<b>'):
        if piece.startswith('Category / Keywords:'):
            metadata['keywords'] = piece.split('</b>')[1].replace('<p />', '\n').strip().split(',')
        if piece.startswith('Date:'):
            metadata['date'] = piece.split('</b>')[1].replace('<p />', '\n').strip()

    return metadata
