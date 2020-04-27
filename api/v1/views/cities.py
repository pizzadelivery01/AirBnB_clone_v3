#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def citysGet(state_id):
    theState = storage.get(State, state_id)
    if theState:
        return jsonify(theState.cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def citysGetId(city_id):
    thecity = storage.get(City, city_id)
    if thecity:
        return jsonify(thecity.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def citysDeleteId(city_id):
    thecity = storage.get(City, city_id)
    if thecity:
        storage.delete(thecity)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def citysPost(state_id):
    print('test')
    requested = request.get_json()
    theState = storage.get(State, state_id)
    if theState:
        if requested:
            if 'name' in requested:
                newcity = City(**requested)
                setattr(newcity, 'state_id', state_id)
                storage.new(newcity)
            else:
                return 'Missing name', 400
        else:
            return 'Not a JSON', 400
        return jsonify(newcity.to_dict()), 201
    else:
        abort(404)
    

@app_views.route('/cities/<city_id>', methods=['PUT'])
def citysPutId(city_id):
    ignore = ['id', 'created_at', 'updated_at', 'state_id']
    thecity = storage.get(City, city_id)
    if thecity:
        requested = request.get_json()
        if requested:
            for x, y in requested.items():
                if x not in ignore:
                    setattr(thecity, x, y)
            thecity.save()
        else:
            return 'Not a JSON', 400
        return jsonify(thecity.to_dict()), 200
    else:
        abort(404)
