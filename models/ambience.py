from base import db

class Ambience(db.Model):
    __tablename__ = 'ambience'
    id = db.Column(db.Integer, primary_key=True)
    overall_id = db.Column(db.Integer, db.ForeignKey('overall_review.id'), nullable=False)
    ambience_score = db.Column(db.Integer, nullable=True)
    ambience_comment = db.Column(db.String(255), nullable=True)