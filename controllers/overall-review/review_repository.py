from models import OverallReviewModel
from connector.mysql_connectors import connect_db
from sqlalchemy.orm import sessionmaker
from flask import jsonify
from db import db

# DB Interaction

class ReviewRepository:
    def __init__(self, db=db, review=OverallReviewModel):
        self.db = db
        self.review = review

    def create_review(self, data):
        return self.review(**data)
    
    def get_reviews_by_user_id(self, user, page=1, per_page=10):
        Session = sessionmaker(bind = connect_db())
        s = Session()
        s.begin()

        try:
            if not user.id:
                raise ValueError
            
            reviews_query = s.query(OverallReviewModel).filter(OverallReviewModel.user_id == user.id)
            reviews = reviews_query.order_by(OverallReviewModel.created_at.desc()).offset((page-1) * per_page).limit(per_page).all()

            return jsonify({
                "page": page,
                "offset": per_page,
                "reviews": [review.create_review() for review in reviews]
            }), 200
        
        except ValueError as e:
            return jsonify({"error": "User not found"}), 404
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        finally:
            s.close()

    def get_reviews_by_restaurant_id(self, restaurant, page=1, per_page=10):
        Session = sessionmaker(bind = connect_db())
        s = Session()
        s.begin()

        try:
            if not restaurant.id:
                raise ValueError

            reviews_query = s.query(OverallReviewModel).filter(OverallReviewModel.restaurant_id == restaurant.id)
            reviews = reviews_query.order_by(OverallReviewModel.created_at.desc()).offset((page-1) * per_page).limit(per_page).all() 
            
            return jsonify({
                "page": page,
                "offset": per_page,
                "reviews": [review.create_review() for review in reviews]
            }), 200
        
        except ValueError as e:
            return {"error": "Restaurant not found"}, 400
        
        except Exception as e:
            return {"error": str(e)}, 500
        
        finally:
            s.close()