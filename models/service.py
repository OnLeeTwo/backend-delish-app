from db import db
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime, timedelta


def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)


class ServiceModel(db.Model):
    __tablename__ = "service"

    id = mapped_column(Integer, primary_key=True)
    overall_id = mapped_column(Integer, ForeignKey("overall_review.id"), unique=False, nullable=False)
    service_score = mapped_column(Integer, unique=False, nullable=True)
    service_comment = mapped_column(String(255), unique=False, nullable=True)
    created_at = mapped_column(DateTime, default=gmt_plus_7_now, nullable=False)
    updated_at = mapped_column(DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now, nullable=False)

    def __repr__(self):
        return f"<Service {self.id}>"

    def to_dictionaries(self):
        return {
            "id": self.id,
            "overall_id": self.overall_id,
            "service_score": self.service_score,
            "service_comment": self.service_comment,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
