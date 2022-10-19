import os
import logging
import threading
from kompromat1.config.db_config import sql_requests_dict
from kompromat1.config.request_config import headers
from kompromat1.service.user_agent import ExtendedUserAgent
from kompromat1.service.crawler import safe_crawler_rotate, TorCrawler
from kompromat1.scrapers.photos_scraper import save_photo
from kompromat1.scrapers.photos_scraper import main_path


def tor_links_crawler(ids_with_links_list, db_driver, crawler_conf: dict):
    commit_period = 10
    crawler = TorCrawler(ctrl_port=crawler_conf['Control'],
                         socks_port=crawler_conf['Socks'])
    ua = ExtendedUserAgent()
    _headers = headers.copy()

    logging.basicConfig(level=logging.INFO,
                        filename=f"links_parse_{threading.current_thread().name}.log",
                        filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    connection, cursor = db_driver.get_connection_from_pool()

    for current_pos in range(len(ids_with_links_list)):
        current_id = ids_with_links_list[current_pos][0]
        current_links = ids_with_links_list[current_pos][1]

        _headers.update({'user-agent': ua.random_fresh_ua})
        response = None

        current_link_pos = 0
        rotate_tries = 0

        while current_link_pos < len(current_links):
            current_link = current_links[current_link_pos]
            for _ in range(2):
                try:
                    response = crawler.get(url=current_link,
                                           headers=_headers)
                    break
                except Exception as ex:
                    print(f'[ERROR] {ex}\nTrying again...')

            try:
                if response.status_code == 200:
                    log_path = save_photo(local_id=current_id, cont=response.content, num=current_link_pos)
                    current_link_pos += 1
                    print(f'[INFO] Photo saved into {log_path}')
                elif response.status_code in (403, 503):
                    if rotate_tries < 3:
                        print(f'[WARNING] Status code: {response.status_code}\n'
                              f'Rotate try #{rotate_tries}')
                        safe_crawler_rotate(crawler)
                        rotate_tries += 1
                    else:
                        rotate_tries = 0
                        current_link_pos += 1
                else:
                    logging.warning(f"Page returned status code: {response.status_code}\n"
                                    f"Link: {current_link}")
                    print(f'[ERROR] Status code: {response.status_code}. Page skipped, see log file!')
                    current_link_pos += 1
                    continue
            except AttributeError:
                print('Response is still None, photo skipped!')
                current_link_pos += 1

        cursor.execute(sql_requests_dict['insert_id_and_photo_path'],
                       (
                           current_id,
                           os.path.join(main_path, str(current_id))
                       ))

        if current_pos % commit_period == 1:
            print(f'[INFO] Committed into mysql!')
            connection.commit()

    db_driver.commit_and_close_connection(connection=connection, cursor=cursor)
