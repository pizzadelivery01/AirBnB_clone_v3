#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def statesGet():
    """ states """
    allList = []
    objs = storage.all(State)
    for x, y in objs.items():
        allList.append(y.to_dict())
    return jsonify(allList)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def statesGetId(state_id):
    """ states """
    target = "State." + str(state_id)
    allList = []
    if target in storage.all(State).keys():
        return jsonify(storage.all(State)[target].to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def statesDeleteId(state_id=None):
    """ states """
    theState = storage.get(State, state_id)
    if theState:
        theState.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def statesPost():
    """ states """
    requested = request.get_json()
    if requested:
        if 'name' in requested:
            newState = State(**request.getjson())
            newState.save()
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")
    return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def statesPutId(state_id=None):
    """ updates """
    ignore = ['id', 'created_at', 'updated_at']
    theState = storage.get(State, state_id)
    if theState:
        requested = request.get_json()
        if requested:
            for x, y in requested.items():
                if x not in ignore:
                    setattr(theState, x, y)
            theState.save()
        else:
            abort(400, "Not a JSON")
        return jsonify(theState.to_dict()), 200
    else:
        abort(404)
