from flask import Blueprint, current_app, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from src.app.blueprints.api_v1.utils.auth0_helper import requires_auth, get_jwt_subject
from src.app.blueprints.api_v1.utils.input_validators import Nanodegree_Input_Schema, Project_Input_Schema, Question_Input_Schema
from src.app.models.user import User
from src.app.models.nanodegree import Nanodegree
from src.app.models.project import Project
from src.app.models.question import Question
from src.app.models.answer import Answer
import sys

db = SQLAlchemy()


api_v1_bp = Blueprint('api_v1', __name__)


@api_v1_bp.route('/')
def api_home():
    return jsonify({"message": "Welcome to the Student Hub API"})


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

        if len(list_of_projects) == 0:
            return make_response(jsonify({
                "success": False,
                "error": 404,
                "message": "There is currently no project for this nanodegree. Please check back later."
            }), 404)

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


@api_v1_bp.route('/nanodegrees/<int:nanodegree_id>/students', methods=['GET'])
@requires_auth(permission="get:nanodegree-students")
def get_nanodegree_students(jwt, nanodegree_id):
    """
    Returns a paginated list of students enrolled in a given nanodegree
    """

    nanodegree = Nanodegree.query.get(nanodegree_id)

    if nanodegree is None:
        abort(404)

    request_body = request.get_json(
    ) or {'page': 1, 'students_per_page': int(current_app.config[
        'STUDENTS_PER_PAGE'])}

    page = request_body['page'] or 1

    if page <= 0:
        abort(400)

    students_per_page = request_body['students_per_page'] or int(current_app.config[
        'STUDENTS_PER_PAGE'])

    if students_per_page <= 0:
        abort(400)

    total_number_of_students = nanodegree.students.count()

    if total_number_of_students < 1:
        abort(404)

    try:
        start = ((page - 1) * students_per_page) + 1

        # list_of_students is a pagination object
        students = nanodegree.students.paginate(
            start, students_per_page, False)

        has_next_page = students.has_next

        has_prev_page = students.has_prev

        next_page = None

        previous_page = None

        if has_next_page:
            next_page = page + 1

        if has_prev_page:
            previous_page = page - 1

        list_of_students = [student.serialize() for student in students.items]

        response_data = {
            "success": True,
            "data": {
                "nanodegree": nanodegree.title,
                "students": list_of_students,
                "total_number_of_students": total_number_of_students,
                "has_next_page": has_next_page,
                "next_page": next_page,
                "has_previous_page": has_prev_page,
                "previous_page": previous_page
            }
        }

        return jsonify(response_data)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()


@api_v1_bp.route('/nanodegrees/<int:nanodegree_id>/enroll', methods=['GET'])
def enroll_in_nanodegree(nanodegree_id):
    """Enrolls a user in a given nanodgree"""

    jwt_subject = get_jwt_subject()

    nanodegree = Nanodegree.query.get(nanodegree_id)

    # check if the student is already enrolled and raise an error if so
    already_enrolled_student = nanodegree.students.filter_by(
        jwt_subject=jwt_subject).first()

    if already_enrolled_student is not None:
        return make_response(jsonify({"error": 409,
                                      "message": "The request failed because the student is already enrolled in this nanodegree.",
                                      "success": False}), 409)

    try:
        # check if the student is in the db
        student = User.query.filter_by(jwt_subject=jwt_subject).first()

        # if not present create the student in the db
        if student is None:
            # create student
            student = User(jwt_subject=jwt_subject)

        # then proceed as usual and register the student for that nanodegree
        nanodegree.students.append(student)
        nanodegree.save()

        # return success message
        response_object = {
            "success": True,
            "message": "Enrollment was successful."
        }

        return jsonify(response_object)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()


@api_v1_bp.route('/questions', methods=['POST'])
@requires_auth(permission="create:question")
def create_new_question(jwt):
    """
    Creates a new question on the platform
    """

    question = request.get_json()

    try:
        question_payload_is_valid = Question_Input_Schema().load(question)

    except ValidationError as error:
        print("Validation error", error.messages)
        abort(400)

    nanodegree_id = question['nanodegree_id']
    project_id = question['project_id']
    title = question['title']
    details = question['details']
    github_link = question['github_link']

    # get nanodegree
    nanodegree = Nanodegree.query.get(nanodegree_id)

    if nanodegree is None:
        print("Nanodegree not found")
        abort(404)

    # get project
    project = Project.query.get(project_id)

    if project is None:
        print("Project not found")
        abort(404)

    try:
        # Find out who is making this request
        jwt_subject = get_jwt_subject()

        # check if the student is enrolled in that nanodegree and return an error if not
        already_enrolled_student = nanodegree.students.filter_by(
            jwt_subject=jwt_subject).first()

        if already_enrolled_student is None:
            return make_response(jsonify({
                "success": False,
                "message": "The student is not enrolled in the Nanodegree so they are not allowed to post a question"
            }), 403)

        # get the student
        student = User.query.filter_by(jwt_subject=jwt_subject).first()

        # create question
        question = Question(title=title,
                            details=details, github_link=github_link, posted_by=student.id, project_id=project.id, nanodegree_id=nanodegree.id)

        # assign question to user
        # student.questions.append(question)

        # # assign question to project
        # project.questions.append(question)

        # # assign question to nanodegree
        # nanodegree.questions.append(question)

        question.save()

        # get back the question data
        response_data = {
            "success": True,
            "data": question.serialize_preview()
        }

        return make_response(jsonify(response_data), 201)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()


@api_v1_bp.route('/questions', methods=['GET'])
def get_questions():
    """
    Returns a paginated list of questions on the platform
    """

    request_body = request.get_json(
    ) or {'page': 1, 'questions_per_page': int(current_app.config['QUESTIONS_PER_PAGE'])}

    page = request_body['page'] or 1

    if page <= 0:
        abort(400)

    questions_per_page = request_body['questions_per_page'] or int(current_app.config['QUESTIONS_PER_PAGE'])

    if questions_per_page <= 0:
        abort(400)

    start = ((page - 1) * questions_per_page) + 1

    questions = Question.query

    total_number_of_questions = questions.count()

    questions_pagination_object = questions.paginate(
        start, questions_per_page, False)

    if total_number_of_questions < 1:
        abort(404)

    try:
        has_next_page = questions_pagination_object.has_next

        has_prev_page = questions_pagination_object.has_prev

        next_page = None

        previous_page = None

        if has_next_page:
            next_page = page + 1

        if has_prev_page:
            previous_page = page - 1

        list_of_questions = [question.serialize_preview()
                             for question in questions_pagination_object.items]

        response_data = {
            "success": True,
            "data": {
                "questions": list_of_questions,
                "total_number_of_questions": total_number_of_questions,
                "has_next_page": has_next_page,
                "next_page": next_page,
                "has_previous_page": has_prev_page,
                "previous_page": previous_page
            }
        }

        return jsonify(response_data)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()


@api_v1_bp.route('/questions/<int:question_id>', methods=['PATCH'])
@requires_auth(permission="update:question")
def update_question(jwt, question_id):
    "Updates the details of a given question the person making the request is the same as the original poster and returns the updated question"

    who_made_the_request = get_jwt_subject()

    question_to_be_edited = Question.query.get(question_id)

    if question_to_be_edited is None:
        abort(404)

    original_poster = User.query.get(question_to_be_edited.posted_by)

    if original_poster.jwt_subject != who_made_the_request:
        abort(403)

    request_payload = request.get_json()

    title = request_payload.get('title', question_to_be_edited.title)
    details = request_payload.get('details', question_to_be_edited.details)
    github_link = request_payload.get(
        'github_link', question_to_be_edited.github_link)

    # validate input
    if type(title) != str:
        return make_response(jsonify({"message": "bad title"}), 400)

    if type(details) != str:
        return make_response(jsonify({"message": "bad details"}), 400)
        # abort(400)

    if type(github_link) not in [str, None]:
        return make_response(jsonify({"message": "bad link"}), 400)
        # abort(400)

    try:
        question_to_be_edited.title = title

        question_to_be_edited.details = details

        question_to_be_edited.github_link = github_link

        question_to_be_edited.update()

        question = question_to_be_edited

        response_data = {"success": True,
                         "message": "Question successfully updated",
                         "data": question.serialize_preview()}

        return jsonify(response_data)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()


@api_v1_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@requires_auth(permission="delete:question")
def delete_question(jwt, question_id):
    "Marks a given question as deleted if the person making the request is the same as the original poster"

    who_made_the_request = get_jwt_subject()

    question_to_be_deleted = Question.query.get(question_id)

    if question_to_be_deleted is None:
        abort(404)

    original_poster = User.query.get(question_to_be_deleted.posted_by)

    if original_poster.jwt_subject != who_made_the_request:
        abort(403)

    try:
        question_to_be_edited.is_deleted = True

        response_data = {"success": True,
                         "message": "Question successfully deleted"}

        return jsonify(response_data)

    except:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()
