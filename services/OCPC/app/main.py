from flask import Blueprint, jsonify, make_response, redirect, url_for, request
from . import db
from .models import User, Log
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity, verify_jwt_in_request

from .auth import check_usr_credetntials

main = Blueprint('main', __name__, url_prefix="/main")
CORS(main, supports_credentials=True)

# @main.route('/')
# def index():
#     return 'Index'

@main.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@main.route('/profile')
def profile():
    return 'Profile'

# @main.route('/upload_log',  methods=['POST'])
# @jwt_required()
# def add_log():
#     file = request.files['log']
#     data = request.get_json()
#
#     email = data.get('email')
#     password = data.get('password')
#     print(email)
#     print(password)
#
#     if not check_usr_credetntials(email, password):
#         return make_response({'error': 'User is not authenticated'}, 300)
#
#     new_file_name = secure_filename(file)
#     file.save(os.path.join(main.config.UPLOAD_FOLDER, new_file_name))
#     # TODO check if file with this name already exits and adjusts appropriately
#
#     usr = User.query.filter_by(email=email).first()
#
#     new_log = Log(user_id=usr.id, filename=new_file_name)
#     # add the new user to the database
#     db.session.add(new_log)
#     db.session.commit()
#
#     response = make_response({"success": "New log was save successfully"})
#     response.cache_control.no_cache = True
#     return response