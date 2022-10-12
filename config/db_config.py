db_config = {
    'host': '127.0.0.1',
    'passwd': '1111rucrim',
    'user': 'rucriminal',
    'db': 'rucriminal'
}

sql = {
    'update_table_links_with_pages': """INSERT IGNORE INTO rucriminal.links_with_pages
                                        (page_num, link)
                                        VALUES (%s, %s);
                                     """,
    'check_collected_pages': """select distinct page_num from rucriminal.links_with_pages;"""
}
