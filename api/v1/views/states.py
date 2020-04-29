#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def statesGet():
    """ states """
    allList = [x.to_dict() for x in storage.all(State).items()]
    return jsonify(allList)


@app_views.route('/states/<state_id>', methods=['GET'])
def statesGetId(state_id):
    """ states """
    theState = storage.get(State, state_id)
    if theState:
        return jsonify(theState.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def statesDeleteId(state_id):
    """ states """
    theState = storage.get(State, state_id)
    if theState:
        storage.delete(theState)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def statesPost():
    """ states """
    print('test')
    requested = request.get_json()
    if requested:
        if 'name' in requested:
            newState = State(**requested)
            storage.new(newState)
        else:
            return 'Missing name', 400
    else:
        return 'Not a JSON', 400
    return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def statesPutId(state_id):
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
            return 'Not a JSON', 400
        return jsonify(theState.to_dict()), 200
    else:
        abort(404)
