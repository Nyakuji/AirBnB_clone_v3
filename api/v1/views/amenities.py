#!/usr/bin/python3
"""amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    """Retrieves a list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    list_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    amenity_obj.remove(amenity_obj[0])
    for obj in all_amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """Creates an Amenity"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    # Check if amenity_id is linked to any Amenity object
    if amenity is None:
        abort(404)

    # Check if the request body is valid JSON
    if not request.is_json:
        abort(400, description='Not a JSON')

    # Get the JSON data from the request body
    data = request.get_json()

    # Update the Amenity object with valid key-value pairs
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    # Save the updated Amenity object
    amenity.save()

    # Return the updated Amenity object with status code 200
    return jsonify(amenity.to_dict()), 200
