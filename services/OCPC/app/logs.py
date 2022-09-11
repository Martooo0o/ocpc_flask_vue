import os

from flask import Blueprint, make_response, redirect, url_for, request, jsonify, app
from werkzeug.utils import secure_filename

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Log
from flask_cors import CORS
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity, verify_jwt_in_request
import json
from markupsafe import escape
from flask import current_app
from flask import g
from pm4pymdl.objects.ocel.importer import importer as ocel_importer
from pm4pymdl.objects.ocel.exporter import exporter as ocel_exporter
import pm4py

logs = Blueprint('logs', __name__, url_prefix="/logs")
CORS(logs, supports_credentials=True)
# uploads_dir = ""
# with g.app_context():
# uploads_dir = os.path.join(current_app.instance_path, 'uploads/logs')
# Create a directory in a known location to save files to.
# uploads_dir = os.path.join(logs.instance_path, 'uploads')
# os.makedirs(uploads_dir, exists_ok=True)

# example code
@logs.after_request
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

@logs.route('/all', methods=['POST'])
@jwt_required()
def get_logs():
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        return jsonify({
            'logs': [log.filename for log in usr_obj.logs]
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

def getLogAttrs(log_path, logname, original_df, original_obj_df):

    all_attrs = [x for x in original_obj_df.columns.astype(str)]
    # print(all_attrs)
    all_attrs.remove('object_type')
    all_attrs.remove('object_id')
    print(all_attrs)

    log_ocel = pm4py.read_ocel(log_path)
    obj_types = pm4py.ocel_get_object_types(log_ocel)

    attrs = {}
    # get event attrs
    # for original_df
    attribute_names = pm4py.ocel_get_attribute_names(log_ocel)
    print(attribute_names)
    # get object attrs
    attrs['Events'] = []
    # print("THIIIS")
    # print(attrs_no_obj_at_start)
    for attr in attribute_names:
        if not "object_" + attr in all_attrs:
            attrs['Events'].append(attr)

    print("EVENT ATTRS")
    print(attrs)
    for type in obj_types:
        type_df = original_obj_df.loc[original_obj_df['object_type'] == type]
        type_df = type_df.dropna(axis=1)
        out_type_df = [x for x in type_df.columns.astype(str)]
        print("Obj DF columns")
        print(out_type_df)
        print(type_df.head(10))

        for attr in all_attrs:
            if attr in out_type_df:
                if not type in attrs.keys():
                    attrs[type] = []
                attrs[type].append(attr)

    return attrs

@logs.route('/get/<logname>', methods=['POST'])
@jwt_required()
def get_log(logname):
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        for log in usr_obj.logs:
            if log.filename == escape(logname):
                log_path =  os.path.join(current_app.instance_path, 'logs') + "/" + logname

                original_df, original_obj_df = ocel_importer.apply(
                    log_path)

                attrs = getLogAttrs(log_path, logname, original_df, original_obj_df)

                return jsonify({
                    'log': log.filename,
                    'attrs': attrs,
                    'num_events': len(original_df),
                    'num_objs': len(original_obj_df),
                }), 200

        return jsonify({
            'error': "Log not found"
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

def createLog(user_id, new_file_name):
    new_log = Log(user_id=user_id, filename=new_file_name)
    # add the new user to the database
    db.session.add(new_log)
    db.session.commit()
    return new_log

@logs.route('/add',  methods=['POST'])
@jwt_required()
def add_log():
    file = request.files['file']
    print(request.files)
    # data = request.get_json()
    #
    # dimens = data.get('dimens')

    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        new_file_name = secure_filename(file.filename)
        # with open(os.path.join(UPLOAD_FOLDER, new_file_name), )
        uploads_dir = os.path.join(current_app.instance_path, 'logs')
        file.save(os.path.join(uploads_dir, new_file_name))
        # TODO check if file with this name already exits and adjusts appropriately
        createLog(usr_obj.id, new_file_name)

        response = make_response({"success": "New log was save successfully"})
        response.cache_control.no_cache = True
        return response
    else:
        return jsonify(message="Unauthorized no user found"), 401


@logs.route('/delete/<logname>',  methods=['POST'])
@jwt_required()
def delete_log(logname):
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        for log in usr_obj.logs:
            if log.filename == logname:
                for cube in log.cubes:
                    for analysis in cube.analyses:
                        db.session.delete(analysis)
                    db.session.delete(cube)
                db.session.delete(log)
                db.session.commit()

        response = make_response({"success": "Log and all it's cubes and analyses were deleted successfully"})
        response.cache_control.no_cache = True
        return response
    else:
        return jsonify(message="Unauthorized no user found"), 401