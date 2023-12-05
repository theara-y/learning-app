from flask import Blueprint, jsonify, request
from app import db
from ..models import Progress, User, Question
from datetime import datetime, timezone
from sqlalchemy import tuple_

bp = Blueprint('progress', __name__, url_prefix='/progress')

@bp.route('', methods=['GET'])
def create_progress():
    if 'user_id' not in request.json:
        return jsonify(
            message = "'user_id' missing in request",
        ), 400
    
    if 'question_ids' not in request.json:
        return jsonify(
            message = "'question_ids' missing in request"
        ), 400
    
    user = User.query.get(request.json['user_id'])

    if not user:
        return jsonify(
            message = 'user not found'
        ), 404
    
    questions = Question.query.filter(
        Question.id.in_(request.json['question_ids'])
    ).all()

    if len(questions) != len(request.json['question_ids']):
        return jsonify(
            message = "Invalid question ids"
        ), 400
    
    progress_list = []
    for question in questions:
        progress_list.append(
            Progress(
                user_id = request.json['user_id'],
                question_id = question.id,
                next_milestone = 1,
                next_milestone_date = datetime.now(timezone.utc),
                mastered = False
        ))
    
    db.session.bulk_save_objects(progress_list)
    db.session.commit()

    result = []
    for progress in progress_list:
        result.append(progress.serialize())

    return jsonify(result)

@bp.route('', methods=['PATCH'])
def update_progress():
    if 'user_id' not in request.json:
        return jsonify(
            message = "'user_id' missing in request",
        ), 400
    
    if 'question_ids' not in request.json:
        return jsonify(
            message = "'question_ids' missing in request"
        ), 400
    
    user = User.query.get(request.json['user_id'])

    if not user:
        return jsonify(
            message = 'user not found'
        ), 404
    
    questions = Question.query.filter(
        Question.id.in_(request.json['question_ids'])
    ).all()

    if len(questions) != len(request.json['question_ids']):
        return jsonify(
            message = "Invalid question ids"
        ), 400

    if 'mastered' not in request.json and \
    ('next_milestone' not in request.json or \
     'next_milestone_date' not in request.json):
        return jsonify(
            message = "'mastered' or 'next_milestone' and 'next_milestone_date' missing in request"
        ), 400
    
    common_values = {}

    if 'mastered' in request.json:
        common_values['mastered'] = request.json['mastered']

    if 'next_milestone' in request.json:
        common_values['next_milestone'] = request.json['next_milestone']
    
    if 'next_milestone_date' in request.json:
        common_values['next_milestone_date'] = request.json['next_milestone_date']
    
    composite_keys = []
    for question in questions:
        composite_keys.append((user.id, question.id))

    progress_list = db.session.query(Progress).filter(tuple_(Progress.user_id, Progress.question_id).in_(composite_keys)).all()

    if len(progress_list) != len(request.json['question_ids']):
        return jsonify(
            message = "Invalid progress not found"
        ), 400
    
    update_query = (
        Progress.__table__
        .update()
        .where(tuple_(Progress.user_id, Progress.question_id).in_(composite_keys))
        .values(common_values)
    )

    db.session.execute(update_query)
    db.session.commit()
    
    result = []
    for progress in progress_list:
        result.append(progress.serialize())

    return jsonify(result)