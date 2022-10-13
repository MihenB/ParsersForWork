import random
import threading
import time
from config.tor_config import TOR_PORT_CONFIG
from db_driver import DBControl
from tor_pages_parse import tor_pages_crawler


def parse_data(boardings):
    db_driver = DBControl()

    # threads = [threading.Thread(target=tor_pages_crawler,
    #                             args=(page_num_list,
    #                                   db_driver,
    #                                   TOR_PORT_CONFIG[i])
    #                             ) for i, page_num_list in enumerate(boardings)]

    threads = [threading.Thread(target=tor_pages_crawler,
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
