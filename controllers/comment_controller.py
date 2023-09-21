from flask import Blueprint, render_template, request, redirect
from services import comment_service
from datetime import datetime

comment_blueprint = Blueprint('comment', __name__)

@comment_blueprint.route('/create_comment')
def create_comment():
    return render_template('create_comment.html')

@comment_blueprint.route('/add_comment', methods=['POST'])
def add_comments():
    content_timestamp = datetime.now()
    content = request.form.get('comment')
    post_id = request.form.get('post_id')
    comment_service.comment_post(post_id, content, content_timestamp)
    return redirect(f'/detail/{post_id}')