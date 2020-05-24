from flask import current_app
from src.app.models.base import Base
from src.app import db
import enum


class Answer(Base):
    __tablename__ = 'answer'

    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    details = db.Column(db.String(), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)

    accepted = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Answer to question {self.question_id} posted by {self.posted_by}>'

    def serialize(self):
        return {
            "id": self.id,
            "posted_by": self.posted_by,
            "details": self.details,
            "accepted": self.accepted,
            "timestamp": self.date_created
        }
