import random
import time
from bs4 import BeautifulSoup
from config.db_config import sql_requests_dict
from config.request_config import headers
from crawler import TorCrawler
from user_agent import ExtendedUserAgent
from crawler import safe_crawler_rotate
from links_scraper import get_info_from_site
from correcting_algorithm_links import get_id_from_link


def log_print(cur_link):
    print(f'[INFO] Current link: {cur_link}')


def tor_links_crawler(links_list, db_driver, crawler_conf: dict):
    current_pos = 0
    commit_period = 10
    crawler = TorCrawler(ctrl_port=crawler_conf['Control'],
                         socks_port=crawler_conf['Socks'])
    ua = ExtendedUserAgent()
    _headers = headers.copy()

    connection, cursor = db_driver.get_connection_from_pool()

    while current_pos < len(links_list):
        current_link = links_list[current_pos]
        _headers.update({'user-agent': ua.random_fresh_ua})
        response = None
        for _ in range(2):
            try:
                response = crawler.get(url=current_link,
                                       headers=_headers)
                break
            except Exception as ex:
                print(f'[ERROR] {ex}\nTrying again...')
        log_print(current_link)
        try:

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                link_id = get_id_from_link(current_link)
                parsed_data = get_info_from_site(soup=soup, primary_key=link_id)
                current_pos += 1
                print(f'[INFO] Title: {parsed_data["title"]} PARSED!')
            elif response.status_code == 403:
                safe_crawler_rotate(crawler)
                time.sleep(random.random())
                continue
            else:
                print(f'[ERROR] Status code: {response.status_code})
                continue

            cursor.execute(sql_requests_dict['insert_data_from_link'],
                           (parsed_data.get('title'), parsed_data.get('text'),
                            parsed_data.get('photo_path'), parsed_data.get('tags'),
                            parsed_data.get('date'), parsed_data.get('primary_key'),
                            parsed_data.get('photos_links')))
            if current_pos % commit_period == 1:
                print(f'[INFO] Committed into mysql!')
                connection.commit()

        except AttributeError:
            print('Response is still None, page skipped!')
            current_pos += 1

    db_driver.commit_and_close_connection(connection=connection, cursor=cursor)
