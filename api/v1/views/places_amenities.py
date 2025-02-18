#!/usr/bin/python3
""" Places-Amenities view for the API """
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from werkzeug.exceptions import NotFound

@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_of_place(place_id):
    """ Retrieves all Amenity objects linked to a specific Place """
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound(f"Place {place_id} not found")
    
    # Get all amenities linked to the place and return as a list of dictionaries
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def unlink_amenity_from_place(place_id, amenity_id):
    """ Unlinks an Amenity from a Place """
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound(f"Place {place_id} not found")
    
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        raise NotFound(f"Amenity {amenity_id} not found")
    
    if amenity not in place.amenities:
        raise NotFound(f"Amenity {amenity_id} not linked to Place {place_id}")
    
    # Remove the amenity from the place
    place.amenities.remove(amenity)
    storage.save()  # Save the changes to the database or file storage
    
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """ Links an Amenity to a Place """
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound(f"Place {place_id} not found")
    
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        raise NotFound(f"Amenity {amenity_id} not found")
    
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200  # Amenity already linked
    
    # Link the amenity to the place
    place.amenities.append(amenity)
    storage.save()  # Save the changes to the database or file storage
    
    return jsonify(amenity.to_dict()), 201

