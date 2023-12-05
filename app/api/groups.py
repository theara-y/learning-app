from flask import Blueprint, jsonify, request
from app import db
from ..models import Group

bp = Blueprint('groups', __name__, url_prefix='/group')

@bp.route('', methods=['GET'])
def get_groups():
    groups = Group.query.all()

    result = []
    for group in groups:
        result.append(group.serialize())

    return jsonify(result)

@bp.route('', methods=['POST'])
def create_group():
    if 'name' not in request.json:
        return jsonify(
            message="'name' missing in request"
        ), 400
    
    if Group.query.filter_by(name = request.json['name']).one_or_none():
        return jsonify(
            message=f"group '{request.json['name']}' already exists"
        ), 400
    
    group = Group(name = request.json['name'])

    db.session.add(group)
    db.session.commit()

    return jsonify(group.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update_group(id):
    if 'name' not in request.json:
        return jsonify(
            message="'name' missing in request"
        ), 400
    
    group = Group.query.get(id)

    if not group:
        return jsonify(
            message = "group not found"
        ), 404
    
    if group.name == request.json['name']:
        return jsonify(
            message = "name not different"
        ), 400
    
    if Group.query.filter_by(name = request.json['name']).one_or_none():
        return jsonify(
            message=f"group '{request.json['name']}' already exists"
        ), 400

    group.name = request.json['name']

    db.session.commit()

    return jsonify(group.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_questions(id):
    group = Group.query.get(id)
    
    if not group:
        return jsonify(
            message = "group not found"
        ), 404

    db.session.delete(group)
    db.session.commit()

    return jsonify(
        message = f"group '{group.name}' deleted"
    ), 200