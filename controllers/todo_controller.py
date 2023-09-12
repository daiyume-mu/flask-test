from flask import Blueprint, render_template, request, redirect
from services import todo_service

todo_blueprint = Blueprint('todo', __name__)

@todo_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = todo_service.get_all_posts()
        return render_template('index.html', posts=posts)
    else:
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
    post = todo_service.get_post_by_id(id)
    return render_template('detail.html', post=post)

@todo_blueprint.route('/delete/<int:id>')
def delete(id):
    todo_service.delete_post(id)
    return redirect('/')

@todo_blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        post = todo_service.get_post_by_id(id)
        return render_template('update.html', post=post)
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        if title and detail and due:  # Make sure all variables have values
            todo_service.update_post(id, title, detail, due)  # Pass all required arguments here
            return redirect('/')
        else:
            return "Error: Missing required fields", 400

