#!/usr/bin/python3
""" User API endpoints """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieve all User objects """
    return jsonify([user.to_dict() for user in storage.all("User").values()])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieve a specific User by ID """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Delete a User by ID """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a new User """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Update an existing User """
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200

