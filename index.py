from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from config.config import Config
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from datetime import timedelta
from db import db
from connector.mysql_connectors import connect_db
from models.user import UserModel

import os

from controllers.city_controller import city_blueprint
from controllers.auth_controller import auth_blueprint, revoked_tokens
from controllers.restaurant import restaurant_routes
from controllers.review_controller import review_blueprint

from flask_cors import CORS

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = "your_secret_key_here"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=8)
    jwt = JWTManager(app)

    CORS(
        app,
        origins=["*"],
        supports_credentials=True,
        methods=["*"],
        resources={r"/*": {"origins": "*"}},
        allow_headers=["Content-Type", "Authorization", "XCSRF-Token"],
    )

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in revoked_tokens
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return ({"message": "Token has expired", "error": "token_expired"}), 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            ({"message": "Signature verification failed", "error": "invalid_token"}),
            401,
        )


    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            (
                {
                    "message": "Request doesnt contain valid token",
                    "error": "authorization_header",
                }
            ),
            401,
        )

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
    app.register_blueprint(restaurant_routes)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(review_blueprint)


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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
