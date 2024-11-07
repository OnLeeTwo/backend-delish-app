from base import db
from datetime import datetime, timezone


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    overall_id = db.Column(db.Integer, db.ForeignKey('overall_review.id'), nullable=False)
    location = db.Column(db.Text, nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))