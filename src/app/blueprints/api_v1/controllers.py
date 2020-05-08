from flask import Blueprint, request, g, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
# from flask_login import login_required
from src.app.models.user import User
from src.app.models.nanodegree import Nanodegree
from src.app.models.project import Project
from src.app.models.question import Question, QuestionComment  # , CurrentVoteQuestion
from src.app.models.answer import Answer, AnswerComment  # , CurrentVoteAnswer
import sys

# from src.app.blueprints.api_v1.utils.auth0_helper import AuthError, requires_auth

db = SQLAlchemy()


api_v1_bp = Blueprint('api_v1', __name__)


@api_v1_bp.route('/')
def api_home():
    return 'Hello API', 200


@api_v1_bp.route('/questions')
def get_questions():
    try:
        payload = request.get_json()

        questions = Question.query.all()

    except:
        print(sys.exc_info())

    finally:
        db.session.close()

    response_data = {
        "success": True,
        "data": "data"
    }

    return jsonify(response_data)
