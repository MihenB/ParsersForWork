import random
import threading
import time
import mysql.connector
from bs4 import BeautifulSoup
from crawler import TorCrawler
from user_agent import ExtendedUserAgent
from config.tor_config import TOR_PORT_CONFIG
from config.request_config import headers, params, url
from db_driver import DBControl
from config.db_config import sql


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


def tor_data_access(page_num_list, db_driver, crawler_conf: dict):
    current_pos = 0
    commit_period = 2
    crawler = TorCrawler(ctrl_port=crawler_conf['Control'],
                         socks_port=crawler_conf['Socks'])
    ua = ExtendedUserAgent()
    link_body = 'https://kompromat1.pro'
    _headers = headers.copy()
    _params = params.copy()

    connection, cursor = db_driver.create_connection()

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
                cursor.execute(sql['update_table_links_with_pages'], (link, current_page))
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


def parse_data(boardings):
    db_driver = DBControl()

    threads = [threading.Thread(target=tor_data_access,
                                args=(page_num_list,
                                      db_driver,
                                      TOR_PORT_CONFIG[i])
                                ) for i, page_num_list in enumerate(boardings)]

    for thread in threads:
        thread.start()
        time.sleep(random.random())

    for thread in threads:
        thread.join()

    # db_driver.close_connections_pool()


if __name__ == '__main__':
    # Program starts from cor_alg!
    pass
