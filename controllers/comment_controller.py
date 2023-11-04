from flask import Blueprint, jsonify, render_template, request, redirect
from models.comment import CommentModel
from services.comment_service import CommentService
from datetime import datetime
from models.post import db

comment_blueprint = Blueprint('comment', __name__)
commentmodel = CommentModel(db.session)
commentservice = CommentService(commentmodel)

"""@comment_blueprint.route('/create_comment')
def create_comment():
    return render_template('create_comment.html')"""

@comment_blueprint.route('/add_comment', methods=['POST'])
def add_comments():
    content_timestamp = datetime.now()
    content = request.form.get('comment')
    post_id = request.form.get('post_id')
    commentservice.comment_post(post_id, content, content_timestamp)
    return jsonify({"message": "Comment added successfully"}), 201