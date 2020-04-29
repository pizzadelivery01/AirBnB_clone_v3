#!/usr/bin/python3
""" runs app """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def dbColose(error):
    """ close """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ note that we set the 404 status explicitly """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
