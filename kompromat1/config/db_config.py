db_config = {
    'host': '127.0.0.1',
    'passwd': '1111rucrim',
    'user': 'rucriminal',
    'db': 'rucriminal'
}

sql_requests_dict = {
    'update_table_links_with_pages': """INSERT IGNORE INTO rucriminal.links_with_pages
                                        (page_num, link)
                                        VALUES (%s, %s);
                                     """,
    'check_collected_pages': """select distinct page_num from rucriminal.links_with_pages;""",
    'get_all_links': """select link from rucriminal.links_with_pages;""",
    'check_collected_link_ids': """select local_id from rucriminal.news;""",
    'insert_data_from_link': """INSERT IGNORE INTO rucriminal.news 
                                (title, text, tags, date, local_id, photos_links) 
                                VALUES (%s, %s, %s, %s, %s, %s);""",
    'select_id_and_photo_links': """select local_id, photos_links from rucriminal.news;""",
    'insert_id_and_photo_path': """insert ignore into rucriminal.photos_paths
                                   (local_id, path)
                                   values (%s, %s);""",
    'update_pages_in_table_links_with_pages': """update rucriminal.links_with_pages
                                                 set page_num = page_num + %s;""",
    'get_max_page_from_table_links_with_pages': """select max(page_num) from rucriminal.links_with_pages;""",
    # 'update_local_ids_in_table_links_with_pages': """update rucriminal.links_with_pages
    #                                                  set local_id = %s
    #                                                  where id = %s;""",
    # 'select_link_where_id_in_table_links_with_pages': """select link from rucriminal.links_with_pages where id = %s;""",
    # 'get_max_id_from_table_links_with_pages': """select max(id) from rucriminal.links_with_pages;"""
}
