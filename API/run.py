""" Initializes and runs the application"""
import os

from dotenv import load_dotenv
from flask import Flask
import v1, v2
from config import config
from database import Database

load_dotenv()
app = Flask(__name__, instance_relative_config=True)


app.config.from_object(config[os.getenv("ENVIRONMENT", "DEVELOPMENT")])
database = Database(app)

v1.initialize_app(app)

if __name__ == '__main__':
    app.run()
