#!/usr/bin/python3
"""
amenities routes
"""

from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def amentiyGet(amenity_id=None):
    """ amenity get """
    a_list = []
    a_id = "Amenity." + str(amenity_id)
    if amenity_id is None:
        theAmenities = storage.all(Amenity)
        if theAmenities:
            for x, y in theAmenities.items():
                a_list.append(y.to_dict())
    elif a_id in storage.all(Amenity).keys():
        return jsonify(storage.all(Amenity)[a_id].to_dict())
    else:
        abort(404)
    return jsonify(a_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """
    deletes an amenity
    """
    amen = storage.get(Amenity, amenity_id)
    if amen:
        amen.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities/", strict_slashes=False, methods=['POST'])
def post_amenities():
    """
    Post an amenity
    """
    requested = request.get_json()
    if requested is None:
        abort(400, "Not a JSON")
    if "name" not in requested:
        abort(400, "Missing name")
    amen = Amenity(**requested)
    amen.save()
    return jsonify(amen.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id=None):
    """
    Update
    """
    ignore = ['id', 'created_at', 'updated_at']
    amen = storage.get(Amenity, amenity_id)
    if amen:
        requested = request.get_json()
        if requested:
            for x, y in requested.items():
                if x not in ignore:
                    setattr(amen, x, y)
            amen.save()
        else:
            abort(400, "Not a JSON")
        return jsonify(amen.to_dict()), 200
    else:
        abort(404)
