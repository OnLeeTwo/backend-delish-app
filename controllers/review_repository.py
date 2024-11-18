from typing import List, Optional, Tuple
from connector.mysql_connectors import connect_db
from sqlalchemy.orm import sessionmaker
from models import OverallReviewModel
from models.ambience import AmbienceModel
from models.food import FoodModel
from models.service import ServiceModel
from models.media import MediaModel
from models.restaurant import RestaurantModel

from models.enums import ReviewStatusEnum


def get_session():
    Session = sessionmaker(bind=connect_db())
    return Session()


class ReviewRepository:
    def create(self, review: OverallReviewModel) -> dict:
        s = get_session()
        s.begin()

        try:
            s.add(review)
            s.commit()
            result = review.to_dictionaries()
            return result
        except Exception as e:
            s.rollback()
            raise e
        finally:
            s.close()

    def find_by_id(self, review_id: int) -> Optional[OverallReviewModel]:
        s = get_session()
        s.begin()
        try:
            return s.query(OverallReviewModel).get(review_id)
        except Exception as e:
            raise e
        finally:
            s.close()

    def find_by_user_and_restaurant(
        self, user_id: int, restaurant_id: int
    ) -> Optional[OverallReviewModel]:
        s = get_session()
        s.begin()

        try:
            return (
                s.query(OverallReviewModel)
                .filter_by(user_id=user_id, restaurant_id=restaurant_id)
                .first()
            )
        except Exception as e:
            raise e
        finally:
            s.close()

    def find_restaurant(self, restaurant_id):
        s = get_session()
        s.begin()

        try:
            return s.query(RestaurantModel).filter_by(id=restaurant_id).first()
        except Exception as e:
            raise e
        finally:
            s.close()

    def find_all_pagination(
        self, filters: dict, page: int, per_page: int
    ) -> Tuple[List[OverallReviewModel], dict]:

        s = get_session()
        s.begin()

        try:
            query = s.query(OverallReviewModel)
            if filters.get("restaurant_id"):
                query = query.filter(
                    OverallReviewModel.restaurant_id == filters["restaurant_id"]
                )
            if filters.get("user_id"):
                query = query.filter(OverallReviewModel.user_id == filters["user_id"])
            if filters.get("status"):
                query = query.filter(
                    OverallReviewModel.review_status == filters["status"]
                )

            total_items = query.count()

            total_pages = (total_items + per_page - 1) // per_page
            offset = (page - 1) * per_page

            reviews = (
                query.order_by(OverallReviewModel.created_at.desc())
                .offset(offset)
                .limit(per_page)
                .all()
            )

            pagination_meta = {
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "total_items": total_items,
                "has_next": page < total_pages,
                "has_prev": page > 1,
                "next_page": page + 1 if page < total_pages else None,
                "prev_page": page - 1 if page > 1 else None,
            }

            return reviews, pagination_meta
        except Exception as e:
            raise e
        finally:
            s.close()

    def find_all_filters(self, filters: dict) -> List[OverallReviewModel]:
        s = get_session()
        s.begin()
        try:
            query = s.query(OverallReviewModel)
            if filters.get("restaurant_id"):
                query = query.filter(
                    OverallReviewModel.restaurant_id == filters["restaurant_id"]
                )
            if filters.get("user_id"):
                query = query.filter(OverallReviewModel.user_id == filters["user_id"])
            if filters.get("status"):
                query = query.filter(
                    OverallReviewModel.review_status == filters["status"]
                )

            return query.all()
        except Exception as e:
            raise e
        finally:
            s.close()

    def update(self, review: OverallReviewModel) -> OverallReviewModel:
        s = get_session()
        s.begin()

        try:
            s.commit()
            return review
        except Exception as e:
            s.rollback()
            raise e
        finally:
            s.close()

    @staticmethod
    def submit(
        review_id,
        review_data,
        food_data=None,
        service_data=None,
        ambience_data=None,
        media_data=None,
    ):
        s = get_session()
        s.begin()

        try:
            review = s.query(OverallReviewModel).get(review_id)
            if review:
                review.review_status = ReviewStatusEnum.completed

                for key, value in review_data.items():
                    setattr(review, key, value)

                food_review = FoodModel(overall_id=review_id, **food_data)
                s.add(food_review)

                service_review = ServiceModel(overall_id=review_id, **service_data)
                s.add(service_review)

                ambience_review = AmbienceModel(overall_id=review_id, **ambience_data)
                s.add(ambience_review)

                if media_data:
                    for media_item in media_data:
                        media = MediaModel(overall_id=review_id, **media_item)
                        s.add(media)
            s.commit()
            return review
        except Exception as e:
            s.rollback()
            raise e
        finally:
            s.close()

    def delete(self, review: OverallReviewModel) -> None:
        s = get_session()
        s.begin()

        try:
            s.query(FoodModel).filter(FoodModel.overall_id == review.id).delete()
            s.query(ServiceModel).filter(ServiceModel.overall_id == review.id).delete()
            s.query(AmbienceModel).filter(
                AmbienceModel.overall_id == review.id
            ).delete()
            s.query(MediaModel).filter(MediaModel.overall_id == review.id).delete()

            s.delete(review)

            s.commit()
        except Exception as e:
            s.rollback()
            raise e
        finally:
            s.close()
