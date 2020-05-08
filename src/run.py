import os
from src.config import DevelopmentConfig
from .app import create_app, db
from .app.models.user import User
from .app.models.nanodegree import Nanodegree, nanodegree_enrollments
from .app.models.project import Project
from .app.models.question import Question, QuestionComment  # , CurrentVoteQuestion
from .app.models.answer import Answer, AnswerComment  # , CurrentVoteAnswer


app = create_app(DevelopmentConfig)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        "Nanodegree": Nanodegree,
        "Project": Project,
        'Question': Question,
        # "Question_Vote": CurrentVoteQuestion,
        "Question_Comment": QuestionComment,
        "Answer": Answer,
        # "Answer_Vote": CurrentVoteAnswer,
        "Answer_Comment": AnswerComment
    }
