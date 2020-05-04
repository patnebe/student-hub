from flask import current_app
from src.app.models.base import Base
from src.app import db
import enum


class Question(Base):
    __tablename__ = 'question'

    title = db.Column(db.String(150), nullable=False)

    details = db.Column(db.String(), nullable=False)

    # votes = db.relationship("CurrentVoteQuestion", backref="question")

    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    nanodegree_id = db.Column(db.Integer, db.ForeignKey('nanodegree.id'), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    github_link = db.Column(db.String(150), nullable=True)

    # vote_count = db.Column(db.Integer, default=0, nullable=False)

    answers = db.relationship("Answer", backref="question", lazy=True)

    has_accepted_answer = db.Column(db.Boolean, nullable=False, default=False)

    comments = db.relationship("QuestionComment", backref="question", lazy=True)


    def __repr__(self):
        return f'<Question: {self.title} >'



# class CurrentVoteEnum(enum.Enum):
#     up = 'up'
#     down = 'down'



# class CurrentVoteQuestion(Base):
#     __tablename__ = 'current_vote_question'

#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

#     current_vote = db.Column(db.Enum(CurrentVoteEnum), default=None, nullable=True)


#     def __repr__(self):
#         return f'<Vote: User {self.user_id} voted {self.current_vote} on question {self.question_id}>'



class QuestionComment(Base):
    __tablename__ = "question_comment"

    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    details = db.Column(db.String(), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


    def __repr__(self):
        return f'<Comment on question {self.question_id}, posted by user {self.posted_by} >'