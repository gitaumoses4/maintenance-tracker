"""Runs the database set up options such as refresh, reset and create"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Migration:
    def __init__(self, app):
        self.db_name = app.config['DATABASE_NAME']
        self.db_user = app.config['DATABASE_USER']
        self.db_password = app.config['DATABASE_PASSWORD']
        self.db_host = app.config['DATABASE_HOST']
        self.connection = self.connect()
        self.cursor = self.connection.cursor()

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
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """Closes the connection to the database"""
        self.cursor.close()
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def refresh(self):
        """The refresh function does not recreate the database, but deletes data from the tables"""
        pass
