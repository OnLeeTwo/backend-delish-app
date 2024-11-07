from base import db

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    overall_id = db.Column(db.Integer, db.ForeignKey('overall_review.id'), nullable=False)
    service_score = db.Column(db.Integer, nullable=True)
    service_comment = db.Column(db.String(255), nullable=True)