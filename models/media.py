from db import db
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, Text, ForeignKey, DateTime
from datetime import datetime, timedelta


def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)


class MediaModel(db.Model):
    __tablename__ = "media"

    id = mapped_column(Integer, primary_key=True)
    overall_id = mapped_column(Integer, ForeignKey("overall_review.id"), unique=False, nullable=False)
    location = mapped_column(Text, unique=False, nullable=True)  # Stored as link
    created_at = mapped_column(DateTime, default=gmt_plus_7_now, nullable=False)
    updated_at = mapped_column(DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now, nullable=False)

    def __repr__(self):
        return f"<Media {self.id}>"

    def to_dictionaries(self):
        return {
            "id": self.id,
            "overall_id": self.overall_id,
            "location": self.location,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
