#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieves the list of all State objects."""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "Not a page")
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "Not a page")
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "Not a page")
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
