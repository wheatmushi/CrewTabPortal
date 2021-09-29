# CrewTab portal authorization v2.5
# with retries, custom timeout, pickled credentials and login forwarding wrapped in modified requests.Session obj

import requests
import re
import pickle
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class SessionCrewTabPortal(requests.Session):  # set timeout=10s and 5 retries by default for every request
    def __init__(self, url_main):
        super(SessionCrewTabPortal, self).__init__()
        retries = Retry(total=5, backoff_factor=1)
        self.mount('https://', HTTPAdapter(max_retries=retries))
        self.mount('http://', HTTPAdapter(max_retries=retries))
        self.url_main = url_main

    def request(self, *args, **kwargs):
        if kwargs.get('timeout') is None:
            kwargs['timeout'] = 10
        args = (args[0],) + (self.url_main + args[1],) + args[2:]
        return super(SessionCrewTabPortal, self).request(*args, **kwargs)

    def get_csrf(self, url):  # catch CSRF keys from http responses
        req = self.get(url)
        if type(req) == requests.models.Response:
            soup = BeautifulSoup(req.content, 'html.parser')
            return soup.find('input', {'name': '_csrf'}).get('value')
        return req

    def authentication(self, login=None, password=None):
        if not login and not password:
            with open('/Volumes/zip/credentials.pkl', 'rb') as inp:
                credentials = pickle.load(inp)
            destination = self.url_main.replace('https://', '').replace('http://', '').replace('/', '')
            login = credentials[destination]['login']
            password = credentials[destination]['password']
        print('\nopening session...')

        if not re.match('[^@]+@[^@]+\.[^@]+', login):
            login = login + '@sita.aero'

        csrf = self.get_csrf('login')
        credentials = {'username': login, 'password': password, '_csrf': csrf}
        p = self.post('login', credentials)

        #if p.url != self.url_main + 'core/index':
        if not p.url.startswith(self.url_main + 'core/index'):
            print('incorrect login or password, try again!\n')
            return self.authentication()
        else:
            print('session loaded successfully\n')
            return self, login
