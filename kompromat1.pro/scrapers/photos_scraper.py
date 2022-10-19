import requests
from config.db_config import sql_requests_dict
import asyncio
import os
from config.request_config import headers
import logging
from db_driver import DBControl

main_path = '/news_photos'
logging.basicConfig(level=logging.INFO, filename="links_parse_logging.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")


def format_list_to_dict(cursor):
    cursor.execute(sql_requests_dict['select_id_and_photo_links'])
    ids_and_links = cursor.fetchall()
    result_dict = {
        item[0]: item[1].split('|')[1::] for item in ids_and_links
    }
    return result_dict


async def load_and_safe_picture(local_id, link_dict):
    path = os.path.join(main_path, local_id)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    for num, link in enumerate(link_dict):
        with open(os.path.join(path, str(num)), "wb") as file:
            try:
                picture = requests.get(link, headers=headers)
            except Exception:
                logging.exception(f'Link {link} is not available')
                continue
            try:
                file.write(picture.content)
            except AttributeError:
                logging.exception(f'Links {link} content damaged')
    print(f'[INFO] file(s) has written to {path}')


async def run_tasks(collected_dict):
    tasks = [asyncio.create_task(load_and_safe_picture(key, val))
             for key, val in collected_dict.items()]
    await asyncio.gather(*tasks)


def collect(cursor):
    collected_dict = format_list_to_dict(cursor)
    asyncio.run(run_tasks(collected_dict))


def main():
    db_control = DBControl()
    conn, cur = db_control.create_single_connection()
    collect(cur)
    db_control.close_single_connection()


if __name__ == '__main__':
    main()


