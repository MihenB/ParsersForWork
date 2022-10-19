import random
import time
import logging
from bs4 import BeautifulSoup
from kompromat1.config.db_config import sql_requests_dict
from kompromat1.config.request_config import headers
from kompromat1.service.user_agent import ExtendedUserAgent
from kompromat1.service.crawler import safe_crawler_rotate, TorCrawler
from kompromat1.scrapers.articles_scraper import get_info_from_site
from kompromat1.cor_algs.correcting_algorithm_articles import get_id_from_link


def log_print(cur_link):
    print(f'[INFO] Current link: {cur_link}')


def tor_links_crawler(links_list, db_driver, crawler_conf: dict):
    current_pos = 0
    commit_period = 10
    crawler = TorCrawler(ctrl_port=crawler_conf['Control'],
                         socks_port=crawler_conf['Socks'])
    ua = ExtendedUserAgent()
    _headers = headers.copy()

    logging.basicConfig(level=logging.INFO, filename="links_parse_logging.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
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
            elif response.status_code == 404:
                print(f'[ERROR] Status code: 404, page not found! Going next page')
                current_pos += 1
                continue
            else:
                logging.warning(f"Page returned status code: {response.status_code}\n"
                                f"Link: {current_link}")
                print(f'[ERROR] Status code: {response.status_code}. Page skipped, see log file!')
                current_pos += 1
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
