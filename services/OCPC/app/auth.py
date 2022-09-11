from flask import Blueprint, make_response, redirect, url_for, request, jsonify
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Log
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity, verify_jwt_in_request
import json

auth = Blueprint('auth', __name__, url_prefix="/auth")
CORS(auth, resources={r"*": {"origins": "*"}})

# example code
# @auth.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r

@auth.route('/login', methods=['POST'])
def login():
    #
    # if request.method == "GET":
    #     # check if user is loged in
    #
    #     return redirect('http://127.0.0.1:5000/logs')

    # data = request.get_json()
    data = json.loads(request.get_data())
    print(data)
    email = data.get('email')
    password = data.get('password')
    # remember = True if data.get('remember', False) else False
    user = User.authenticate(email, password)
    print(user)
    if user:
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)
        print("Acccess Token")
        print(access_token)

        print("Refresh Token")
        print(refresh_token)

        # resp = jsonify({'login': True})
        # set_access_cookies(resp, access_token)
        # set_refresh_cookies(resp, refresh_token)
        # resp.set_cookie('value1', ".frontend.local", domain="localhost")
        # resp.set_cookie('value2', "frontend.local", domain="frontend.local")
        # print(resp.headers)
        # print(resp.data)
        # print(resp.response)

        return jsonify(access_token=access_token,
                       refresh_token=refresh_token)
        # return  resp, 200
    else:
        return jsonify(message="Unauthorized"), 401

    # user = User.query.filter_by(email=email).first()
    #
    # # check if the user actually exists
    # # take the user-supplied password, hash it, and compare it to the hashed password in the database
    # if not user or not check_password_hash(user.password, password):
    #     # flash('Please check your login details and try again.')
    #     print("No user found>")
    #     response = make_response({"error": "User does not exists or password was wrong!"})  # if the user doesn't exist or password is wrong, reload the page
    #     # response.cache_control.no_cache = True
    #     return response
    #
    # # if the above check passes, then we know the user has the right credentials
    # # login_user(user, remember=True)
    # print("User Found" + str(user))
    #
    # response = make_response({"success": "User was loged in"})
    # response.cache_control.no_cache = True
    # return response

@auth.route('/refresh', methods=('POST',))
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first()
    access_token = create_access_token(identity=user.user_id)

    # response = jsonify()
    # set_access_cookies(response, access_token)

    # return response, 201
    return jsonify(access_token=access_token)

@auth.route('/refresh', methods=['OPTION'])
def refresh_opt():
    # Setup things like the `allow` header here.
    return '', 204

@auth.route('/check_jwt', methods=('POST',))
@jwt_required()
def check():
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        return jsonify({
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@auth.route('/user', methods=('POST',))
@jwt_required(locations=["headers"])
def user():

    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        return jsonify({
            'email': usr_obj.email,
            'logs': usr_obj.logs
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@auth.route('/signup', methods=['POST'])
def signup():
    # code to validate and add user to database goes here
    data = request.get_json()
    email = data.get('email')
    # name = request.form.get('name')
    password = data.get('password')

    print(email)

    if not email or not password:
        return make_response({"error": "Email or password is missing!"}, 401)


    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        return make_response({"error": "A user with this e_mail already exists!"}, 401)

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    response = make_response({"success": "New user was register"})
    response.cache_control.no_cache = True
    return response

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return 'Logout'

def check_usr_credetntials(email, password):
    usr = User.query.filter_by(email=email).first()
    if not usr or not check_password_hash(usr.password, password):
        return False
    else:
        return True