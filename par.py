import os
import random
import threading
import time
from bs4 import BeautifulSoup
from crawler import TorCrawler
from user_agent import ExtendedUserAgent
from config.tor_config import TOR_PORT_CONFIG
from config.request_config import headers, params, url


def read_url_list(positions):
    with open('urls.txt', 'r', encoding='utf-8') as read_file:
        all_lines = read_file.readlines()
        return [(i, all_lines[i]) for i in range(len(all_lines)) if i in positions]


def safe_crawler_rotate(crawler):
    for _ in range(2):
        try:
            crawler.rotate()
            break
        except Exception as ex:
            print(f'[ERROR] {ex}')
            print('IP rotate failed, trying again...')
            time.sleep(random.random() * 2)


def log_print(cur_num):
    print(f'Current page: {cur_num}')


def tor_data_access(page_num_list, filename, crawler_conf: dict):
    current_pos = 0
    crawler = TorCrawler(ctrl_port=crawler_conf['Control'],
                         socks_port=crawler_conf['Socks'])
    ua = ExtendedUserAgent()
    _headers = headers.copy()
    _params = params.copy()

    while current_pos < len(page_num_list):
        current_page = page_num_list[current_pos]
        _headers.update({'user-agent': ua.random_fresh_ua})
        _params.update({'pg': current_page})
        response = None
        for _ in range(2):
            try:
                response = crawler.get(url=url,
                                       headers=_headers,
                                       params=_params)
                break
            except Exception as ex:
                print(f'[ERROR] {ex}\nTrying again...')
        log_print(f'Page: {current_page}')
        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                cards = soup.find_all('a', class_='articles_title')
                for card in cards:
                    link = card.get('href')
                    print(f'Success! {link}')
            elif response.status_code == 403:
                safe_crawler_rotate(crawler)
                time.sleep(random.random())
                continue
            else:
                print(response.text)
                continue
        except AttributeError:
            print('Response is still None, page skipped!')


def parse_data(boardings):
    threads = [threading.Thread(target=tor_data_access,
                                args=(page_num_list,
                                      os.path.join('written_data', f'THREAD_{i}.json'),
                                      TOR_PORT_CONFIG[i])
                                ) for i, page_num_list in enumerate(boardings)]

    for thread in threads:
        thread.start()
        time.sleep(random.random())

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    # Program starts from cor_alg!
    pass
