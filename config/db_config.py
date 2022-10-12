db_config = {
    'host': '192.168.43.48',
    'passwd': '00000000qQ!',
    'user': 'test',
    'db': 'test'
}

sql = {
    'update_table_links_with_pages': """INSERT IGNORE INTO rucriminal.links_with_pages
                                        (page_num, link)
                                        VALUES (%s, %s);
                                     """,
    'check_collected_pages': """
    select page_num from rucriminal.links_with_pages;
    """
}
