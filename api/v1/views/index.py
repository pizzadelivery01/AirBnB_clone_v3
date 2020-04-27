#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User



allTypes = {"user": User, "state": State, "city": City,
                "amenity": Amenity, "place": Place, "review": Review}

@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    results = {}
    for x, y in allTypes.items():
        results[x] = storage.count(y)
    return jsonify(results)
