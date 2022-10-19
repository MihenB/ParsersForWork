import random
import threading
import time
import logging
from kompromat1.config.tor_config import TOR_PORT_CONFIG
from kompromat1.service.db_driver import DBControl


def parse_data(boardings):
    from kompromat1.parsers.tor_photos_parse import tor_links_crawler
    db_driver = DBControl()

    logging.basicConfig(level=logging.INFO,
                        filename=f"links_parse_{threading.current_thread().name}.log",
                        filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    threads = [threading.Thread(target=tor_links_crawler,
                                args=(links_list,
                                      db_driver,
                                      TOR_PORT_CONFIG[i])
                                ) for i, links_list in enumerate(boardings)]

    for thread in threads:
        thread.start()
        time.sleep(random.random())

    for thread in threads:
        thread.join()

    # db_driver.close_connections_pool()


if __name__ == '__main__':
    # Program starts from cor_alg!
    pass
