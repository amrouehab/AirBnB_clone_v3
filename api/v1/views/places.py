#!/usr/bin/python3
""" Place API endpoints """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Retrieve all places of a city """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieve a specific Place by ID """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Delete a Place by ID """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Create a new Place """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    user = storage.get("User", data["user_id"])
    if not user:
        abort(404)

    place = Place(**data)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201

