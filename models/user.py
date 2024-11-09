from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from datetime import datetime, timedelta
import bcrypt
from flask_login import UserMixin


def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)


class UserModel(db.Model, UserMixin):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(255), unique=True, nullable=False)
    password = mapped_column(String(255), unique=False, nullable=False)
    pin = mapped_column(Integer, unique=False, nullable=False)
    created_at = mapped_column(DateTime, default=gmt_plus_7_now, nullable=False)
    updated_at = mapped_column(DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now, nullable=False)

    user_information = relationship("UserInformationModel", backref="user", lazy=True, uselist=False)
    overall_review = relationship("OverallReviewModel", backref="user", lazy=True)
    reservation = relationship("ReservationModel", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.id}>"

    def to_dictionaries(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def set_pin(self, pin):
        self.pin = bcrypt.hashpw(pin.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_pin(self, pin):
        return bcrypt.checkpw(pin.encode("utf-8"), self.pin.encode("utf-8"))
