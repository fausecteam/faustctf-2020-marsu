import argparse
from pprint import pprint

from . import acm
from . import arxiv
from . import doi
from . import drops
from . import eprint
from . import ieee
from . import springer
from . import usenix

from .handler import handle

def get_metadata(url):
    return handle(url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    pprint(args)
    pprint(get_metadata(args.url))
