#!/usr/bin/python3
""" Start Flask app, setup Blueprint """

from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import (app_views, states, cities,
                          amenities, places, users, reviews)
import os

app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix="/api/v1")
app.register_blueprint(states, url_prefix="/api/v1/states")
app.register_blueprint(cities, url_prefix="/api/v1/cities")
app.register_blueprint(users, url_prefix="/api/v1/users")
app.register_blueprint(amenities, url_prefix="/api/v1/amenities")
app.register_blueprint(places, url_prefix="/api/v1/places")
app.register_blueprint(reviews, url_prefix="/api/v1/reviews")


@app.teardown_appcontext
def close(f):
    """ app teardown """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ 404 alternate """
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    # set host and port using environ variables if not defined
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    # Run the flask server
    app.run(host=host, port=port, threaded=True)
