from base import db

class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    overall_id = db.Column(db.Integer, db.ForeignKey('overall_review.id'), nullable=False)
    food_score = db.Column(db.Integer, nullable=True)
    food_comment = db.Column(db.String(255), nullable=True)