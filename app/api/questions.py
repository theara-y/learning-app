from flask import Blueprint, jsonify, request
from app import db
from ..models import Question, Group

bp = Blueprint('questions', __name__, url_prefix='/question')

@bp.route('', methods=['GET'])
def get_questions():
    questions = Question.query.all()

    result = []
    for question in questions:
        result.append(question.serialize())

    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    question = Question.query.get(id)

    if not question:
        return jsonify(
            message = "question not found"
        ), 404

    return jsonify(question.serialize())

@bp.route('', methods=['POST'])
def create_question():
    if 'group_id' not in request.json:
        return jsonify(
            message="'group_id' missing in request"
        ), 400
    
    group = Group.query.get(request.json['group_id'])

    if not group:
        return jsonify(
            message = "group not found"
        ), 404
    
    if 'questions_data' not in request.json:
        return jsonify(
            message="'questions_data' missing in request"
        ), 400
    
    questions_to_insert = []
    for question in request.json['questions_data']:
        questions_to_insert.append(
            Question(
                info = question,
                group_id = request.json['group_id']
            )
        )

    db.session.bulk_save_objects(questions_to_insert)
    db.session.commit()

    return jsonify(request.json['questions_data'])


@bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    if 'question_data' not in request.json:
        return jsonify(
            message="'question_data' missing in request"
        ), 400
    
    question = Question.query.get(id)

    if not question:
        return jsonify(
            message = "question not found"
        ), 404
    
    question.info = request.json['question_data']

    db.session.commit()

    return jsonify(question.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_questions(id):
    question = Question.query.get(id)
    
    if not question:
        return jsonify(
            message = "question not found"
        ), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify(
        message = f"question '{question.info['question']}' deleted"
    ), 200