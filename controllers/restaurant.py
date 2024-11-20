from flask import Blueprint, jsonify, request
from connector.mysql_connectors import connect_db
from models.restaurant import RestaurantModel
from datetime import time

from flask_jwt_extended import (
    jwt_required
)

from sqlalchemy.orm import sessionmaker

restaurant_routes = Blueprint("restaurant_routes", __name__)

engine = connect_db()


@restaurant_routes.route("/restaurants", methods=["POST"])
@jwt_required()
def create_restaurant():
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()

    data = request.get_json()
    if data is None or not isinstance(data, dict):
        return jsonify({"message": "Invalid data provided"}), 400

    required_fields = [
        "city_id",
        "restaurant_name",
        "restaurant_status",
        "open_time",
        "closed_time",
    ]

    for field in required_fields:
        if field not in data:
            return (
                jsonify({"message": f"{field.replace('_', ' ').title()} is required"}),
                400,
            )

    try:
        NewRestaurant = RestaurantModel(
            city_id=data.get("city_id"),
            restaurant_name=data.get("restaurant_name"),
            restaurant_status=data.get("restaurant_status"),
            open_time=data.get("open_time"),
            closed_time=data.get("closed_time"),
        )

        s.add(NewRestaurant)
        s.commit()

    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Failed to Add Restaurant"}, 500

    return {"message": "Restaurant Added"}, 200


@restaurant_routes.route("/restaurants", methods=["GET"])
def get_restaurants():
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()

    try:
        restaurants = s.query(RestaurantModel).all()

        restaurant_list = [
            {
                "id": r.id,
                "city_id": r.city_id,
                "restaurant_name": r.restaurant_name,
                "restaurant_status": r.restaurant_status,
                "open_time": (
                    r.open_time.strftime("%H:%M:%S")
                    if isinstance(r.open_time, time)
                    else r.open_time
                ),
                "closed_time": (
                    r.closed_time.strftime("%H:%M:%S")
                    if isinstance(r.closed_time, time)
                    else r.closed_time
                ),
            }
            for r in restaurants
        ]

        return {"restaurants": restaurant_list}, 200

    except Exception as e:
        print(e)
        return {"message": "Unexpected Error"}, 500


@restaurant_routes.route("/restaurants/<id>", methods=["GET"])
def get_restaurant(id):
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()

    try:
        restaurant = s.query(RestaurantModel).filter(RestaurantModel.id == id).first()

        if restaurant == None:
            return {"message": "Restaurant not found"}, 404

        restaurant = {
            "id": restaurant.id,
            "city_id": restaurant.city_id,
            "restaurant_name": restaurant.restaurant_name,
            "restaurant_status": restaurant.restaurant_status,
            "open_time": (
                restaurant.open_time.strftime("%H:%M:%S")
                if isinstance(restaurant.open_time, time)
                else restaurant.open_time
            ),
            "closed_time": (
                restaurant.closed_time.strftime("%H:%M:%S")
                if isinstance(restaurant.closed_time, time)
                else restaurant.closed_time
            ),
        }

        return {"restaurant": restaurant}, 200

    except Exception as e:
        print(e)
        return {"message": "Unexpected Error"}, 500


@restaurant_routes.route("/restaurants/<id>", methods=["PUT"])
def update_restaurant(id):
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()

    try:
        restaurant = s.query(RestaurantModel).filter(RestaurantModel.id == id).first()

        if restaurant == None:
            return {" message": "Restaurant not found"}, 404

        data = request.json

        restaurant.city_id = data["city_id"]
        restaurant.restaurant_name = data["restaurant_name"]
        restaurant.restaurant_status = data["restaurant_status"]
        restaurant.open_time = data["open_time"]
        restaurant.closed_time = data["closed_time"]

        s.commit()
        return {"message": "Update Restaurant Success"}, 200

    except Exception as e:
        print(str(e))
        s.rollback()
        return {"message": "Update Failed", "error": str(e)}, 500


@restaurant_routes.route("/restaurants/<id>", methods=["DELETE"])
def delete_restaurant(id):
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()

    try:
        restaurant = s.query(RestaurantModel).filter(RestaurantModel.id == id).first()

        if restaurant == None:
            return {"message": "Restaurant not found"}, 403

        s.delete(restaurant)
        s.commit()
        return {"message": "Restaurant Deleted"}, 200

    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Delete Failed"}, 500
