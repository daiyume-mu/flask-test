from flask import Blueprint, render_template, request, redirect
from services.comment_service import CommentService
from datetime import datetime
from models.post import db

comment_blueprint = Blueprint('comment', __name__)
commentservice = CommentService(db.session)

@comment_blueprint.route('/create_comment')
def create_comment():
    return render_template('create_comment.html')

@comment_blueprint.route('/add_comment', methods=['POST'])
def add_comments():
    content_timestamp = datetime.now()
    content = request.form.get('comment')
    post_id = request.form.get('post_id')
    commentservice.comment_post(post_id, content, content_timestamp)
    return redirect(f'/detail/{post_id}')