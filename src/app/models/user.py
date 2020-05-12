from flask import current_app
from src.app.models.base import Base
from src.app.models.nanodegree import nanodegree_enrollments
from src.app.models.question import QuestionComment
from src.app.models.answer import AnswerComment
from src.app import db


class User(Base):
    __tablename__ = 'user'

    jwt_subject = db.Column(
        db.String(200), nullable=False, unique=True, index=True)
    # This maps the subject claim of the Auth0 JWT to a unique user in the users table

    nanodegrees = db.relationship('Nanodegree', secondary=nanodegree_enrollments,
                                  lazy='subquery', backref=db.backref('users', lazy=True))

    # questions
    questions = db.relationship('Question', backref="user", lazy=True)

    question_comments = db.relationship(
        'QuestionComment', backref="user", lazy=True)

    # anwers
    answers = db.relationship('Answer', backref="user", lazy=True)

    answer_comments = db.relationship(
        'AnswerComment', backref="user", lazy=True)

    # question vote M2M

    # answer vote M2M

    # figure out how to get the following fields from the user

    # email = db.Column(db.String(150), nullable=True)

    # firstname = db.Column(db.String(150), nullable=True)

    # lastname = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f'<User {self.jwt_subject}>'
