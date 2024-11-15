from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

review_blueprint = Blueprint("review_blueprint", __name__, url_prefix="/api")