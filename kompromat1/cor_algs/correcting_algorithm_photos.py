from kompromat1.threads_start import parse_data
from kompromat1.config.db_config import sql_requests_dict
from kompromat1.service.db_driver import DBControl
from correcting_algorithm_pages import _get_data_slices
import os
from kompromat1.scrapers.photos_scraper import main_path


def get_all_ids_and_links():
    db_control = DBControl()
    connection, cursor = db_control.create_single_connection()
    cursor.execute(sql_requests_dict['select_id_and_photo_links'])
    all_ids_and_links = cursor.fetchall()
    db_control.close_single_connection()
    return all_ids_and_links


def check_missing_data(show_list=False):
    all_ids_and_links = get_all_ids_and_links()
    collected_ids = list(map(int, os.listdir(main_path)))
    missed_ids_with_links = [(i[0], i[1].split('|')[1::]) for i in all_ids_and_links if i[0] not in collected_ids]
    # i[0] - id
    # i[1] - glued links of photos
    if show_list:
        print(f"The next ids of links haven't been collected: {len(missed_ids_with_links)}")
    return missed_ids_with_links


def _get_boardings():
    missed_ids_with_links = check_missing_data(show_list=True)
    data_slices = _get_data_slices(len(missed_ids_with_links))
    return [missed_ids_with_links[i:j] for i, j in data_slices]


def parse_missed_data():
    parse_data(boardings=_get_boardings())


if __name__ == '__main__':
    parse_missed_data()
