import os
from kompromat1.config.db_config import sql_requests_dict

main_path = '/news_photos'


def format_list_to_dict(cursor):
    cursor.execute(sql_requests_dict['select_id_and_photo_links'])
    ids_and_links = cursor.fetchall()
    result_dict = {
        item[0]: item[1].split('|')[1::] for item in ids_and_links
    }
    return result_dict


def save_photo(local_id, cont, num):
    path = os.path.join(main_path, str(local_id))
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    with open(f'{os.path.join(path, str(num))}.jpg', "wb") as file:
        file.write(cont)
    return path


def main():
    pass


if __name__ == '__main__':
    main()
