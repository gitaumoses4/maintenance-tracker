from flask import Blueprint, send_from_directory

web = Blueprint("routes.web", __name__)


@web.route('/')
def docs():
    return send_from_directory('../docs', 'index.html')
