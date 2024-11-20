from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey, DateTime, Enum
from datetime import datetime, timedelta
from enums.enum import ReviewStatusEnum


def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)


class OverallReviewModel(db.Model):
    __tablename__ = "overall_review"

    id = mapped_column(Integer, primary_key=True)
    restaurant_id = mapped_column(
        Integer, ForeignKey("restaurant.id"), unique=False, nullable=False
    )
    user_id = mapped_column(
        Integer, ForeignKey("user.id"), unique=False, nullable=False
    )
    score = mapped_column(Integer, unique=False, nullable=True)
    review_status = mapped_column(
        Enum(ReviewStatusEnum),
        default=ReviewStatusEnum.pending,
        unique=False,
        nullable=False,
    )
    review_body = mapped_column(Text, unique=False, nullable=True)
    created_at = mapped_column(DateTime, default=gmt_plus_7_now, nullable=False)
    updated_at = mapped_column(
        DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now, nullable=False
    )

    media = relationship("MediaModel", backref="overall_review", lazy="joined")
    food = relationship("FoodModel", backref="overall_review", lazy=True)
    service = relationship("ServiceModel", backref="overall_review", lazy=True)
    ambience = relationship("AmbienceModel", backref="overall_review", lazy=True)

    def __repr__(self):
        return f"<Overall Review {self.id}>"

    def to_dictionaries(self, include_media=False):
        review_dict = {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "user_id": self.user_id,
            "score": self.score,
            "review_status": self.review_status.name,
            "review_body": self.review_body,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        
        if include_media:
            review_dict["media_urls"] = [media.location for media in self.media] if self.media else []
    
        return review_dict
