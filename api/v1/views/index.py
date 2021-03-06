#!/usr/bin/python3
""" main """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User
from models.base_model import BaseModel, Base

allTypes = {"users": User, "states": State, "cities": City,
            "amenities": Amenity, "places": Place, "reviews": Review}


@app_views.route('/status',  strict_slashes=False)
def status():
    """ status """
    return jsonify({"status": "OK"})


@app_views.route('/stats',  strict_slashes=False)
def stats():
    """ stats """
    results = {}
    for x, y in allTypes.items():
        results[x] = storage.count(y)
    return jsonify(results)

if __name__ == "__main__":
    pass
