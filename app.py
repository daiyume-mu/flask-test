from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.post import db
from models.tag import db
from models.comment import db
from controllers.post_controller import post_blueprint
from controllers.comment_controller import comment_blueprint
from controllers.tag_controller import tag_blueprint
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

app.register_blueprint(post_blueprint)
app.register_blueprint(comment_blueprint)
app.register_blueprint(tag_blueprint)