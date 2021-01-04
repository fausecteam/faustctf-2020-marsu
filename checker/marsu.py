#!/usr/bin/python3

import requests
import logging
import json
import secrets

from ctf_gameserver import checkerlib
from utils import *



class CheckerException(BaseException):
    def __init__(self, status, longform=None):
        self._status = status
        self._longform = longform

    @property
    def status(self):
        return self._status

    @property
    def longform(self):
        return self._longform




class MarsuChecker(checkerlib.BaseChecker):
    def _register(self, session=None):
        if session is None:
            session = requests.session()

        r1 = session.get('http://[%(ip)s]:12345/accounts/register' % {'ip': self.ip})
        username = generate_username()
        password = generate_password()
        try:
            r2 = session.post('http://[%(ip)s]:12345/accounts/register' % {'ip': self.ip},
                              data={'username': username,
                                    'password1': password,
                                    'password2': password,
                                    'csrfmiddlewaretoken': session.cookies['csrftoken']},
                              allow_redirects=False)
        except KeyError:
            raise CheckerException(checkerlib.CheckResult.FAULTY)

        if r2.status_code != 302:
            logging.error("%s %s" % (r2.url, r2.text))
            raise CheckerException(checkerlib.CheckResult.FAULTY)

        logging.debug("%s %s" % (r2.url, r2.text))
        return username, password


    def _login(self, session, username, password):
        if session is None:
            session = requests.session()

        r1 = session.get('http://[%(ip)s]:12345/accounts/login' % {'ip': self.ip})
        try:
            r2 = session.post('http://[%(ip)s]:12345/accounts/login/' % {'ip': self.ip},
                              data={'username': username,
                                    'password': password,
                                    'csrfmiddlewaretoken': r1.cookies['csrftoken']},
                              allow_redirects=False)
        except KeyError:
            raise CheckerException(checkerlib.CheckResult.FAULTY)

        if r2.status_code == 200:
            logging.error("Login Failed: %s %s %d" % (r2.url, r2.text, r2.status_code))
            raise CheckerException(status=checkerlib.CheckResult.FLAG_NOT_FOUND)

        if r2.status_code != 302:
            logging.error("%s %s %d" % (r2.url, r2.text, r2.status_code))
            raise CheckerException(status=checkerlib.CheckResult.DOWN)

        logging.debug("%s %s" % (r2.url, r2.text))



    def _get_pad(self, session, content):
        r = session.post('http://[%(ip)s]:12345/p/create/pad' % {'ip': self.ip},
                         data=json.dumps({'name': content}),
                         headers={'X-CSRFToken': session.cookies['csrftoken']},
                         allow_redirects=False
                         )

        try:
            return r.json()
        except json.decoder.JSONDecodeError:
            raise CheckerException(status=checkerlib.CheckResult.FAULTY)


    def _add_pad(self, session, content):
        p = session.post('http://[%(ip)s]:12346/new' % {'ip': self.ip},
                         data=content, allow_redirects=False)

        r = session.post('http://[%(ip)s]:12345/p/add/pad' % {'ip': self.ip},
                         data=json.dumps({'url': p.next.url}),
                         headers={'X-CSRFToken': session.cookies['csrftoken']},
                         allow_redirects=False
                         )
        try:
            return r.json()
        except json.decoder.JSONDecodeError:
            raise CheckerException(status=checkerlib.CheckResult.FAULTY)
        

    def _create_project(self, session, content):
        r1 = session.get('http://[%(ip)s]:12345/p/create' % {'ip': self.ip})

        if secrets.randbits(1) == 0:
            pad = self._get_pad(session, content)
        else:
            pad = self._add_pad(session, content)
        r = session.get(pad['url'])
        if r.status_code != 200:
            raise CheckerException(checkerlib.CheckResult.FAULTY)

        r = session.get(pad['url'] + '/download')
        if r.status_code != 200:
            raise CheckerException(checkerlib.CheckResult.FAULTY)

        r2 = session.post('http://[%(ip)s]:12345/p/create/' % {'ip': self.ip},
                         data={'title': 'My Awesome Mars Research',
                               'people': json.dumps([]),
                               'pad': json.dumps([pad['pk']]),
                               'csrfmiddlewaretoken': r1.cookies['csrftoken']},
                         allow_redirects=False)

        if r2.status_code != 302:
            logging.error("%s %s %d" % (r2.url, r2.text, r2.status_code))
            raise CheckerException(status=checkerlib.CheckResult.DOWN)

        logging.info("%s %s" % (r2.url, r2.text))
        return pad['url'] + '/download', r2.next.url


    def place_flag(self, tick):
        try:
            session = requests.session()
            registration = self._register(session)

            checkerlib.store_state('registration_%(tick)d' % {'tick': tick}, registration)

            urls = self._create_project(session, checkerlib.get_flag(tick))

            checkerlib.store_state('flagurls_%(tick)d' % {'tick': tick}, urls)


            return checkerlib.CheckResult.OK

        except CheckerException as e:
            return e.status

    def check_service(self):
        return checkerlib.CheckResult.OK

    def check_flag(self, tick):
        try:
            session = requests.session()
            try:
                username, password = checkerlib.load_state('registration_%(tick)d' % {'tick': tick})
                logging.info((username, password))
            except TypeError:
                logging.exception("Loading account information")
                return checkerlib.CheckResult.FLAG_NOT_FOUND

            self._login(session, username, password)

            flag = checkerlib.get_flag(tick)
            try:
                urls = checkerlib.load_state('flagurls_%(tick)d' % {'tick': tick})

                for url in urls:
                    r = session.get(url)
                    if not flag in r.text:
                        logging.warning("Flag not found in URL %s %s %s", url, repr(flag), repr(r.text))
                        return checkerlib.CheckResult.FLAG_NOT_FOUND

            except TypeError:
                logging.exception("Loading flag locations")
                return checkerlib.CheckResult.FLAG_NOT_FOUND

            return checkerlib.CheckResult.OK

        except CheckerException as e:
            return e.status




if __name__ == '__main__':
    checkerlib.run_check(MarsuChecker)
