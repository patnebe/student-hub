from flask import Blueprint, request, g, session, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from src.app.blueprints.api_v1.utils.auth0_helper import requires_auth
from src.app.blueprints.api_v1.utils.input_validators import Nanodegree_Input_Schema, Project_Input_Schema
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


@api_v1_bp.route('/nanodegrees', methods=['GET'])
def get_nanodegrees():
    """Returns a list of all available nanodegrees"""
    try:
        list_of_nanodegrees = Nanodegree.query.all()

        list_of_nanodegrees = [nanodegree.serialize()
                               for nanodegree in list_of_nanodegrees]

        response_object = {
            "success": True,
            "data": list_of_nanodegrees
        }

        return jsonify(response_object)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()


@api_v1_bp.route('/nanodegrees/<int:nanodegree_id>/projects', methods=['POST'])
@requires_auth(permission="create:project")
def create_nanodegree_projects(jwt, nanodegree_id):
    """Creates new projects for a nanodegree"""

    request_payload = request.get_json()

    list_of_projects = request_payload['projects']

    try:
        for project in list_of_projects:
            project_is_valid = Project_Input_Schema().load(project)

    except ValidationError:
        abort(400)

    try:
        nanodegree = Nanodegree.query.get(nanodegree_id)

        for project in list_of_projects:
            new_project = Project(title=project['title'])
            nanodegree.projects.append(new_project)

        nanodegree.save()

        number_of_projects = len(list_of_projects)

        response_object = {
            "success": True,
            "message": f"{number_of_projects} new projects have been created for this nanodegree"
        }

        return make_response(jsonify(response_object), 201)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()


@api_v1_bp.route('/nanodegrees/<int:nanodegree_id>/projects', methods=['GET'])
def get_nanodegree_projects(nanodegree_id):
    """Returns all the projects for a given nanodegree"""

    nanodegree = Nanodegree.query.get(nanodegree_id)

    if nanodegree is None:
        abort(404)

    try:
        list_of_projects = [project.serialize()
                            for project in nanodegree.projects]

        response_data = {
            "success": True,
            "data": list_of_projects
        }

        return jsonify(response_data)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()
