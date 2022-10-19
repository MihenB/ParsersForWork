import random
import requests
import time
import os
import cfscrape
from stem import Signal
from stem.control import Controller
from stem.connection import authenticate_none, authenticate_password


def safe_crawler_rotate(crawler):
    for _ in range(2):
        try:
            crawler.rotate()
            break
        except Exception as ex:
            print(f'[ERROR] {ex}')
            print('IP rotate failed, trying again...')
            time.sleep(random.random() * 2)


class TorCrawler(object):
    def __init__(
            self,
            ctrl_port=9051,
            ctrl_pass=None,
            enforce_limit=4,
            enforce_rotate=False,
            n_requests=25,
            socks_port=9050,
            socks_host="localhost",
            use_tor=True
    ):
        # Number of requests that have been made since last ip change
        self.req_i = 0

        # The number of consecutive requests made with the same IP.
        self.n_requests = n_requests

        # Do we want to use tor?
        self.use_tor = use_tor

        # Enforce rotation of IPs (if true, redraw circuit until IP is changed)
        self.enforce_rotate = enforce_rotate

        # The threshold at which we can stop trying to rotate IPs and accept
        # the new path. This value is capped at 100 because we don't want to
        # kill the tor network.
        self.enforce_limit = min(100, enforce_limit)

        # SOCKS5 params
        self.tor_port = socks_port
        self.tor_host = socks_host

        # The tor controller that will be used to receive signals
        self.ctrl_port = ctrl_port

        self.tor_controller = None
        if self.use_tor:
            self._setTorController()

        # The control port password
        self.ctrl_pass = None
        self._setCtrlPass(ctrl_pass)
        self.session = self._set_session()

        # Keep an IP address logged
        self.ip = self.check_ip()

    def _setCtrlPass(self, p):
        if p:
            self.ctrl_pass = p
        elif "TOR_CTRL_PASS" in os.environ:
            self.ctrl_pass = os.environ["TOR_CTRL_PASS"]

    def _setTorController(self):
        try:
            self.tor_controller = Controller.from_port(port=self.ctrl_port)
        except Exception as err:
            raise EnvironmentError(err)

    def _set_session(self):
        """Create CFSCRAPE session with proxy. New session creates after each rotate"""
        session = cfscrape.create_scraper(sess=requests.Session())

        session.proxies = {'http': f'socks5h://localhost:{self.tor_port}',
                           'https': f'socks5h://localhost:{self.tor_port}'}
        return session

    def _newCircuit(self):
        if self.ctrl_pass:
            authenticate_password(self.tor_controller, self.ctrl_pass)
        else:
            authenticate_none(self.tor_controller)
        self.tor_controller.signal(Signal.NEWNYM)

    def _updateCount(self):
        """Increment counter and check if we need to rotate."""
        self.req_i += 1
        if self.req_i > self.n_requests and self.enforce_rotate:
            self.rotate()
            self.req_i = 0

    def check_ip(self):
        """Check my public IP via tor."""
        return self.session.get("http://www.icanhazip.com").text[:-2]

    def rotate(self):
        """Redraw the tor circuit and (hopefully) change the IP."""
        count = 0
        while count < self.enforce_limit:
            self._newCircuit()
            self.session = self._set_session()
            new_ip = self.check_ip()

            if new_ip == self.ip and self.enforce_rotate:
                print("IP did not change upon rotation. Retrying...")
                time.sleep(2)
                count += 1
                continue
            else:
                self.ip = new_ip
                print("IP successfully rotated. New IP: {}".format(self.ip))
                break

    def get(self, url, headers=None, cookies=None, params=None) -> requests.Response:
        """Return raw response from GET request."""
        response = self.session.get(url, headers=headers, cookies=cookies, params=params)
        self._updateCount()
        return response

    def post(self, url, data, headers=None, cookies=None) -> requests.Response:
        """Return raw response from POST request."""
        response = self.session.post(url, data=data, headers=headers, cookies=cookies)
        self._updateCount()
        return response
