from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def api_home():
    return jsonify({"message": "Welcome to the Student Hub API"})
