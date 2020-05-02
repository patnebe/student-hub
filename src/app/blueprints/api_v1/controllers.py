from flask import Blueprint, request, g, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required

# from src.app.blueprints.api_v1.utils.auth0_helper import AuthError, requires_auth

db = SQLAlchemy()


api_v1_bp = Blueprint('api_v1', __name__)


@api_v1_bp.route('/')
@login_required
def api_home():
    return 'Hello API', 200
