import psycopg2
from psycopg2.extras import RealDictCursor

from config import config


class Database:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = psycopg2.connect(dbname=config.DATABASE_NAME, user=config.DATABASE_USER,
                                           password=config.DATABASE_PASSWORD, host=config.DATABASE_HOST,port=config.DATABASE_PORT)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)


db = Database()
