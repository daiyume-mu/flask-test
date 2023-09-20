from flask import Blueprint, render_template, request, redirect
from services import todo_service
from datetime import datetime

todo_blueprint = Blueprint('todo', __name__)

@todo_blueprint.route('/')
def index():
    posts = todo_service.get_all_posts()
    return render_template('index.html', posts=posts)

@todo_blueprint.route('/store', methods=['POST'])
def store():
    title = request.form.get('title')
    detail = request.form.get('detail')
    due = request.form.get('due')
    todo_service.create_post(title, detail, due)
    return redirect('/')
    
@todo_blueprint.route('/create')
def create():
    return render_template('create.html')

@todo_blueprint.route('/detail/<int:id>')
def read(id):
    post= todo_service.get_post_by_id(id)
    comments = post.comments
    return render_template('detail.html', post=post, comments=comments)

@todo_blueprint.route('/delete/<int:id>')
def delete(id):
    todo_service.delete_post(id)
    return redirect('/')

@todo_blueprint.route('/update/<int:id>', methods=['POST'])
def update(id):
    
    data = request.form
    title = data.get('title')
    detail = data.get('detail')
    due = data.get('due')

    print(id, title, detail, due)#早期リターンとは何が存在してれば、処理を走らせるって書くのではなく、何が存在してなかったら処理を終わらせるというコードを先に書くこと。これにより、ちゃんとしてた時に走るコードが長ければ長いほどみやすくなる。
    if not id or not title or not detail or not due:  # Make sure all variables have values
        return "Error: Missing required fields", 400
    try:
        #print(id, title, detail, due)
        todo_service.update_post(id, title, detail, due)  # Pass all required arguments here
        return redirect('/')
    except Exception as e:
        print(e) 
        return "Error: Something went wrong", 500

@todo_blueprint.route('/edit/<int:id>')
def edit(id):
    post = todo_service.get_post_by_id(id)
    return render_template('update.html', post=post)

@todo_blueprint.route('/create_comment')
def create_comment():
    return render_template('create_comment.html')

@todo_blueprint.route('/add_comment', methods=['POST'])
def add_comments():
    comment_timestamp = datetime.now()
    comment = request.form.get('comment')
    post_id = request.form.get('post_id')
    todo_service.comment_post(post_id, comment, comment_timestamp)
    return redirect(f'/detail/{post_id}')