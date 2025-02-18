# api/v1/views/__init__.py
from flask import Blueprint

# Create a Blueprint instance with the URL prefix /api/v1
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Wildcard import of everything in api.v1.views.index
from api.v1.views.index import *
