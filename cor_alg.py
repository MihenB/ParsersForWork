import re
import requests
from bs4 import BeautifulSoup
from my_parser import parse_data
from config.tor_config import THREADS_COUNT
from config.request_config import url, headers
from config.db_config import sql
from db_driver import DBControl


def request_to_db():
    db_control = DBControl()
    connection, cursor = db_control.create_single_connection()
    parsed_nums = cursor.execute(sql['check_collected_pages']).fetchall()
    print(parsed_nums)
    db_control.close_single_connection()
    return parsed_nums


def check_missing_data(last_page: int, show_list=False):
    collected_keys = request_to_db()
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


def _get_boardings():
    soup = BeautifulSoup(requests.get(url=url, headers=headers).text, 'lxml')
    last_page = int(re.search(r'(\d+)', soup.find(class_='pagenate').text)[0])
    broken_nums = check_missing_data(last_page)
    data_slices = _get_data_slices(len(broken_nums))
    return [broken_nums[i:j] for i, j in data_slices]


def parse_missed_data():
    parse_data(boardings=_get_boardings())


if __name__ == '__main__':
    # soup = BeautifulSoup(requests.get(url=url, headers=headers).text, 'lxml')
    # last_page = int(re.search(r'(\d+)', soup.find(class_='pagenate').text)[0])
    # print((check_missing_data(last_page=last_page)))
    parse_missed_data()
