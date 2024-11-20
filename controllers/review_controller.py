from flask import Blueprint, request, json
from flask_jwt_extended import jwt_required, get_jwt_identity

from urllib.parse import urlencode

from services.review_service import ReviewService
from .review_repository import ReviewRepository

review_blueprint = Blueprint("review_blueprint", __name__, url_prefix="/api")

review_service = ReviewService(ReviewRepository())


@review_blueprint.route("/reviews", methods=["POST"])
@jwt_required()
def create_review():
    try:
        data = request.get_json()
        is_valid, error_message = review_service.validate_review_data(data)

        if not is_valid:
            return {"error": error_message}, 400

        review, error = review_service.create_review(data, get_jwt_identity())

        if error:
            return {"error": error}, 409

        return {
            "message": "Review created successfully",
            "review_id": review["id"],
        }, 201

    except Exception as e:
        return {"error": str(e)}, 500


@review_blueprint.route("/reviews", methods=["GET"])
def get_reviews():
    try:
        # Get pagination parameters
        page = request.args.get("page", type=int, default=ReviewService.DEFAULT_PAGE)
        per_page = request.args.get(
            "per_page", type=int, default=ReviewService.DEFAULT_PER_PAGE
        )

        # Get filters
        filters = {
            "restaurant_id": request.args.get("restaurant_id", type=int),
            "user_id": request.args.get("user_id", type=int),
            "status": request.args.get("status"),
        }

        # Remove None values from filters
        filters = {k: v for k, v in filters.items() if v is not None}

        # Get paginated reviews
        reviews, pagination_meta = review_service.get_reviews_paginated(
            filters, page, per_page
        )

        # Generate pagination links
        def get_page_url(page_num):
            if page_num:
                params = request.args.copy()
                params["page"] = page_num
                return f"{request.base_url}?{urlencode(params)}"
            return None

        pagination_links = {
            "self": get_page_url(pagination_meta["page"]),
            "next": get_page_url(pagination_meta["next_page"]),
            "prev": get_page_url(pagination_meta["prev_page"]),
            "first": get_page_url(1),
            "last": get_page_url(pagination_meta["total_pages"]),
        }

        return {
            "reviews": [review.to_dictionaries() for review in reviews],
            "pagination": {
                "metadata": pagination_meta,
                "links": pagination_links,
            },
        }, 200

    except Exception as e:
        return {"message": "Database error occurred", "error": str(e)}, 500


@review_blueprint.route("/reviews/<int:review_id>", methods=["GET"])
def get_review(review_id):
    try:
        review = review_service.get_review(review_id)
        if not review:
            return {"message": "Review not found"}, 404

        return {"review": review.to_dictionaries()}, 200

    except Exception as e:
        return {"message": "Database error occurred", "error": str(e)}, 500


@review_blueprint.route("/reviews/<int:review_id>", methods=["PUT"])
@jwt_required()
def submit_review(review_id):
    try:
        review_data = request.form.get("data")
        if not review_data:
            return {"error": "Missing review data"}, 400

        review_data = json.loads(review_data)

        # Get files if any
        files = request.files.getlist("media")

        review, error = review_service.submit_review(
            review_id, review_data, files if files else None
        )

        if error:
            return {"error": error}, 409

        return {"message": "success submiting the review"}, 200
    except Exception as e:
        return {"error": str(e)}, (404)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON data"}, 400


@review_blueprint.route("/reviews/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):
    try:
        success, error = review_service.delete_review(review_id, get_jwt_identity())

        if not success:
            return {"error": error}, 404

        return {"message": "Review deleted successfully"}, 200

    except Exception as e:
        return {"message": "Database error occurred", "error": str(e)}, 500
