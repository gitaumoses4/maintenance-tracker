""" Initializes and runs the application"""
from flask import Flask
import v1, v2

app = Flask(__name__, instance_relative_config=True)

v1.initialize_app(app)

if __name__ == '__main__':
    app.run()
