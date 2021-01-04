import re
import json

import requests

from .handler import add_handler

@add_handler(r'http(s?)://ieeexplore.ieee.org/(\w+)')
def download(url):
    metadata = dict()
    metadata['importer'] = 'ieee'
    data = requests.get(url)

    metadataline = [ x for x in data.text.split('\n') if 'document.metadata' in x ][0]
    metadataline = metadataline[metadataline.find('=')+1:-1]

    metadata['abstract'] = list()
    while True:
        if not '"abstract"' in metadataline:
            break

        pos   = metadataline.find('"abstract"')
        left  = metadataline[:pos]
        right = metadataline[pos+len('"abstract":"'):]
        pos2  = re.search(r'([^\\]")', right).end()
        abstract = right[:pos2-1]
        if not abstract in ['true', 'false']:
            metadata['abstract'].append(abstract)
        right = right[pos2+1:]

        metadataline = left + right

    data = json.loads(metadataline)

    metadata['DOI']      = data['doi']
    metadata['url']      = 'https://ieeexplore.ieee.org/' + data['pdfUrl']
    metadata['authors']  = [x['name'] for x in data['authors'] ]
    metadata['venue']    = data['publicationTitle']
    metadata['title']    = data['standardTitle']
    metadata['date']     = data['publicationDate']
    metadata['metaurl']  = 'https://ieeexplore.ieee.org/document/%s' % (data['articleId'], )
    metadata['abstract'] = ''.join(metadata['abstract'])
    metadata['keywords'] = []
    for bag in data['keywords']:
        metadata['keywords'] = metadata['keywords'] + bag['kwd']

    metadata['keywords'] = sorted(metadata['keywords'])
    try:
        metadata['abstract'] = metadata['abstract'][:metadata['abstract'].find('<\\n<')]
    except Exception:
        pass
    metadata['uid']      = metadata['DOI']

    return metadata
