from flask import Blueprint, request
from connector.mysql_connectors import connect_db
from models.city import CityModel
from sqlalchemy.orm import sessionmaker
from schemas.city_schema import add_city_schema
from cerberus import Validator
from utils.handle_response import ResponseHandler

city_blueprint = Blueprint("city_blueprint", __name__)


@city_blueprint.post("/api/city")
def add_city():
    Session = sessionmaker(bind=connect_db())
    s = Session()
    s.begin()

    try:
        data = request.get_json()
        validator = Validator(add_city_schema)

        if not validator.validate(data):
            return ResponseHandler.error(message="Data Invalid!", data=validator.errors, status=400)

        city = data.get("city")

        new_city = CityModel(city=city)

        s.add(new_city)
        s.commit()

        return ResponseHandler.success(
            message="City added successfully",
            data=new_city.to_dictionaries(),
            status=201,
        )

    except Exception as e:
        s.rollback()
        return ResponseHandler.error(
            message="An error occurred while adding the city",
            data=str(e),
            status=500,
        )

    finally:
        s.close()


@city_blueprint.get("/api/city")
def show_all_city():
    try:
        cities = CityModel.query.all()
        cities_list = [city.to_dictionaries() for city in cities]

        response_data = {"cities": cities_list}

        return ResponseHandler.success(data=response_data, status=200)

    except Exception as e:
        return ResponseHandler.error(
            message="An error occurred while showing cities",
            data=str(e),
            status=500,
        )
