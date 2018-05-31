""" Initializes and runs the application"""
from dotenv import load_dotenv

load_dotenv()

import app

app = app.initialize_app()
if __name__ == '__main__':
    app.run()
