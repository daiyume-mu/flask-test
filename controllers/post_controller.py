from flask import Blueprint, render_template, request, redirect
from services import post_service
from services import tag_service
from services import user_service

post_blueprint = Blueprint('todo', __name__)

@post_blueprint.route('/')
def index():
    user_id = request.cookies.get('user_id')
    user = user_service.get_current_user(user_id)
    print(user)
    if not user:
        return redirect('/login')
    posts = post_service.get_all_posts(user_id)
    tags = tag_service.get_all_tags()
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
    user = user_service.get_current_user(user_id)
    if not user:
        return redirect('/login')
    post = post_service.create_post(title, detail, due, user)
    tag_service.associate_tags(post, tag_id)
    return redirect('/')
    
@post_blueprint.route('/create')
def create():
    tags = tag_service.get_all_tags()
    return render_template('create.html', tags=tags)

@post_blueprint.route('/detail/<int:id>')
def read(id):
    post= post_service.get_post_by_id(id)
    return render_template('detail.html', post=post)

@post_blueprint.route('/delete/<int:id>')
def delete(id):
    post_service.delete_post(id)
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
        post = post_service.update_post(id, title, detail, due)
        tag_service.tag_clear(post)
        tag_service.associate_tags(post, tag_id)
         
        return redirect('/')
    except Exception as e:
        print(e) 
        return "Error: Something went wrong", 500

@post_blueprint.route('/edit/<int:id>')
def edit(id):
    post = post_service.get_post_by_id(id)
    tags = tag_service.get_all_tags()
    return render_template('update.html', post=post, tags=tags)

