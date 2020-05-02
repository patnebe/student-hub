from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, abort, make_response
from flask_login import current_user, login_user, logout_user
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from src.app import db
from src.app.models.user import User
from marshmallow import ValidationError
from src.app.blueprints.auth.utils.input_validators import Login_Input_Validator, Signup_Input_Validator
from src.app.blueprints.auth.utils.jwt_helper_methods import get_token_from_auth_header, AuthError
import sys


auth = HTTPBasicAuth()

########################################
# This part is getting super confusing #
########################################

@auth.verify_password
def verify_password(email, password):
    """
    This authenticates the user by validating the bearer token included in the request header. If this is not present/is invalid then a username:password combination in the Authorization header is used.
    """
    # Get auth token
    try:
        token = get_token_from_auth_header()

    except AuthError as auth_error:
        abort(auth_error.status_code)
        
    user = User.verify_auth_token(token)

    if user is None:
        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.verify_password(password):
            return False
    
    g.user = user
    
    return True


# Authentication blueprint and it's controllers
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Registers a new unique user in the database
    """
    if current_user.is_authenticated:
        return jsonify({
            'message': 'User is already logged in',
            'success': True
        })
        # return redirect(url_for('index'))

    request_payload = request.get_json()

    try:
        signup_input_data_is_valid = Signup_Input_Validator().load(request_payload)
    
    except ValidationError:
        abort(400)

    try:
        response_data = {}        

        email = request_payload['email']
        first_name = request_payload['first_name']
        last_name = request_payload['last_name']
        password = request_payload['password']

        # Check if a user with that email exists, and return an error_message if it does

        existing_user = User.query.filter_by(email=email).first()

        if existing_user is not None:
            response_data['success'] = False
            response_data['message'] = 'A user with that email already exists'
            response_data['status'] = 409
            return make_response(jsonify(response_data), 409)
        
        # register the new user
        new_user = User(first_name=first_name, last_name=last_name, email=email)

        new_user.set_password(password=password)

        new_user.save()

        response_data['success'] = True
        response_data['status'] = 201
        response_data['message'] = f'User with email: {email} was successfully created'
        response_data['data'] = 'user' #change this to a serialized version of the user

        return make_response(jsonify(response_data), 201) # Or redirect users wherever you want them to go
    
    except Exception:
        print(sys.exc_info())
        abort(500)
    
    finally:
        db.session.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({
            'message': 'User is already logged in',
            'success': True
        })
        # return redirect(url_for('index'))

    request_payload = request.get_json()
    
    try:
        login_input_data_is_valid = Login_Input_Validator().load(request_payload)
    
    except ValidationError:
        abort(400)

    try:
        response_data = {}
 
        email = request_payload['email']
        password = request_payload['password']

        user = User.query.filter_by(email=email).first()

        if user is None or not user.verify_password(password):
            response_data['success'] = False
            response_data['status'] = 401
            response_data['message'] = 'Invalid login credentials'

            return make_response(jsonify(response_data), 401)

        login_user(user)

        token = user.generate_auth_token(600)
    
        token = token.decode('ascii')

        # Construct response data  
        response_data['success'] = True
        response_data['status'] = 200
        response_data['message'] = 'Login was successful'
        response_data['token'] = token

        return jsonify(response_data) # or redirect the user to the index page

    except Exception:
        print(sys.exc_info())
        abort(500)
    
    finally:
        db.session.close()


@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()

    # revoke the token?

    return jsonify({
        'success': True,
        'message': 'Logout was successful',
        'status': 200
    })


@auth_bp.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    
    return jsonify({
        'success': True,
        'status': 200,
        'token': token.decode('ascii')
    })

