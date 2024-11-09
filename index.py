from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from config.config import Config

from db import db
from connector.mysql_connectors import connect_db
from models.user import UserModel
from models.city import CityModel
from models.user_information import UserInformationModel
from models.restaurant import RestaurantModel
from models.overall_review import OverallReviewModel
from models.reservation import ReservationModel
from models.media import MediaModel
from models.food import FoodModel
from models.service import ServiceModel
from models.ambience import AmbienceModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    connect_db()

    @app.route("/")
    def hello_world():
        return "Hello World"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
