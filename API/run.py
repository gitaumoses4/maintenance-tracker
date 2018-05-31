""" Initializes and runs the application"""
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    import app

    APP = app.initialize_app()
    APP.run()
