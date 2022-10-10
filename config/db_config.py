db_config = {
    'host': '192.168.43.48',
    'passwd': '00000000qQ!',
    'user': 'test',
    'db': 'test'
}

sql = {
    'update_table_links_with_pages': """INSERT INTO test.links_with_pages
                                        (link, page_num)
                                        VALUES (%s, %s);
                                     """
}
