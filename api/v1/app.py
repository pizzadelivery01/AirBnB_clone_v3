#!/usr/bin/python3
""" runs app """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='0.0.0.0')
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def dbColose(error):
    """ close """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ note that we set the 404 status explicitly """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
