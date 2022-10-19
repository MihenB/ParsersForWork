import random
import time
import mysql.connector
from bs4 import BeautifulSoup
from kompromat1.config.db_config import sql_requests_dict
from kompromat1.config.request_config import headers, params, url
from kompromat1.service.crawler import TorCrawler, safe_crawler_rotate
from kompromat1.service.user_agent import ExtendedUserAgent


def log_print(cur_num):
    print(f'Current page: {cur_num}')


def tor_pages_crawler(page_num_list, db_driver, crawler_conf: dict):
    current_pos = 0
    commit_period = 2
    crawler = TorCrawler(ctrl_port=crawler_conf['Control'],
                         socks_port=crawler_conf['Socks'])
    ua = ExtendedUserAgent()
    link_body = 'https://kompromat1.pro'
    _headers = headers.copy()
    _params = params.copy()

    connection, cursor = db_driver.get_connection_from_pool()

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
        log_print(current_page)
        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                cards = soup.find_all('a', class_='articles_title')
                links = [link_body + card.get('href') for card in cards]
                current_pos += 1
                print(f'Links on page: {len(links)}')
            elif response.status_code == 403:
                safe_crawler_rotate(crawler)
                time.sleep(random.random())
                continue
            else:
                print(response.text)
                continue
            for link in links:
                cursor.execute(sql_requests_dict['update_table_links_with_pages'], (current_page, link))
            if current_pos % commit_period == 1:
                print(f'[INFO] Committed into mysql!')
                try:
                    connection.commit()
                except mysql.connector.errors.IntegrityError:
                    pass

        except AttributeError:
            print('Response is still None, page skipped!')
            current_pos += 1

    db_driver.commit_and_close_connection(connection=connection, cursor=cursor)
