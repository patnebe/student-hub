from flask import current_app
from src.app.models.base import Base
from src.app import db


class Project(Base):
    __tablename__ = 'project'

    title = db.Column(db.String(150), nullable=False)

    nanodegree_id = db.Column(db.Integer, db.ForeignKey(
        'nanodegree.id'), nullable=False)

    questions = db.relationship('Question', backref='project', lazy=True)

    def serialize(self):
        return {
            "id": int(self.id),
            "title": str(self.title),
            "nanodegree_id": int(self.nanodegree_id)
        }

    def __repr__(self):
        return f'<Project: {self.title} >'
