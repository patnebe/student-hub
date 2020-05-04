from flask import current_app
from src.app.models.base import Base
from src.app import db
import enum

class Answer(Base):
    __tablename__ = 'answer'

    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    details = db.Column(db.String(), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    accepted = db.Column(db.Boolean, default=False, nullable=False)

    comments = db.relationship('AnswerComment', backref="answer", lazy=True)

    # votes = db.relationship("CurrentVoteQuestion", backref="question")


    def __repr__(self):
        return f'<Answer to question {self.question_id} posted by {self.posted_by}>'


# class CurrentVoteEnum(enum.Enum):
#     up = 'up'
#     down = 'down'


# class CurrentVoteAnswer(Base):
#     __tablename__ = 'current_vote_answer'

#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)

#     current_vote = db.Column(db.Enum(CurrentVoteEnum), default=None, nullable=True)


#     def __repr__(self):
#         return f'<Vote: User {self.user_id} voted {self.current_vote} on answer {self.answer_id}>'


class AnswerComment(Base):
    __tablename__ = "answer_comment"

    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    details = db.Column(db.String(), nullable=False)

    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)


    def __repr__(self):
        return f'<Comment on answer {self.answer_id}, posted by user {self.posted_by}>'