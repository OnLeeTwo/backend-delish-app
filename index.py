from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from config.config import Config
from sqlalchemy.orm import sessionmaker

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

from controller.city_controller import city_blueprint
from controller.auth_controller import auth_blueprint, revoked_tokens

from flask_cors import CORS


from controllers.upload import upload_routes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(upload_routes)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = "your_secret_key_here"
    jwt = JWTManager(app)

    CORS(
        app,
        origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        supports_credentials=True,
        methods=["*"],
        resources={r"/*": {"origins": "*"}},
        allow_headers=["Content-Type", "Authorization", "XCSRF-Token"],
    )

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in revoked_tokens

    db.init_app(app)
    Migrate(app, db)
    connect_db()

    init_login_manager(app)
    register_blueprints(app)

    @app.route("/")
    def hello_world():
        return "Hello World"

    return app


def register_blueprints(app):
    app.register_blueprint(city_blueprint)
    app.register_blueprint(auth_blueprint)


def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        Session = sessionmaker(connect_db())
        s = Session()
        try:
            return s.query(UserModel).get(int(user_id))
        finally:
            s.close()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
