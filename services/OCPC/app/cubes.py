import pandas as pd
from flask import Blueprint, make_response, redirect, url_for, request, jsonify
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

from .logs import createLog, getLogAttrs
from .models import User, Cube
from flask_cors import CORS
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity, verify_jwt_in_request
import json
from markupsafe import escape
import pm4py
import os
from flask import current_app

from pm4pymdl.objects.ocel.importer import importer as ocel_importer
from pm4pymdl.objects.ocel.exporter import exporter as ocel_exporter

from .helper.cubeUtils import calcFreqCube
import time

cubes = Blueprint('cubes', __name__, url_prefix="/cubes")
CORS(cubes, supports_credentials=True)

# example code
@cubes.after_request
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

def createCube(name, log, dimens, event_df, obj_df):

    # logFile = pm4py.read_ocel(os.path.join(current_app.instance_path, 'logs') + "/" + logname)  # ORIGINAL LOG
    counts = calcFreqCube(event_df, obj_df, dimens)
    freqAll = json.dumps(counts['All'])
    freqExistence = json.dumps(counts['Existence'])
    # print(freqAll)
    # try:
    new_cube = Cube(name=name, log_id=log.id, dimens=json.dumps(dimens), freq_all=freqAll, freq_existence=freqExistence)
    # add the new user to the database
    db.session.add(new_cube)
    db.session.commit()
    # except Exception as e:
    #     print(str(e))
    #     raise RuntimeError("Eroor while creating or saving cube!")

@cubes.route('/add', methods=['POST'])
@jwt_required()
def add_cube():
    print(request)
    print(request.get_data())
    print(request.get_json())
    # print(request.args)
    # print(request.json)
    # print(request.data)
    data = json.loads(request.get_data())
    print(data)
    logname = data.get('logname')
    dimens = data.get('dimens')
    # name = data.get('name')
    name = data.get('name')
    print(logname)
    print(dimens)
    print(name)

    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        # new_file_name = secure_filename(file)
        # file.save(os.path.join(logs.config.UPLOAD_FOLDER, new_file_name))
        # TODO check if file with this name already exits and adjusts appropriately
        for log in usr_obj.logs:
            if log.filename == logname:
                # logFile = None # get this
                event_df, obj_df = ocel_importer.apply(os.path.join(current_app.instance_path, 'logs') + "/" + logname)
                # # logFile = pm4py.read_ocel(os.path.join(current_app.instance_path, 'logs') + "/" + logname)  # ORIGINAL LOG
                # counts  = calcFreqCube(event_df, obj_df, dimens)
                # freqAll = json.dumps(counts['All'])
                # freqExistence = json.dumps(counts['Existence'])
                # print(freqAll)
                # try:
                    # new_cube = Cube(name=name, log_id=log.id, dimens=json.dumps(dimens), freq_all=freqAll, freq_existence=freqExistence)
                    # # add the new user to the database
                    # db.session.add(new_cube)
                    # db.session.commit()

                createCube(name, log, dimens, event_df, obj_df)
                # except:
                    # return jsonify(message="Error while creating or storing Cube in DB"), 500

                response = make_response({"success": "New cube was saved successfully"})
                response.cache_control.no_cache = True
                return response
    else:
        return jsonify(message="Unauthorized no user found"), 401

@cubes.route('/all', methods=['POST'])
@jwt_required()
def get_cubes():
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        list_cubes = []
        for log in usr_obj.logs:
            for cube in log.cubes:
                list_cubes.append(cube.name)
        print(list_cubes)
        return jsonify({
            'cubes': list_cubes
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@cubes.route('/all_analyses', methods=['POST'])
@jwt_required()
def get_cubes_analyses():
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        cubes_analyses = {}
        for log in usr_obj.logs:
            for cube in log.cubes:
                cubes_analyses[cube.name] = []
                for analysis in cube.analyses:
                    cubes_analyses[cube.name].append(analysis.name)
                # list_cubes.append(cube.name)
        print(cubes_analyses)
        return jsonify({
            'cubes_analyses': cubes_analyses
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@cubes.route('/get/<cubename>', methods=['POST'])
@jwt_required()
def get_cube(cubename):
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:

                if cube.name == escape(cubename):
                    return jsonify({
                        'cube': cube.name,
                        'dimens': json.loads(cube.dimens),
                        'sourcelog': log.filename,
                        'analyses': json.dumps([analysis.name for analysis in cube.analyses]),
                        'freq_all': cube.freq_all,
                        'freq_existence': cube.freq_existence
                    }), 200

        return jsonify({
            'error': "Cube not found"
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@cubes.route('/get/<cubename>/dim', methods=['POST'])
@jwt_required()
def get_cube_dim(cubename):
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    data = json.loads(request.get_data())
    print(data)
    # cube = data.get('cube')
    dim1 = data.get('dim1')
    dim2 = data.get('dim2')
    mat = data.get('mat')
    print('Mat from data: ' + mat)

    # there is a selected Materialisaion and and at least one dimension
    if mat is None or dim1 is None or dim2 is None:
        return jsonify(message="Missing a parameter. Please provide a non empty mat, dim1, dim2"), 401

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                if cube.name == escape(cubename):
                    if mat == "Existence":
                        print("Mat is existence")
                        result = json.dumps(json.loads(cube.freq_existence)[dim1+','+dim2])
                        print(result)
                        return jsonify(result), 200
                    else:
                        print("Mat is all")
                        result = json.dumps(json.loads(cube.freq_all)[dim1 + ',' + dim2])
                        print(result)
                        return jsonify(result), 200

        return jsonify({
            'error': "Cube not found"
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@cubes.route('/delete/<cubename>', methods=['POST'])
@jwt_required()
def delete_cube(cubename):
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                if cube.name == cubename:
                    for analysis in cube.analyses:
                        db.session.delete(analysis)
                    db.session.delete(cube)
                    db.session.commit()

                    response = make_response({"success": "Cube and all it's analyses were deleted successfully"})
                    response.cache_control.no_cache = True
                    return response
    else:
        return jsonify(message="Unauthorized no user found"), 401

@cubes.route('/performance', methods=['POST'])
@jwt_required()
def testCubePerformance():
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:

        performance = {}
        #generate logs with different number of events
        for i in range(10):
            print("Looping" + str(i))
            num_events = 10 + i*10
            logname = 'example_eventlog.jsonocel'
            log_path = os.path.join(current_app.instance_path, 'logs') + "/performance/" + logname

            filtered_log_path = os.path.join(current_app.instance_path, 'logs') + "/performance/" + str(i) + "events.jsonocel"
            original_df, original_obj_df = ocel_importer.apply(
                log_path)

            new_df = original_df.sample(n = num_events)
            # print(new_df)

            # print(original_obj_df)

            new_obj_df = pd.DataFrame()
            for x in new_df.index:
                for x1 in new_df.loc[x]['customers']:
                    print(new_df.loc[x]['customers'])
                    print(x1)
                    print(original_obj_df.loc[original_obj_df['object_id'] == x1])
                    new_obj_df = new_obj_df.append(original_obj_df.loc[original_obj_df['object_id'] == x1])
                for x1 in new_df.loc[x]['items']:
                    print(new_df['items'])
                    print(x1)
                    print(original_obj_df.loc[original_obj_df['object_id'] == x1])
                    new_obj_df = new_obj_df.append(original_obj_df.loc[original_obj_df['object_id'] == x1])
                for x1 in new_df.loc[x]['orders']:
                    print(new_df['orders'])
                    print(x1)
                    print(original_obj_df.loc[original_obj_df['object_id'] == x1])
                    new_obj_df = new_obj_df.append(original_obj_df.loc[original_obj_df['object_id'] == x1])
            # print(original_obj_df)
            print(new_obj_df)

            ocel_exporter.apply(new_df, filtered_log_path, obj_df=new_obj_df)

            log = createLog(usr_obj.id, str(i) + "events.jsonocel")
            logname = log.filename
            # logFile = None # get this
            event_df, obj_df = ocel_importer.apply(os.path.join(current_app.instance_path, 'logs') + "/performance/" + logname)

            # record start time here
            print('Started creating cube')
            start_time = time.time()
            createCube(str(i) + "events", log, getLogAttrs(filtered_log_path, str(i) + "events.jsonocel", event_df, obj_df), event_df, obj_df)
            performance[str(num_events)] = time.time() - start_time
            print("Performance " + str(i))
            print(performance[str(num_events)])
        print(performance)
        return jsonify({
            'stats': performance
        }), 200


