from flask import current_app
from src.app.models.base import Base
from src.app.models.nanodegree import nanodegree_enrollments
from src.app import db


class User(Base):
    __tablename__ = 'user'

    jwt_subject = db.Column(
        db.String(200), nullable=False, unique=True, index=True)
    # This maps the subject claim of the Auth0 JWT to a unique user in the users table

    nanodegrees = db.relationship('Nanodegree', secondary=nanodegree_enrollments,
                                  lazy='dynamic', backref=db.backref('students', lazy='dynamic'))

    # questions
    questions = db.relationship('Question', backref="user", lazy=True)

    # anwers
    answers = db.relationship('Answer', backref="user", lazy=True)

    def serialize(self):
        return {"id": self.id}

    def __repr__(self):
        return f'<User {self.jwt_subject}>'
