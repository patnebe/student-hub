from flask import current_app
from src.app.models.base import Base
from src.app import db


class Nanodegree(Base):
    __tablename__ = 'nanodegree'

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.String(2000), nullable=False)
    
    projects = db.relationship('Project', backref="nanodegree", lazy=True)

    questions = db.relationship('Question', backref="nanodegree", lazy=True)


    def __repr__(self):
        return f'<Nanodegree: {self.title} >'


nanodegree_enrollments = db.Table(
    'nanodegree_enrollment',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('nanodegree_id', db.Integer, db.ForeignKey('nanodegree.id'), primary_key=True)
)
