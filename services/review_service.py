from typing import List, Optional, Tuple, Dict
from controllers.review_repository import ReviewRepository

from models import OverallReviewModel
from enums.enum import ReviewStatusEnum
from werkzeug.datastructures import FileStorage

from services.upload import UploadFiles

from cerberus import Validator
from schemas.overall_review_schema import create_review_schema, submit_review_schema


class ReviewService:
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100

    def __init__(self, repository: ReviewRepository):
        self.repository = repository
        self.file_uploader = UploadFiles()

    def validate_review_data(self, data: dict) -> Tuple[bool, Optional[str]]:
        validator = Validator(create_review_schema)

        if not validator.validate(data):
            return False, validator.errors

        return True, None

    def create_review(self, data, user_id) -> Tuple[bool, Optional[str]]:
        # Check for existing review
        restaurant = self.repository.find_restaurant(data["restaurant_id"])
        if not restaurant:
            return None, "Restaurant ID not found!"

        existing_review = self.repository.find_by_user_and_restaurant(
            user_id, data["restaurant_id"]
        )
        if existing_review:
            return (
                None,
                "You already have a ongoing pending review for this restaurant",
            )

        # Create new review
        new_review = OverallReviewModel(
            restaurant_id=data["restaurant_id"],
            user_id=user_id,
            review_status=ReviewStatusEnum.pending,
        )

        return self.repository.create(new_review), None

    def get_reviews(self, filters: dict) -> List[OverallReviewModel]:
        return self.repository.find_all_filters(filters)

    def get_review(self, review_id: int) -> Optional[OverallReviewModel]:
        return self.repository.find_by_id(review_id)

    def get_reviews_paginated(
        self, filters: dict, page: int = DEFAULT_PAGE, per_page: int = DEFAULT_PER_PAGE
    ) -> Tuple[List[OverallReviewModel], Dict]:
        # Validate and sanitize pagination parameters
        page = max(1, page)  # Ensure page is at least 1
        per_page = min(
            max(1, per_page), self.MAX_PER_PAGE
        )  # Ensure per_page is between 1 and MAX_PER_PAGE

        # Convert status string to enum if present
        if filters.get("status"):
            try:
                filters["status"] = ReviewStatusEnum[filters["status"]]
            except KeyError:
                filters.pop("status")  # Remove invalid status from filters

        return self.repository.find_all_pagination(filters, page, per_page)

    def update_review(
        self, review_id: int, data: dict, user_id: int
    ) -> Tuple[Optional[OverallReviewModel], Optional[str]]:
        review = self.repository.find_by_id(review_id)

        if not review:
            return None, "Review not found"

        if review.user_id != user_id:
            return None, "Unauthorized to modify this review"

        review.score = data["score"]
        review.review_body = data["review_body"]

        return self.repository.update(review), None

    def delete_review(self, review_id: int, user_id: int) -> Tuple[bool, Optional[str]]:
        review = self.repository.find_by_id(review_id)

        if not review:
            return False, "Review not found"

        if review.user_id != user_id:
            return False, "Unauthorized to modify this review"

        self.repository.delete(review)
        return True, None

    def submit_review(
        self, review_id: int, data: dict, files: List[FileStorage] = None
    ):
        review = self.repository.find_by_id(review_id)
        if not review:
            return False, "Review with id {review_id} not found"

        review_validator = Validator(submit_review_schema)
        if not review_validator.validate(data):
            return False, review_validator.errors

        media_data = None
        if files:
            media_data = self._process_media_files(files)
            if isinstance(media_data, dict) and "errors" in media_data:
                error_messages = "\n".join(
                    [
                        f"{error['filename']}: {error['error']}"
                        for error in media_data["errors"]
                    ]
                )
                raise Exception(f"Error uploading media files:\n{error_messages}")

        return (
            self.repository.submit(
                review_id,
                data.get("review"),
                data.get("food"),
                data.get("service"),
                data.get("ambience"),
                media_data,
            ),
            None,
        )

    def _process_media_files(self, files: List[FileStorage]) -> List[dict]:
        media_data = []
        errors = []  # Collect errors

        for file in files:
            result = self.file_uploader.process_single_file(file)
            if "error" in result:
                errors.append({"filename": file.filename, "error": result["error"]})
            else:
                media_data.append({"location": result["file_url"]})

        if errors:
            return {"errors": errors}  # Return all errors
        return media_data
