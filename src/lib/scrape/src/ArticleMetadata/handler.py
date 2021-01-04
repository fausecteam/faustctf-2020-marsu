import re

HANDLERS = []

def add_handler(regex):
    def _add_handler(f):
        HANDLERS.append((re.compile(regex), f))
        return f
    return _add_handler

def handle(url):
    for regex, fun in HANDLERS:
        if re.match(regex, url):
            return fun(url)

    return None
