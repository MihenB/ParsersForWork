import re
from kompromat1.service.threads_start import parse_data
from kompromat1.config.db_config import sql_requests_dict
from kompromat1.service.db_driver import DBControl
from correcting_algorithm_pages import _get_data_slices


def get_collected_and_all_ids():
    db_control = DBControl()
    connection, cursor = db_control.create_single_connection()
    cursor.execute(sql_requests_dict['check_collected_link_ids'])
    parsed_ids = [i[0] for i in cursor.fetchall()]
    cursor.execute(sql_requests_dict['get_all_links'])
    all_link_ids = [(get_id_from_link(i[0]), i[0]) for i in cursor.fetchall()]
    db_control.close_single_connection()
    return parsed_ids, all_link_ids


def get_id_from_link(link):
    link_id = int(re.search(r'/(\d+)-', link)[1])
    return link_id


def check_missing_data(show_list=False):
    collected_ids, all_link_ids = get_collected_and_all_ids()
    missed_links = [i[1] for i in all_link_ids if i[0] not in collected_ids]
    if show_list:
        print(f"The next ids of links haven't been collected: {len(missed_links)}")
    return missed_links


def _get_boardings():
    missed_links = check_missing_data(show_list=True)
    data_slices = _get_data_slices(len(missed_links))
    return [missed_links[i:j] for i, j in data_slices]


def parse_missed_data():
    parse_data(boardings=_get_boardings())


if __name__ == '__main__':
    parse_missed_data()
    check_missing_data(show_list=True)
