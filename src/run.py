import os
from .config import DevelopmentConfig
from .app import create_app, db
from .app.models.user import User
from .app.models.nanodegree import Nanodegree, nanodegree_enrollments
from .app.models.project import Project
from .app.models.question import Question
from .app.models.answer import Answer

app = create_app(DevelopmentConfig)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        "Nanodegree": Nanodegree,
        "Project": Project,
        'Question': Question,
        "Answer": Answer
    }
