from flask import Blueprint, send_from_directory

web = Blueprint("routes.web", __name__)


@web.route('/api/v1')
def docs():
    return send_from_directory('v1/docs', 'index.html')
