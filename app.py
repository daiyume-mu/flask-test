from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.post import db
from models.tag import db
from models.comment import db
from controllers.todo_controller import todo_blueprint
from controllers.comment_controller import comment_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

app.register_blueprint(todo_blueprint)
app.register_blueprint(comment_blueprint)