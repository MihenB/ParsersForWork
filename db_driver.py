import mysql.connector
from config.db_config import db_config
from config.tor_config import THREADS_COUNT


class DBControl:
    def __init__(self):
        self.connections_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="news_parser",
                                                                            pool_size=THREADS_COUNT,
                                                                            **db_config)

    def create_connection(self):
        connection = self.connections_pool.get_connection()
        cursor = connection.cursor()
        return connection, cursor

    @staticmethod
    def commit_and_close_connection(connection, cursor):
        connection.commit()
        cursor.close()
        connection.close()
