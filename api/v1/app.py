#!/usr/bin/python3
"""Flask app for API"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

# Enable CORS for all domains (for development purposes)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """Close storage after each request"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Returns JSON response for 404 errors"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)

