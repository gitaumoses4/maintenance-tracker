"""Runs the database set up options such as refresh, reset and create"""
import psycopg2
from flask import Flask
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor

from config import default_config
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config.from_object(default_config)


class Database:
    def __init__(self, app):
        self.db_name = app.config['DATABASE_NAME']
        self.db_user = app.config['DATABASE_USER']
        self.db_password = app.config['DATABASE_PASSWORD']
        self.db_host = app.config['DATABASE_HOST']
        self.connection = self.connect()
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def connect(self, dbname='postgres'):
        """Connects to the postgres database in order to run migrations and create another database
        based on the configuration set"""

        connection = psycopg2.connect(dbname=dbname, user=self.db_user,
                                      password=self.db_password, host=self.db_host)

        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return connection

    def run(self):
        """Drops the existing database and creates a new one with the specific tables"""

        self.cursor.execute("DROP DATABASE IF EXISTS {}".format(self.db_name))
        self.cursor.execute("CREATE DATABASE {}".format(self.db_name))

        self.commit()
        self.close_connection()

        # reconnect to the database
        self.connection = self.connect(self.db_name)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def close_connection(self):
        """Closes the connection to the database"""
        self.cursor.close()
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def refresh(self):
        """The refresh function does not recreate the database, but deletes data from the tables"""
        pass


# Running this file drops the database and creates the tables
if __name__ == '__main__':
    migration = Database(app)
    migration.run()
    dict_cur = migration.cursor
    dict_cur.execute("CREATE TABLE IF NOT EXISTS test(num serial PRIMARY KEY, data varchar);")
    dict_cur.execute("INSERT INTO test (num, data) VALUES(%s, %s) ", (100, "abc'def"))
    dict_cur.execute("SELECT * FROM test")
    rec = dict_cur.fetchone()
