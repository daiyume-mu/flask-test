from flask import Blueprint, render_template, request, redirect
from models.user import UserModel
from services.post_service import PostService
from models.tag import TagModel
from services.tag_service import TagService
from services.user_service import UserService
from models.post import PostModel, db


post_blueprint = Blueprint('todo', __name__)

postmodel = PostModel(db.session)
postservice = PostService(postmodel)
tagmodel = TagModel(db.session)
tagservice = TagService(tagmodel)
usermodel = UserModel(db.session)
userservice = UserService(usermodel)

@post_blueprint.route('/')
def index():
    user_id = request.cookies.get('user_id')
    user = userservice.get_current_user(user_id)
    print(user)
    if not user:
        return redirect('/login')
    posts = postservice.get_all_posts(user_id)
    tags = tagservice.get_all_tags()
    return render_template('index.html', posts=posts, tags=tags, user=user)

@post_blueprint.route('/store', methods=['POST'])
def store():
    user_id = request.cookies.get('user_id')
    print(user_id)
    data = request.form
    title = data.get('title')
    detail = data.get('detail')
    due = data.get('due')
    tag_id = request.form.getlist('tag_id')
    user = userservice.get_current_user(user_id)
    if not user:
        return redirect('/login')
    post = postservice.create_post(title, detail, due)
    postservice.associate_user(post, user)
    tagservice.associate_tags(post, tag_id)
    return redirect('/')
    
@post_blueprint.route('/create')
def create():
    tags = tagservice.get_all_tags()
    return render_template('create.html', tags=tags)

@post_blueprint.route('/detail/<int:id>')
def read(id):
    post= postservice.get_post_by_id(id)
    return render_template('detail.html', post=post)

@post_blueprint.route('/delete/<int:id>')
def delete(id):
    postservice.delete_post(id)
    return redirect('/')

@post_blueprint.route('/update/<int:id>', methods=['POST'])
def update(id):
    
    data = request.form
    title = data.get('title')
    detail = data.get('detail')
    due = data.get('due')
    tag_id = request.form.getlist('tag_id')

    print(id, title, detail, due)#早期リターンとは何が存在してれば、処理を走らせるって書くのではなく、何が存在してなかったら処理を終わらせるというコードを先に書くこと。これにより、ちゃんとしてた時に走るコードが長ければ長いほどみやすくなる。
    if not id or not title or not detail or not due: 
        return "Error: Missing required fields", 400
    try:
        post = postservice.update_post(id, title, detail, due)
        tagservice.tag_clear(post)
        tagservice.associate_tags(post, tag_id)
         
        return redirect('/')
    except Exception as e:
        print(e) 
        return "Error: Something went wrong", 500

@post_blueprint.route('/edit/<int:id>')
def edit(id):
    post = postservice.get_post_by_id(id)
    tags = tagservice.get_all_tags()
    return render_template('update.html', post=post, tags=tags)

