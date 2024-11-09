from db import db
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, Time, ForeignKey, DateTime, Enum
from datetime import datetime, timedelta
from .enums import ReviewStatusEnum


def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)


class ReservationModel(db.Model):
    __tablename__ = "reservation"

    id = mapped_column(Integer, primary_key=True)
    restaurant_id = mapped_column(Integer, ForeignKey("restaurant.id"), unique=False, nullable=False)
    user_id = mapped_column(Integer, ForeignKey("user.id"), unique=False, nullable=False)
    number_of_people = mapped_column(Integer, unique=False, nullable=True)
    reservation_time = mapped_column(Time, unique=False, nullable=True)
    reservation_status = mapped_column(
        Enum(ReviewStatusEnum), default=ReviewStatusEnum.pending, unique=False, nullable=True
    )
    created_at = mapped_column(DateTime, default=gmt_plus_7_now, nullable=False)
    updated_at = mapped_column(DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now, nullable=False)

    def __repr__(self):
        return f"<Reservation {self.id}>"

    def to_dictionaries(self):
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "user_id": self.user_id,
            "number_of_people": self.number_of_people,
            "reservation_time": self.reservation_time,
            "reservation_status": self.reservation_status.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
