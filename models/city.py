from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from datetime import datetime, timedelta


def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)


class CityModel(db.Model):
    __tablename__ = "city"

    id = mapped_column(Integer, primary_key=True)
    city = mapped_column(String(255), unique=False, nullable=False)
    created_at = mapped_column(DateTime, default=gmt_plus_7_now, nullable=False)
    updated_at = mapped_column(DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now, nullable=False)

    user_information = relationship("UserInformationModel", backref="city", lazy=True)
    restaurant = relationship("RestaurantModel", backref="city", lazy=True)

    def __repr__(self):
        return f"<City {self.id}>"

    def to_dictionaries(self):
        return {
            "id": self.id,
            "city": self.city,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
