# /my_flask_app/app/routes/views.py

from flask import Blueprint, jsonify

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/test')
def test():
    return jsonify({"message": "This is a test endpoint!"})
