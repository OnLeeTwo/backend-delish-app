from flask import Blueprint, request, jsonify
from db import db
from models.reservation import ReservationModel
from enums.enum import ReviewStatusEnum
from datetime import datetime

from connector.mysql_connectors import connect_db
from sqlalchemy.orm import sessionmaker

from flask_jwt_extended import get_jwt_identity, jwt_required

reservation_blueprint = Blueprint('reservation_blueprint', __name__,  url_prefix="/api")

engine = connect_db()

# Create a new reservation
@reservation_blueprint.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()

    try:
        user_id = get_jwt_identity()

        data = request.get_json()
        
        # Convert reservation_time string to Time object
        time_str = data.get('reservation_time')
        reservation_time = datetime.strptime(time_str, '%H:%M').time() if time_str else None
        
        new_reservation = ReservationModel(
            restaurant_id=data['restaurant_id'],
            user_id=user_id,
            number_of_people=data.get('number_of_people'),
            reservation_time=reservation_time,
            reservation_status=ReviewStatusEnum.completed 
        )
        
        s.add(new_reservation)
        s.commit()
        
        return jsonify({'message': 'Reservation created successfully', 
                       'reservation': new_reservation.to_dictionaries()}), 201
    except Exception as e:
        s.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        s.close()

# Read all reservations
@reservation_blueprint.route('/reservations', methods=['GET'])
def get_all_reservations():
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()

    try:
        reservations = s.query(ReservationModel).all()

        if reservations == None or reservations == []:
            return {"message": "Reservation not found"}, 404

        return jsonify([reservation.to_dictionaries() for reservation in reservations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        s.close()

# Read a specific reservation
@reservation_blueprint.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()
    try:
        reservation = s.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()

        if reservation == None or reservation == []:
            return {"message": "Reservation not found"}, 404
        return jsonify(reservation.to_dictionaries()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    finally:
        s.close()

# Update a reservation
@reservation_blueprint.route('/reservations/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()
    try:
        reservation = s.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()

        if reservation == None or reservation == []:
            return {"message": "Reservation not found"}, 404

        data = request.get_json()
        
        if 'restaurant_id' in data:
            reservation.restaurant_id = data['restaurant_id']
        if 'user_id' in data:
            reservation.user_id = data['user_id']
        if 'number_of_people' in data:
            reservation.number_of_people = data['number_of_people']
        if 'reservation_time' in data:
            time_str = data['reservation_time']
            reservation.reservation_time = datetime.strptime(time_str, '%H:%M').time()
        if 'reservation_status' in data:
            reservation.reservation_status = ReviewStatusEnum[data['reservation_status']]
        
        s.commit()
        return jsonify({'message': 'Reservation updated successfully',
                       'reservation': reservation.to_dictionaries()}), 200
    except Exception as e:
        s.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        s.close()

# Delete a reservation
@reservation_blueprint.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()
    try:
        reservation = s.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()

        if reservation == None or reservation == []:
            return {"message": "Reservation not found"}, 404

        s.delete(reservation)
        s.commit()
        return jsonify({'message': 'Reservation deleted successfully'}), 200
    except Exception as e:
        s.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        s.close()

# Optional: Get reservations by restaurant_id
@reservation_blueprint.route('/reservations/restaurant/<int:restaurant_id>', methods=['GET'])
def get_reservations_by_restaurant(restaurant_id):
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()
    try:
        reservations = s.query(ReservationModel).filter(ReservationModel.restaurant_id == restaurant_id).all()
        
        if reservations == None or reservations == []:
            return {"message": "Reservation not found"}, 404

        return jsonify([reservation.to_dictionaries() for reservation in reservations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        s.close()

# Optional: Get reservations by user_id
@reservation_blueprint.route('/reservations/user/<int:user_id>', methods=['GET'])
def get_reservations_by_user(user_id):
    Session = sessionmaker(bind=engine)
    s = Session()
    s.begin()
    try:
        reservations = s.query(ReservationModel).filter(ReservationModel.user_id == user_id).all()

        if reservations == None or reservations == []:
            return {"message": "Reservation not found"}, 404

        return jsonify([reservation.to_dictionaries() for reservation in reservations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        s.close()
