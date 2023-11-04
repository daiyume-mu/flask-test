from flask import Blueprint, jsonify, render_template, request, redirect, flash, make_response
from models.user import UserModel
from services.user_service import UserService
from request import add_user_request
from models.post import db

user_blueprint = Blueprint('user', __name__)
usermodel = UserModel(db.session)
userservice = UserService(usermodel)

"""@user_blueprint.route('/login')
def login():
    return render_template('login.html')"""


@user_blueprint.route('/login_check', methods=['POST'])
def login_check():
    email = request.form['email']
    password = request.form['password']
    user = userservice.get_user(email)
    if user and userservice.verify_password(user.password, password):
            response = jsonify({"message": "Logged in successfully"})
            response.set_cookie('user_id', str(user.id), max_age=1200)
            return response, 200
    return jsonify({"message": "Invalid credentials"}), 401


"""@user_blueprint.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')"""


@user_blueprint.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    if not add_user_request.is_unique_user(email):
        return jsonify({"message": f"Email '{email}' already exists."}), 400
    
    userservice.register_user(email, password)
    return jsonify({"message": "User registered successfully"}), 201


@user_blueprint.route('/logout')
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.set_cookie('user_id', '', expires=0)
    return response, 200