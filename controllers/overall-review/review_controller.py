from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

# REST Management

review_blueprint = Blueprint("review_blueprint", __name__, url_prefix="/api/review")

@review_blueprint.route("/user", methods=["GET"])
@jwt_required()
def user_information():
    current_user = get_jwt_identity()
    user_id = current_user.get(id)
    return user_id


# @review_blueprint.route("/create", methods=["GET"])
# def create_overall_review():
#     data = 