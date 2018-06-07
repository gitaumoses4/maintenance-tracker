""" Initializes and runs the application"""
import os
import psycopg2

from dotenv import load_dotenv
from flask import Flask
import v1, v2
from config import config

load_dotenv()
app = Flask(__name__, instance_relative_config=True)

app.config.from_object(config[os.getenv("ENVIRONMENT", "DEVELOPMENT")])

connection = psycopg2.connect(dbname=app.config['DATABASE_NAME'], user=app.config['DATABASE_USER'],
                              password=app.config['DATABASE_PASSWORD'], host=app.config['DATABASE_HOST'])
cursor = connection.cursor()

v1.initialize_app(app)

if __name__ == '__main__':
    app.run()
