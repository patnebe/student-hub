from flask import Blueprint, request, g, session, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from src.app.blueprints.api_v1.utils.auth0_helper import requires_auth
from src.app.blueprints.api_v1.utils.input_validators import Nanodegree_Input_Schema
from src.app.models.user import User
from src.app.models.nanodegree import Nanodegree
from src.app.models.project import Project
from src.app.models.question import Question, QuestionComment  # , CurrentVoteQuestion
from src.app.models.answer import Answer, AnswerComment  # , CurrentVoteAnswer
import sys


db = SQLAlchemy()


api_v1_bp = Blueprint('api_v1', __name__)


@api_v1_bp.route('/')
@requires_auth(permission="create:nanodegree")
def api_home():
    return 'Hello API', 200


@api_v1_bp.route('/nanodegrees', methods=['POST'])
@requires_auth(permission="create:nanodegree")
def create_nanodegree(jwt):
    """
    Creates a new Nanodegree program
    """
    request_payload = request.get_json()

    try:
        input_is_valid = Nanodegree_Input_Schema().load(request_payload)

    except ValidationError:
        abort(400)

    try:
        title = request_payload['title']
        description = request_payload['description']

        new_nanodegree = Nanodegree(title=title, description=description)
        new_nanodegree.save()
        print(new_nanodegree)

        response_data = {
            "success": True,
            "data": new_nanodegree.serialize()
        }

        return make_response(jsonify(response_data), 201)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()
