#!/usr/bin/python3
""" State API endpoints """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieve all State objects """
    return jsonify([state.to_dict() for state in storage.all("State").values()])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieve a specific State by ID """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Delete a State by ID """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create a new State """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update an existing State """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200

