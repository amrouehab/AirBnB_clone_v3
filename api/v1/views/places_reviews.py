#!/usr/bin/python3
""" Review API endpoints """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ Retrieve all reviews of a place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieve a specific Review by ID """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ Create a new Review """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    review = Review(**data)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201

