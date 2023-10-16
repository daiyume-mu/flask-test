from flask import Blueprint, render_template, request, redirect, flash
from services import tag_service
from request import add_tag_request
from services import user_service

tag_blueprint = Blueprint('tag', __name__)

@tag_blueprint.route('/add_tag', methods=['POST'])
def add_tag():
    tag = request.form.get('tag')
    print(tag)
    if not add_tag_request.is_unique_tag(tag):
        flash(f"Tag '{tag}' already exists.", 'error')
        return render_template('create_tag.html')
    tag_service.create_tag(tag)
    return redirect('/')

@tag_blueprint.route('/create_tag')
def create_tag():
    return render_template('create_tag.html')

@tag_blueprint.route('/tag_post_list/<int:tag_id>')
def tag_list(tag_id):
    user_id = request.cookies.get('user_id')
    user = user_service.get_current_user(user_id)
    if not user:
        return redirect('/login')
    posts = tag_service.get_posts_by_tag_id(tag_id, user_id)
    print(posts)
    return render_template('tag_post_list.html', posts=posts)