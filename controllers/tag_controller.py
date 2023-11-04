from flask import Blueprint, jsonify, render_template, request, redirect, flash
from models.tag import TagModel
from models.user import UserModel
from services.post_service import PostService
from services.tag_service import TagService
from services.user_service import UserService
from request import add_tag_request
from models.post import PostModel, db

tag_blueprint = Blueprint('tag', __name__)
postmodel = PostModel(db.session)
postservice = PostService(postmodel)
tagmodel = TagModel(db.session)
tagservice = TagService(tagmodel)
usermodel = UserModel(db.session)
userservice = UserService(usermodel)

@tag_blueprint.route('/add_tag', methods=['POST'])
def add_tag():
    tag = request.form.get('tag')
    if not add_tag_request.is_unique_tag(tag):
        return jsonify({"error": f"Tag '{tag}' already exists."}), 400
    tagservice.create_tag(tag)
    return jsonify({"message": "Tag created successfully"}), 201


"""@tag_blueprint.route('/create_tag')
def create_tag():
    return render_template('create_tag.html')"""


@tag_blueprint.route('/tag_post_list/<int:tag_id>')
def tag_list(tag_id):
    user_id = request.cookies.get('user_id')
    user = userservice.get_current_user(user_id)
    if not user:
        return jsonify({"error": "User not logged in"}), 401
    posts = tagservice.get_posts_by_tag_id(tag_id, user_id)
    posts_data = [postservice.serialize_post(post) for post in posts]
    return jsonify({"posts": posts_data})