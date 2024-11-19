from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Time, ForeignKey, DateTime
from datetime import datetime, timedelta


def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)


class RestaurantModel(db.Model):
    __tablename__ = "restaurant"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id = mapped_column(Integer, ForeignKey("city.id"), unique=False, nullable=False)
    restaurant_name = mapped_column(String(255), unique=False, nullable=False)
    restaurant_status = mapped_column(Boolean, unique=False, nullable=False)  # True: Open, False: Close
    open_time = mapped_column(Time, unique=False, nullable=False)
    closed_time = mapped_column(Time, unique=False, nullable=False)
    created_at = mapped_column(DateTime, default=gmt_plus_7_now, nullable=False)
    updated_at = mapped_column(DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now, nullable=False)

    overall_review = relationship("OverallReviewModel", backref="restaurant", lazy=True)
    reservation = relationship("ReservationModel", backref="restaurant", lazy=True)

    def __repr__(self):
        return f"<Restaurant {self.id}>"

    def to_dictionaries(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "restaurant_name": self.restaurant_name,
            "restaurant_status": self.restaurant_status,
            "open_time": self.open_time,
            "closed_time": self.closed_time,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
