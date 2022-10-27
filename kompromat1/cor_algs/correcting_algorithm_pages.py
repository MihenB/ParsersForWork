import re
import requests
from bs4 import BeautifulSoup
from kompromat1.service.threads_start import parse_data
from kompromat1.service.db_driver import DBControl
from kompromat1.config.tor_config import THREADS_COUNT
from kompromat1.config.request_config import url, headers
from kompromat1.config.db_config import sql_requests_dict


def get_all_collected_pages_from_db(db_control):
    connection, cursor = db_control.create_single_connection()
    cursor.execute(sql_requests_dict['check_collected_pages'])
    parsed_nums = cursor.fetchall()
    parsed_nums = [i[0] for i in parsed_nums]
    db_control.close_single_connection()
    return parsed_nums


def update_pages_in_db(last_page, db_control):
    connection, cursor = db_control.create_single_connection()
    cursor.execute(sql_requests_dict['update_pages_in_table_links_with_pages'],
                   (last_page - int(cursor.execute(sql_requests_dict['get_max_page_from_table_links_with_pages'])))
                   )
    db_control.close_single_connection()


def rename_entities():
    pass


def union_tables_from_different_web_sites():
    pass


def check_unique_id_tables_from_other_tables():
    pass


def solve_captcha(site_key=None):
    pass


def check_missing_data(last_page: int, show_list=False):
    db_control = DBControl()
    update_pages_in_db(last_page=last_page, db_control=db_control)
    collected_keys = get_all_collected_pages_from_db(db_control=db_control)
    left_pages = [i for i in range(1, last_page + 1) if i not in collected_keys]
    if show_list:
        print(f"The next pages haven't been collected: {left_pages}")
    return left_pages


def _get_data_slices(len_broken_num):
    full_len = len_broken_num
    len_broken_num //= THREADS_COUNT
    boardings = [(len_broken_num * i, len_broken_num * (i + 1)) for i in range(THREADS_COUNT - 1)]
    boardings.append((len_broken_num * (THREADS_COUNT - 1), full_len))
    return boardings


def _get_last_page():
    proxies = {'http': 'http://MvfJp6:TwBmNs@212.81.38.234:9027'}
    soup = BeautifulSoup(requests.get(url=url, headers=headers, proxies=proxies).text, 'lxml')
    return int(re.search(r'(\d+)', soup.find(class_='pagenate').text)[0])


def _get_boardings():
    last_page = _get_last_page()
    broken_nums = check_missing_data(last_page, show_list=True)
    data_slices = _get_data_slices(len(broken_nums))
    return [broken_nums[i:j] for i, j in data_slices]


def parse_missed_data():
    print(_get_boardings())
    # parse_data(boardings=_get_boardings())


if __name__ == '__main__':
    parse_missed_data()
