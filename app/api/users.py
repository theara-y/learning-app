from flask import Blueprint, jsonify, request
from app import db
from ..models import User

bp = Blueprint('users', __name__, url_prefix='/user')

@bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify(
            message = "user not found"
        ), 404

    return jsonify(user.serialize())

@bp.route('', methods=['POST'])
def create_user():
    if 'name' not in request.json:
        return jsonify(
            message="'name' missing in request"
        ), 400
    
    user = User(name = request.json['name'])

    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    if 'name' not in request.json:
        return jsonify(
            message="'name' missing in request"
        ), 400
    
    user = User.query.get(id)

    if not user:
        return jsonify(
            message = "user not found"
        ), 404
    
    if user.name == request.json['name']:
        return jsonify(
            message = "name not different"
        ), 400

    user.name = request.json['name']

    db.session.commit()

    return jsonify(user.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    
    if not user:
        return jsonify(
            message = "user not found"
        ), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify(
        message = f"user '{user.name}' deleted"
    ), 200