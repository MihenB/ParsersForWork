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
    'check_collected_link_ids': """select ID from rucriminal.news;""",
    'insert_data_from_link': """INSERT IGNORE INTO rucriminal.news 
    (title, text, photo_path, tags, date_, primary_key) 
    VALUES (%s, %s, %s, %s, %s, %s);"""
}
