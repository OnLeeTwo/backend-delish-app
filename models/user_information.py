from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey
from datetime import datetime, timedelta


def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)


class UserInformationModel(db.Model):
    __tablename__ = "user_information"

    id = mapped_column(Integer, primary_key=True)
    city_id = mapped_column(Integer, ForeignKey("city.id"), unique=False, nullable=False)
    user_id = mapped_column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    name = mapped_column(String(255), unique=False, nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    phone_number = mapped_column(String(255), unique=True, nullable=False)
    address = mapped_column(String(255), unique=False, nullable=True)
    created_at = mapped_column(DateTime, default=gmt_plus_7_now, nullable=False)
    updated_at = mapped_column(DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now, nullable=False)

    def __repr__(self):
        return f"<User Information {self.id}>"

    def to_dictionaries(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
