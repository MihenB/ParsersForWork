db_config = {
    'host': '192.168.43.48',
    'passwd': '00000000qQ!',
    'user': 'test',
    'db': 'test'
}

sql = {
    'update_table_links_with_pages': """INSERT IGNORE INTO news_parser_db.pages
                                        (page, link)
                                        VALUES (%s, %s);
                                     """,
    'check_collected_pages': """
    select 
    """
}
