""" Initializes and runs the application"""
from dotenv import load_dotenv

load_dotenv()

import app

APP = app.initialize_app()
if __name__ == '__main__':
    APP.run()
