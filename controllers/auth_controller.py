from flask import Blueprint, request
from flask_cors import cross_origin
from connector.mysql_connectors import connect_db
from models.user import UserModel
from models.user_information import UserInformationModel
from models.city import CityModel
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_login import logout_user, login_user, current_user
from cerberus import Validator
from schemas.user_schema import login_email_schema, login_phone_schema, register_schema, update_profile_schema
from utils.handle_response import ResponseHandler

auth_blueprint = Blueprint("auth_blueprint", __name__)
revoked_tokens = set()


@auth_blueprint.post("/api/register")
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
def register():
    Session = sessionmaker(bind=connect_db())
    s = Session()
    s.begin()

    try:
        data = request.get_json()  # Get input data
        validator = Validator(register_schema)

        # Check data is valid or invalid
        if not validator.validate(data):
            return ResponseHandler.error(message="Data Invalid!", data=validator.errors, status=400)

        # Check if the username is exists in database
        existing_username = s.query(UserModel).filter((UserModel.username == data["username"])).first()
        if existing_username:
            return ResponseHandler.error(message="Username is already exists!", status=409)

        # Check if the email is exists in database
        existing_email = s.query(UserInformationModel).filter((UserInformationModel.email == data["email"])).first()
        if existing_email:
            return ResponseHandler.error(message="Email is taken!", status=409)

        # Check if the phone number is exists in database
        existing_phone_number = (
            s.query(UserInformationModel).filter((UserInformationModel.phone_number == data["phone_number"])).first()
        )
        if existing_phone_number:
            return ResponseHandler.error(message="Phone number is taken!", status=409)

        # Check if the inputted city is available in database
        city = s.query(CityModel).filter((CityModel.city == data["city_name"])).first()
        if not city:
            return ResponseHandler.error(message="City name is not available!", status=409)

        # Create new user
        new_user = UserModel(
            username=data["username"],
        )
        new_user.set_password(data["password"])
        new_user.set_pin(data["pin"])  # Cannot hash pin because the data type is integer
        s.add(new_user)
        s.flush()  # Populate the user.id with auto increment-value

        # Create user information
        new_user_info = UserInformationModel(
            city_id=city.id,
            user_id=new_user.id,
            name=data["name"],
            email=data["email"],
            address=data["address"],
            phone_number=data["phone_number"],
        )
        s.add(new_user_info)
        s.commit()

        user_information = {
            "user_id": new_user.id,
            "username": new_user.username,
            "name": new_user_info.name,
            "email": new_user_info.email,
            "address": new_user_info.address,
            "phone_number": new_user_info.phone_number,
        }

        return ResponseHandler.success(data=user_information, status=201)

    except Exception as e:
        s.rollback()
        return ResponseHandler.error(
            message="An error occurred while registering new account",
            data=str(e),
            status=500,
        )

    finally:
        s.close()


@auth_blueprint.post("/api/login-with-email")
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
def login_email():
    Session = sessionmaker(bind=connect_db())
    s = Session()
    s.begin()

    try:
        data = request.get_json()  # Get input data
        validator = Validator(login_email_schema)

        # Check data is valid or invalid
        if not validator.validate(data):
            return ResponseHandler.error(message="Data Invalid!", data=validator.errors, status=400)

        user_info = s.query(UserInformationModel).filter(UserInformationModel.email == data["email"]).first()
        if user_info == None:
            return ResponseHandler.error(message="Email not found!", status=404)

        user = s.query(UserModel).filter(UserModel.id == user_info.user_id).first()

        # Checking if the user is available or pin invalid
        if user == None:
            return ResponseHandler.error(message="User not found!", status=404)
        if not user.check_password(data["password"]):
            return ResponseHandler.error(message="Invalid password!", status=400)

        login_user(user)
        access_token = create_access_token(identity=user.id)

        return ResponseHandler.success(
            data={"access_token": access_token},
            message="Login Success!",
            status=200,
        )

    except Exception as e:
        s.rollback()
        return ResponseHandler.error(
            message="Login failed!",
            data=str(e),
            status=500,
        )

    finally:
        s.close()


@auth_blueprint.post("/api/login-with-phone")
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
def login_phone_number():
    Session = sessionmaker(bind=connect_db())
    s = Session()
    s.begin()

    try:
        data = request.get_json()  # Get input data
        validator = Validator(login_phone_schema)

        # Check data is valid or invalid
        if not validator.validate(data):
            return ResponseHandler.error(message="Data Invalid!", data=validator.errors, status=400)

        user_info = (
            s.query(UserInformationModel).filter(UserInformationModel.phone_number == data["phone_number"]).first()
        )
        if user_info == None:
            return ResponseHandler.error(message="Phone number not found!", status=404)

        user = s.query(UserModel).filter(UserModel.id == user_info.user_id).first()

        # Checking if the user is available or pin invalid
        if user == None:
            return ResponseHandler.error(message="User not found!", status=404)
        if not user.check_pin(data["pin"]):
            return ResponseHandler.error(message="Invalid pin!", status=400)

        login_user(user)
        access_token = create_access_token(identity=user.id)

        return ResponseHandler.success(
            data={"access_token": access_token},
            message="Login success!",
            status=200,
        )

    except Exception as e:
        s.rollback()
        return ResponseHandler.error(
            message="Login failed!",
            data=str(e),
            status=500,
        )

    finally:
        s.close()


@auth_blueprint.get("/api/logout")
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Get the unique identifier of the token
    revoked_tokens.add(jti)  # Add the token's jti to the revoked tokens set

    if current_user.is_authenticated:
        user_info = {"id": current_user.id, "username": current_user.username}
        logout_user()
        return ResponseHandler.success(data={"message": "Logout success!", "user": user_info}, status=200)
    else:
        return ResponseHandler.success(data={"message": "User already logged out or not logged in."}, status=200)


@auth_blueprint.get("/api/profile")
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
@jwt_required()
def show_profile():
    user_id = get_jwt_identity()
    Session = sessionmaker(bind=connect_db())
    s = Session()

    try:
        user = s.query(UserModel).filter(UserModel.id == user_id).first()
        user_info = s.query(UserInformationModel).filter(UserInformationModel.user_id == user_id).first()
        if user is None or user_info is None:
            return ResponseHandler.error(message="User not found!", status=404)

        city = s.query(CityModel).filter(CityModel.id == UserInformationModel.city_id).first()

        user_data = {
            "id": user.id,
            "user_info_id": user_info.id,
            "username": user.username,
            "name": user_info.name,
            "email": user_info.email,
            "address": user_info.address,
            "phone_number": user_info.phone_number,
            "city": city.city,
        }

        return ResponseHandler.success(data=user_data, status=200)

    except Exception as e:
        s.rollback()
        return ResponseHandler.error(
            message="Show Profile Failed!",
            data=str(e),
            status=500,
        )

    finally:
        s.close()


@auth_blueprint.put("/api/profile")
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    Session = sessionmaker(bind=connect_db())
    s = Session()
    s.begin()

    try:
        data = request.get_json()  # Get input data
        validator = Validator(update_profile_schema)

        # Check data is valid or invalid
        if not validator.validate(data):
            return ResponseHandler.error(message="Data Invalid!", data=validator.errors, status=400)

        user = s.query(UserModel).filter(UserModel.id == user_id).first()
        user_info = s.query(UserInformationModel).filter(UserInformationModel.user_id == user_id).first()
        if user is None or user_info is None:
            return ResponseHandler.error(message="User not found!", status=404)

        if "email" in data:
            # Check if the email already exists
            new_email = data.get("email")
            existing_email = (
                s.query(UserInformationModel)
                .filter(UserInformationModel.email == new_email, UserInformationModel.user_id != user_id)
                .first()
            )
            if existing_email:
                return ResponseHandler.error(message="Email already exists", status=409)
            else:
                user_info.email = new_email

        if "username" in data:
            # Check if the username already exists
            new_username = data.get("username")
            existing_username = (
                s.query(UserModel).filter(UserModel.username == new_username, UserModel.id != user_id).first()
            )
            if existing_username:
                return ResponseHandler.error(message="Username already exists", status=409)
            else:
                user.username = new_username

        if "phone_number" in data:
            # Check if the username already exists
            new_phone_number = data.get("phone_number")
            existing_phone_number = (
                s.query(UserInformationModel)
                .filter(UserInformationModel.phone_number == new_phone_number, UserInformationModel.id != user_id)
                .first()
            )
            if existing_phone_number:
                return ResponseHandler.error(message="Phone number already exists", status=409)
            else:
                user_info.phone_number = new_phone_number

        if "city_name" in data:
            # Check if the city name exists
            new_city = data.get("city_name")
            city = s.query(CityModel).filter(CityModel.city == new_city).first()
            if not city:
                return ResponseHandler.error(message="City unavailable!", status=409)
            else:
                user_info.city_id = city.id
        else:
            city = s.query(CityModel).filter(CityModel.id == user_info.city_id).first()

        if "password" in data:
            password = data.get("password")
            user.set_password(password)

        if "name" in data:
            user_info.name = data["name"]
        if "pin" in data:
            user.pin = data["pin"]
        if "address" in data:
            user_info.address = data["address"]

        s.commit()
        updated_user = {
            "id": user.id,
            "user_info_id": user_info.id,
            "username": user.username,
            "name": user_info.name,
            "email": user_info.email,
            "address": user_info.address,
            "city": city.city,
        }

        return ResponseHandler.success(data=updated_user, status=200)

    except Exception as e:
        s.rollback()
        return ResponseHandler.error(
            message="An error occurred while updating the profile",
            data=str(e),
            status=500,
        )

    finally:
        s.close()
