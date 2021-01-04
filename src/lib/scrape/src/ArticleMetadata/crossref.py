import requests


def crossref(doi):
    r = requests.get("https://api.crossref.org/works/%s" % (doi, ))
    return r.json()
