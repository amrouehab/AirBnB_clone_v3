#!/usr/bin/python3
""" Amenity API endpoints """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieve all Amenity objects """
    return jsonify([amenity.to_dict() for amenity in storage.all("Amenity").values()])

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieve a specific Amenity by ID """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete an Amenity by ID """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Create a new Amenity """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an existing Amenity """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200

