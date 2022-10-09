from par import parse_data
from config.tor_config import THREADS_COUNT


def request_to_db():
    return [None, ]


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
    last_page = 10  # requests.get()
    broken_nums = check_missing_data(last_page, show_list=True)
    data_slices = _get_data_slices(len(broken_nums))
    return [broken_nums[i:j] for i, j in data_slices]


def parse_missed_data():
    parse_data(boardings=_get_boardings())


if __name__ == '__main__':
    print((check_missing_data(10, True)))
    # parse_missed_data()
