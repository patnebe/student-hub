from flask import current_app
from src.app.models.base import Base
from src.app import db
import enum


class Question(Base):
    __tablename__ = 'question'

    title = db.Column(db.String(150), nullable=False)

    details = db.Column(db.String(), nullable=False)

    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    nanodegree_id = db.Column(db.Integer, db.ForeignKey(
        'nanodegree.id'), nullable=False, index=True)

    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id'), nullable=False, index=True)

    github_link = db.Column(db.String(150), nullable=True)

    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    answers = db.relationship("Answer", backref="question", lazy=True)

    has_accepted_answer = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Question: {self.title} >'

    def serialize_preview(self):
        return {
            "title": self.title,
            "id": self.id,
            "nanodegree_id": self.nanodegree_id,
            "project_id": self.project_id,
            "asked_by": self.posted_by
        }

    def serialize_full(self):
        return {
            "title": self.title,
            "id": self.id,
            "nanodegree_id": self.nanodegree_id,
            "project_id": self.project_id,
            "details": self.details,
            "github_link": self.github_link,
            "has_accepted_answer": self.has_accepted_answer,
            "answers": self.answers,
        }

