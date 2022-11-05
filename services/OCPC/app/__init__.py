import os, json
from collections import Counter
from sre_constants import SUCCESS
from app.apriori import Apriori
from app import pm4martin
import pandas as pd
from flask import Flask, render_template, abort, send_file, request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
# from pm4py.visualization.common import gview
import pm4py
import warnings
from pm4pymdl.objects.ocel.importer import importer as ocel_importer
from pm4pymdl.objects.ocel.exporter import exporter as ocel_exporter
import re
from . import freq_items as fi
import ast
from functools import cmp_to_key
import locale

from flask.cli import FlaskGroup

from dateutil  import parser

freqItems = {}

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth
from mlxtend.frequent_patterns import association_rules

# import pkg_resources
# pkg_resources.require("werkzeug==2.0.3")
# import werkzeug

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import timedelta

import logging

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder = 'static', instance_relative_config=True)

    #Logging
    # gunicorn_error_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers.extend(gunicorn_error_logger.handlers)
    # app.logger.setLevel(logging.DEBUG)
    # app.logger.debug('this will show in the log')

    # cors = CORS(app, resources={r"/foo": {"origins": "*"}})
    # app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, supports_credentials=True)

    UPLOAD_FOLDER = app.instance_path + '/uploads'
    app_settings = os.getenv('APP_SETTINGS')

    if app_settings is None:
        from . kb_config import DevelopmentConfig
        app_settings = DevelopmentConfig

    app.config.from_object(app_settings)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config['CORS_HEADERS'] = 'Content-Type'

    jwt = JWTManager(app)
    db.init_app(app)
    
    if (
            'SQLALCHEMY_DATABASE_URI' not in app.config and
            'SQLALCHEMY_BINDS' not in app.config
    ):
        warnings.warn(
            'Neither SQLALCHEMY_DATABASE_URI nor SQLALCHEMY_BINDS is set. '
            'Defaulting SQLALCHEMY_DATABASE_URI to "sqlite:///:memory:".'
        )

    print(app.config)


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for non-auth parts of app
    from .logs import logs as logs_blueprint
    app.register_blueprint(logs_blueprint)

    # blueprint for non-auth parts of app
    from .cubes import cubes as cubes_blueprint
    app.register_blueprint(cubes_blueprint)

    # blueprint for non-auth parts of app
    from .analyses import analyses as analyses_blueprint
    app.register_blueprint(analyses_blueprint)

    # blueprint for non-auth parts of app
    from .visualisations import visualisations as visualisations_blueprint
    app.register_blueprint(visualisations_blueprint)

    # example code
    # @app.after_request
    # def add_header(r):
    #     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #     r.headers["Pragma"] = "no-cache"
    #     r.headers["Expires"] = "0"
    #     r.headers['Cache-Control'] = 'public, max-age=0'
    #     return r

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    # app.config.from_pyfile('kb_config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('index.html')

    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({
            'status': 'success',
            'message': 'pong!',
            'container_id': os.uname()[1]
        })

    @app.route('/<path:req_path>', methods=['GET'])
    def dir_listing(req_path):
        BASE_DIR = '/static'

        # Joining the base and the requested path
        # abs_path = os.path.join(BASE_DIR, req_path)
        filename = os.path.join(app.root_path, 'static', req_path)

        # Return 404 if path doesn't exist
        if not os.path.exists(filename):
            print(filename)
            return abort(404)

        # Check if path is a file and serve
        if os.path.isfile(filename):
            return send_file(filename)

        # Show directory contents
        files = os.listdir(abs_path)
        return render_template('files.html', files=files)

    @app.route('/init_ocel')
    def init_ocel():
        # print(request.args)
        ocel_str = request.args.get('ocel_str', default='{}')
        with open("instance/logs/test.jsonocel", "w") as fo:
            fo.write(ocel_str)

        ocel = pm4py.read_ocel("instance/logs/test.jsonocel")

        print(ocel)
        out = {'result': 'saved'}

        return jsonify(result=out)
    
    @app.route('/get_stats')
    def get_stats():
        ocel = pm4py.read_ocel("instance/logs/test.jsonocel")

        js = json.loads(ocel.get_extended_table().to_json(orient = 'columns'))

        # print(ocel)

        statsAll = str(ocel)
        statsList = statsAll.split('\n')
        statsGeneral = statsList[0]
        m = re.search(r'(?<=\()[\s\w:,-]+(?=\))', statsGeneral)
        sub = re.sub(r'(?<=\w)\s(?=\w+)', '-', m.group(0))
        sub2 = re.sub(r'(?<=[\s])(?=[a-zA-Z-]+)','\"', sub)
        sub2 = '\"' + sub2
        sub3 = re.sub(r'(?<=[a-zA-Z])(?=:)','\"', sub2)

        statsObject = re.search(r'{[\w\s\'\':,]+}', statsList[2]).group(0)
        
        print(m.group(0))
        print(sub3)
        print(statsObject)
        print('\n\n')
        sub = json.loads('{' + sub3 + '}')

        statsObject = re.sub(r'\'', '\"', statsObject)
        statsObject = json.loads(statsObject)
        statsCombined = {**sub, **statsObject}
        print(statsCombined)

        return jsonify(statsCombined)

    def formatTimestamp(x, time_hierarchy):
        time = ''
        time += str(x.year)
        if not time_hierarchy == 'Year':
            time += '-'
            time += str(x.month)
            if not time_hierarchy == 'Month':
                time += '-'
                time += str(x.day)
                if not time_hierarchy == 'Day':
                    time += ' '
                    time += str(x.hour)
                    if not time_hierarchy == 'Hour':
                        time += ':'
                        time += str(x.minute)
        print(time)
        return time

    @app.route('/filter_ocel')
    def filter_ocel():

        index = request.args.get('index', default=0)
        materialisation = request.args.get('materialisation', default = 'Existance')
        filter = json.loads(request.args.get('filter', default='{}'))
        time_hierarchy = request.args.get('time_hierarchy', default='Month')
        print('time_hierarchy')
        print(time_hierarchy)
        overview_filter = filter['overview_filter']
        ocel = pm4py.read_ocel("instance/logs/test.jsonocel") # ORIGINAL LOG

        # FILTER ONLY SELECTED OBJECT TYPES
        only_select_types = pm4py.filter_ocel_object_attribute(ocel, "ocel:type", filter['type_filter'], positive=True)

        original_df, original_obj_df = ocel_importer.apply("instance/logs/test.jsonocel")

        # TODO add event/event filter

        if overview_filter['type_row'] == 'Events' or overview_filter['type_column'] == 'Events':
            event_is_row = overview_filter['type_row'] == 'Events'
            event_attr = overview_filter['row' if event_is_row else 'column']
            event_attr = ('ocel:' if event_attr[6:] == 'activity' or event_attr[6:] == 'timestamp' else '') + event_attr[6:]
            print("Event Attr: " + event_attr)

            # filter by event attr values
            event_attr_filtered = {}

            # values from selection
            event_values = [x[0 if event_is_row else 1] for x in overview_filter['selections']]

            # real_time = [x for x in log_e_values if
            #                 formatTimestamp(x, time_hierarchy) in event_values]


            if len(event_values)>0:
                if event_attr == 'ocel:timestamp':
                    # time values in log
                    log_e_values = [original_df.loc[x]['event_timestamp'] for x in original_df.index]

                    # allowed time values in log
                    allowed_time = [x for x in log_e_values if formatTimestamp(x, time_hierarchy) in event_values]

                    print(log_e_values)
                    print('Select values: ' + str(event_values))
                    # print('real Values: ' + str(real_time))
                    print('Mapped Values: ' + str(allowed_time))

                    event_attr_filtered = pm4py.filter_ocel_event_attribute(only_select_types, event_attr, allowed_time, positive=True)
                    print('Filtered')
                    print(event_attr_filtered)
                    # for x in event_attr_filtered:
                    #     print(event_attr_filtered[x])
                else:
                    event_attr_filtered = pm4py.filter_ocel_event_attribute(only_select_types, event_attr ,event_values, positive=True)
            else:
                event_attr_filtered = only_select_types

            # filter by object attr values
            obj_type = overview_filter['type_column'] if event_is_row else overview_filter['type_row']
            objAttr = overview_filter['column' if event_is_row else 'row']
            objValues = [x[1 if event_is_row else 0] for x in overview_filter['selections']]
            obj_event_attr_filtered = {}
            print('Object Type: ' + obj_type)
            print('Object Attr: ' + objAttr)
            type_filtered_ocel = pm4py.filter_ocel_object_attribute(event_attr_filtered, "ocel:type", [obj_type], positive=True)
            if len(objValues) > 0:
                for i in range(len(objValues)):
                    if objValues[i].isnumeric():
                        objValues[i] = float(int(objValues[i]))

                if type(objValues[0]) == 'int': #reformat the nums
                    objValues = [float(x) for x in objValues]
                    print('Object Values: ' + objValues)
                print(objValues)
                obj_event_attr_filtered = pm4py.filter_ocel_object_attribute(type_filtered_ocel, overview_filter['column' if event_is_row else 'row'] , objValues, positive=True)
            else:
                obj_event_attr_filtered = type_filtered_ocel

            print('Attr Filtered')
            print(obj_event_attr_filtered)

            attr_filtered = obj_event_attr_filtered
            pm4py.write_ocel(attr_filtered, "instance/logs/filteredOCEL" + index + ".jsonocel")

            original_type_filtered = pm4py.filter_ocel_object_attribute(only_select_types, "ocel:type", [obj_type], positive=True)
            pm4py.write_ocel(original_type_filtered, "instance/logs/tempOCEL" + index + ".jsonocel")
            # original_df, original_obj_df = ocel_importer.apply("instance/logs/tempOCEL" + index + ".jsonocel")

            filtered_df, filtered_obj_df = ocel_importer.apply("instance/logs/filteredOCEL" + index + ".jsonocel")
            print(filtered_df.info())

            if materialisation == 'Existance':
                # remove events where exact attr pairs don't match
                # example selection is [['a', 55], ['b', 66]] and until now we also include cases with ['a', 66]
                for x in filtered_df.index:
                    x_event_attr = filtered_df.loc[x][overview_filter['row' if event_is_row else 'column']]
                    x_obj_list = filtered_df.loc[x][obj_type]
                    # print(filtered_obj_df.info())
                    x_obj_attr_values_list = [filtered_obj_df.loc[x]['object_' + objAttr] for x in filtered_obj_df.index
                                              if
                                              (filtered_obj_df.loc[x]['object_id'] in x_obj_list)]

                    selection_pairs = [y for y in overview_filter['selections']]
                    event_index_in_pair = 0 if event_is_row else 1

                    print('x_attr')
                    print(x_event_attr)
                    print()

                    # list of pairs where event attr value matches the of event x
                    if(event_attr == "ocel:timestamp"):
                        select_matching_x_event_attr = [y for y in selection_pairs if
                                                    y[event_index_in_pair] == formatTimestamp(x_event_attr,
                                                                                              time_hierarchy)]
                    else:
                        select_matching_x_event_attr = [y for y in selection_pairs if
                                                    y[event_index_in_pair] == x_event_attr]

                    # print(filtered_df.loc[x])
                    # print(select_matching_x_event_attr)
                    print('matching attrs')
                    print(select_matching_x_event_attr)

                    # remove events where exact attr pairs don't match
                    # example selection is [['a', 55], ['b', 66]] and until now we also include cases with ['a', 66]
                    is_allowed = False
                    for value in x_obj_attr_values_list:
                        for y in select_matching_x_event_attr:
                            # 1 - even_index_in_pair = obj_index_in_pair
                            print('Value in event: ' + str(value))
                            print('Value in selection: ' + str(y[1 - event_index_in_pair]))

                            if y[1 - event_index_in_pair].isnumeric(): #FIGURURE A WAY TO MAKE THIS BETTER
                                # objValues[i] = float(int(objValues[i]))
                                if float(int(y[1 - event_index_in_pair])) == value:
                                    is_allowed = True
                                print('Allowed')
                                break
                            elif y[1 - event_index_in_pair] == value:
                                is_allowed = True
                                print('Allowed')
                                break
                        if is_allowed:
                            break

                    if not is_allowed:
                        filtered_df.drop(x, inplace=True)
                        print('Log Removed')
                    else:
                        print('Log included in final result')

                # ocel_exporter.apply(filtered_df, "instance/logs/filteredOCEL" + index + ".jsonocel", obj_df=filtered_obj_df)
            else:
                for x in filtered_df.index:
                    x_event_attr = filtered_df.loc[x][overview_filter['row' if event_is_row else 'column']]
                    x_obj_list = filtered_df.loc[x][obj_type]
                    print(filtered_obj_df.info())
                    x_obj_attr_values_list = [filtered_obj_df.loc[x]['object_' + objAttr] for x in filtered_obj_df.index
                                              if
                                              (filtered_obj_df.loc[x]['object_id'] in x_obj_list)]

                    selection_pairs = [y for y in overview_filter['selections']]
                    event_index_in_pair = 0 if event_is_row else 1

                    select_matching_x_event_attr = []
                    if (event_attr == "ocel:timestamp"):
                        select_matching_x_event_attr = [y for y in selection_pairs if
                                                        y[event_index_in_pair] == formatTimestamp(x_event_attr,
                                                                                                  time_hierarchy)]
                    else:
                        select_matching_x_event_attr = [y for y in selection_pairs if
                                                    y[event_index_in_pair] == x_event_attr]

                    print(filtered_df.loc[x])
                    print(select_matching_x_event_attr)

                    # remove events where exact attr pairs don't match
                    # example selection is [['a', 55], ['b', 66]] and until now we also include cases with ['a', 66]
                    is_allowed_overall = True
                    for value in x_obj_attr_values_list:
                        is_allowed = False
                        for y in select_matching_x_event_attr:
                            # 1 - even_index_in_pair = obj_index_in_pair
                            print('Value in event: ' + str(value))
                            print('Value in selection: ' + str(y[1 - event_index_in_pair]))
                            if y[1 - event_index_in_pair].isnumeric(): #FIGURURE A WAY TO MAKE THIS BETTER
                                # objValues[i] = float(int(objValues[i]))
                                if float(int(y[1 - event_index_in_pair])) == value:
                                    is_allowed = True
                                print('Allowed')
                                break
                            elif y[1 - event_index_in_pair] == value:
                                is_allowed = True
                                print('Allowed')
                                break
                        if not is_allowed:
                            is_allowed_overall = False
                            break

                    if not is_allowed_overall:
                        filtered_df.drop(x, inplace=True)
                        print('Log Removed')
                    else:
                        print('Log included in final result')

                print(filtered_df.info())
                for x in filtered_df.index:
                    row_filtered = filtered_df.loc[x]
                    print('\nRow Filtered')
                    print(row_filtered)
                    row_in_original = original_df.loc[original_df['event_id'] == filtered_df.loc[x]['event_id']]
                    if row_in_original.index>0:
                        row_in_original = row_in_original.loc[row_in_original.index[0]]
                        print('\nRow Original')
                        print(row_in_original)

                        if len(row_filtered[obj_type]) < len(row_in_original[obj_type]):
                            filtered_df.drop(x, inplace=True)

                # ocel_exporter.apply(filtered_df, "instance/logs/filteredOCEL" + index + ".jsonocel", obj_df=filtered_obj_df)
            # filtered_df, filtered_obj_df = ocel_importer.apply("instance/logs/filteredOCEL" + index + ".jsonocel")

            for x in original_df.index:
                x_id = original_df.loc[x]['event_id']

                rows_in_filtered = filtered_df.loc[filtered_df['event_id'] == x_id]
                if len(rows_in_filtered) == 0:
                    original_df.drop(x, inplace=True)

            ocel_exporter.apply(original_df, "instance/logs/filteredOCEL" + index + ".jsonocel", obj_df=original_obj_df)
        elif len(overview_filter['selections'])>0: #obj/obj filters
            objAttr =  overview_filter['row']
            print(objAttr)
            objValues = [x[0] for x in overview_filter['selections'] ]
            print(objValues)
            for i in range(len(objValues)):
                if objValues[i].isnumeric():
                    objValues[i] = float(int(objValues[i]))
            print(objValues)

            objAttr2 =  overview_filter['column']
            print(objAttr2)
            objValues2 = [x[1] for x in overview_filter['selections'] ]
            print(objValues2)
            for i in range(len(objValues2)):
                if objValues2[i].isnumeric():
                    objValues2[i] = float(int(objValues2[i]))
            print(objValues2)

            filtered_ocel1 = pm4py.filter_ocel_object_attribute(only_select_types, "ocel:type", [overview_filter['type_row'] ], positive=True)
            print(filtered_ocel1)
            filtered_ocel1 = pm4py.filter_ocel_object_attribute(filtered_ocel1, objAttr ,objValues, positive=True )
            print(filtered_ocel1)
            filtered_ocel2 = pm4py.filter_ocel_object_attribute(only_select_types, "ocel:type", [overview_filter['type_column'] ], positive=True)
            filtered_ocel2 = pm4py.filter_ocel_object_attribute(filtered_ocel2, objAttr2 ,objValues2, positive=True)

            pm4py.write_ocel(filtered_ocel1, "instance/logs/temp1filtered" + index + ".jsonocel")
            pm4py.write_ocel(filtered_ocel2, "instance/logs/temp2filtered" + index + ".jsonocel")

            filtered1_df, filtered1_obj_df = ocel_importer.apply("instance/logs/temp1filtered" + index + ".jsonocel")
            filtered2_df, filtered2_obj_df = ocel_importer.apply("instance/logs/temp2filtered" + index + ".jsonocel")

            events_combined = pd.merge(filtered1_df, filtered2_df, on='event_id')
            print(events_combined)

            objs_combined = filtered1_obj_df.append(filtered2_obj_df, ignore_index=True)

            print(objs_combined)

            if materialisation == 'Existance':
                for e in events_combined.index:
                    event = events_combined.loc[e]
                    objs1_list = event[overview_filter['type_row']]
                    objs2_list = event[overview_filter['type_column']]

                    is_allowed = False
                    for x in objs1_list:
                        for y in objs2_list:
                            obj1_row = objs_combined.loc[objs_combined['object_id'] == x]
                            obj2_row = objs_combined.loc[objs_combined['object_id'] == y]

                            if not obj1_row.empty and not obj2_row.empty:
                                obj1_value = obj1_row.iloc[0]['object_' + objAttr]
                                if isinstance(obj1_value, float):
                                    obj1_value = int(obj1_value)
                                obj2_value = obj2_row.iloc[0]['object_' + objAttr2]
                                if isinstance(obj2_value, float):
                                    obj2_value = int(obj2_value)
                                print([str(obj1_value), str(obj2_value)])
                                print(overview_filter['selections'])
                                if [str(obj1_value), str(obj2_value)] in overview_filter['selections']:
                                    print('Allowed')
                                    is_allowed = True

                    if not is_allowed:
                        events_combined.drop(e, inplace=True)
                        print('Log Removed')
                    else:
                        print('Log included in final result')
                print(events_combined)
            else:
                for e in events_combined.index:
                    allowed_overall = True
                    event = events_combined.loc[e]
                    objs1_list = event[overview_filter['type_row']]
                    objs2_list = event[overview_filter['type_column']]

                    for x in objs1_list:
                        is_allowed = False
                        for y in objs2_list:
                            obj1_row = objs_combined.loc[objs_combined['object_id'] == x]
                            obj2_row = objs_combined.loc[objs_combined['object_id'] == y]

                            if not obj1_row.empty and not obj2_row.empty:
                                obj1_value = obj1_row.iloc[0]['object_' + objAttr]
                                if isinstance(obj1_value, float):
                                    obj1_value = int(obj1_value)
                                obj2_value = obj2_row.iloc[0]['object_' + objAttr2]
                                if isinstance(obj2_value, float):
                                    obj2_value = int(obj2_value)
                                print([str(obj1_value), str(obj2_value)])
                                print(overview_filter['selections'])
                            if not [str(obj1_value), str(obj2_value)] in overview_filter['selections']:
                                print('Allowed')
                                is_allowed = True
                                break

                    if not is_allowed:
                        events_combined.drop(e, inplace=True)
                        print('Log Removed')
                    else:
                        print('Log included in final result')
                print(events_combined)

                # Parameters.EVENT_ID = > the
                # event
                # ID
                # column - Parameters.OBJECT_ID = > the
                # object
                # ID
                # column - Parameters.OBJECT_TYPE = > the
                # object
                # type
                # column
                # parameters = {log_exporter.Variants.CLASSIC.value.Parameters.EVENT_ID: "event_id",
                #               log_exporter.Variants.CLASSIC.value.Parameters.OBJECT_ID: "object_id",
                #               log_exporter.Variants.CLASSIC.value.Parameters.OBJECT_TYPE: 'object_type'}
                # ocel_exporter.apply(events_combined, "instance/logs/filteredOCEL" + index + ".jsonocel",
                #                     obj_df=original_obj_df, parameters=parameters)

            for x in original_df.index:
                x_id = original_df.loc[x]['event_id']

                rows_in_filtered = events_combined.loc[events_combined['event_id'] == x_id]
                if len(rows_in_filtered) == 0:
                    original_df.drop(x, inplace=True)

                ocel_exporter.apply(original_df, "instance/logs/filteredOCEL" + index + ".jsonocel", obj_df=original_obj_df)
        else:
            pm4py.write_ocel(only_select_types, "instance/logs/filteredOCEL" + index + ".jsonocel")

        # filtered_ocel = pm4py.read_ocel("instance/logs/filteredOCEL" +index + ".jsonocel") # ORIGINAL LOG

        # filtered_df, filtered_obj_df = ocel_importer.apply("instance/logs/filteredOCEL" + index + ".jsonocel")
        #
        # for x in original_df.index:
        #     x_id = original_df.loc[x]['event_id']
        #
        #     rows_in_filtered = filtered_df.loc[filtered_df['event_id'] == x_id]
        #     if len(rows_in_filtered) == 0:
        #         original_df.drop(x, inplace=True)
        #
        # ocel_exporter.apply(original_df, "instance/logs/filteredOCEL" + index + ".jsonocel", obj_df=original_obj_df)

        out = ''
        with open("instance/logs/filteredOCEL" +index + ".jsonocel") as f:
            out = f.read()
        return jsonify(result=out)

    @app.route('/flatten_ocel')
    def flatten_ocel():
        index = request.args.get('index', default=0)
        flatten_type = request.args.get('type', default='')
        #
        # if flatten_type == '':
        #     return jsonify({'error': 'No type was specified'})
        #
        ocel = pm4py.read_ocel(os.path.join("instance",'logs', "filteredOCEL"+index+".jsonocel"))
        # flattened_log = pm4py.ocel_flattening(ocel, flatten_type)
        # dataframe = log_converter.apply(flattened_log, variant=log_converter.Variants.TO_DATA_FRAME)
        # dataframe.to_csv("instance/logs/flatennedLogs" + index + ".csv")

        event_df, obj_df = ocel_importer.apply("instance/logs/filteredOCEL" + index + ".jsonocel")
        js = event_df.to_json(orient='columns')
        return jsonify({'result': "OCEL " + index + " was flatenned",
        'data': js})

    @app.route('/generate_dfg')
    def generate_dfg():
        index = request.args.get('index', default=0)
        type = request.args.get('type', default='Frequency')
        perf_agr_measure = request.args.get('performace_measure', default='median')
        ocel = pm4py.read_ocel(os.path.join("instance",'logs', "filteredOCEL"+index+".jsonocel"))
        edge_threshold = request.args.get('edge_threshold', default=0)
        if isinstance(edge_threshold, str):
            edge_threshold = 0 if edge_threshold == '' or not edge_threshold.isnumeric() else int(edge_threshold)
        act_threshold = request.args.get('act_threshold', default=0)
        if isinstance(act_threshold, str):
            act_threshold = 0 if act_threshold == '' or not act_threshold.isnumeric() else int(act_threshold)

        ocdfg = None
        try:
            ocdfg = pm4py.discover_ocdfg(ocel)
        except:
            return {'error': 'Could not discover a DFG'}

        if ocdfg:
            if type == 'Frequency':
                pm4py.save_vis_ocdfg(ocdfg, file_path='instance/dfgs/dfg'+index+'.svg', annotation='frequency', edge_threshold=edge_threshold, act_threshold=act_threshold)
            else:
                pm4py.save_vis_ocdfg(ocdfg, file_path='instance/dfgs/dfg' + index + '.svg', annotation='performance', edge_threshold=edge_threshold, performance_aggregation=perf_agr_measure, act_threshold=act_threshold)
            # visualizer.save(gviz, 'instance/dfgs/dfg'+index+'.svg')
            return {'result': SUCCESS}
        else:
            return {'error': 'No DFG was created'}

    @app.route('/get_svg/<int:index>')
    def get_svg(index):
        dfg_name = 'dfg'+str(index)+'.svg'
        print(dfg_name)
        return send_file('/Users/martinvichev/Desktop/WiSe 21:22/Bachelorarbeit/OCPC/instance/dfgs/' + dfg_name, as_attachment=False, cache_timeout=0)
 
    @app.route('/get_freq_items')
    def get_freq_items():
        attr = request.args.get('attr', default='')
        dataset = json.loads(request.args.get('dataset', default='[]'))

        index = request.args.get('index', default = 1)
        ocel = pm4py.read_ocel(os.path.join("instance",'logs', "filteredOCEL"+str(index)+".jsonocel"))

        min_supp = float(request.args.get('min_supp', default = 0))/100
        min_conf = float(request.args.get('min_conf', default=0))/100
        min_lift = float(request.args.get('min_lift', default=0))/100
        set_size = int(request.args.get('set_size', default = 1))

        freq_set_alg = request.args.get('freq_set_alg', default="apriori")

        # dataset = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
        #            ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
        #            ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
        #            ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
        #            ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]

        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        print("Input DF")
        print(df)
        frequent_itemsets = None
        if freq_set_alg ==  "apriori":
            frequent_itemsets = apriori(df, min_support=min_supp, use_colnames=True)
        elif freq_set_alg == "fpmax":
            frequent_itemsets = fpmax(df, min_support=min_supp, use_colnames=True)
        elif freq_set_alg == "fpgrowth":
            frequent_itemsets = fpgrowth(df, min_support=min_supp, use_colnames=True)
        else:
            print("Wrong algorithm")

        print("MlXtend Out")
        print(frequent_itemsets)

        # if frequent_itemsets:

        assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_conf)
        assoc_rules_out = []
        for i in assoc_rules.index:
            row_out=[]
            row = assoc_rules.loc[i]
            row_out.append(list(row['antecedents']))
            row_out.append(list(row['consequents']))
            row_out.append(row['support'])
            row_out.append(row['confidence'])
            row_out.append(row['lift'])
            assoc_rules_out.append(row_out)

        print("Association rules")
        print(assoc_rules_out)

        #OTHER LIBRARY
        # apriori = Apriori(dataset=dataset)
        # print(type(min_supp))
        # apriori_result = apriori.generate_L(min_sup=min_supp, min_conf=min_conf)
        # freqItems1 = apriori_result['freq_itemsets']
        # assoc_rules = apriori_result['assoc_rules']

        # trasform set to list and filter out only sets with given size
        out = {'data': []}
        # for itemSet in freqItems1:
        #   row = frequent_itemsets.loc[x]
        #   if len(itemSet[0]) >= set_size:
        #       listMappedObjs = []
        #       for obj in itemSet[0]:
        #           listMappedObjs.append(obj)
        #       out['data'].append([listMappedObjs, itemSet[1]])

        # print("Apriori out: ")
        # print(freqItems1)

        for itemSetIndex in frequent_itemsets.index:
            row = frequent_itemsets.loc[itemSetIndex]
            if len(row['itemsets']) >= set_size:
                listMappedObjs = []
                for obj in row['itemsets']:
                    listMappedObjs.append(obj)
                out['data'].append([listMappedObjs, row['support']])

        print("Flask out: ")
        print(out)

        # edited_out = {'data': str(out['data'])}
        # with open('instance/freq_itemsets/filteredOCEL' + str(index) + '.json', 'w') as f:
        #     json.dump(edited_out, f)

        freqItems[index] = out
        # print({'freq_itemsets': out['data'],
        #                        'assoc_rules': assoc_rules})
        return jsonify(result={'freq_itemsets': out['data'],
                               'assoc_rules': assoc_rules_out})

    @app.errorhandler(404)
    @app.errorhandler(405)
    def _handle_api_error(ex):
        if request.path.startswith('/api/'):
            return jsonify(error=str(ex)), ex.code
        else:
            return ex

    @app.route('/freq_items/filtered_events')
    def getFilteredFreqentItemEvents():
        # itemsets = request.args.get('index', default=0)
        # materialisation = request.args.get('materialisation', default='Existance')
        itemsets = request.args.get('itemsets', default='[]')
        index = request.args.get('index', default=1)
        # time_hierarchy = request.args.get('time_hierarchy', default='Month')

        itemsets = ast.literal_eval(itemsets)
        itemsets = [n.strip() for n in itemsets]

        filtered_df, filtered_obj_df = ocel_importer.apply("instance/logs/filteredOCEL" + index + ".jsonocel")
        # ocel = pm4py.read_ocel(os.path.join("instance", 'logs', "filteredOCEL" + str(index) + ".jsonocel"))

        with open('instance/freq_itemsets/filteredOCEL' + index + '.json', 'w') as f: # Opening JSON file
            # returns JSON object as
            # a dictionary
            data = json.load(f)

        # Iterating through the json
        # list
        for i in data['data']:
            print(i)

        freq_items_filtered_df = filtered_df.copy()
        # for i in filtered_df.index:
        for i in range(len(filtered_df.index)-1, -1, -1):
            print("Event in iterator:")
            print(filtered_df.loc[i])
            print("Event in copy:")
            print(freq_items_filtered_df.loc[i])
            e_fprint = fi.get_events_freq_fingerprints(freq_items_filtered_df.loc[i])
            if not e_fprint in data['data']:
                freq_items_filtered_df.drop(i, inplace=True)
                print('deleted')

        ocel_exporter.apply(freq_items_filtered_df, "instance/logs/freqItemsFilteredOCEL" + index + ".jsonocel", obj_df=filtered_obj_df)

    @app.route('/freq_items/filtered_dfg')
    def getFilteredFreqentItemDfg():
        # itemsets = request.args.get('index', default=0)
        # materialisation = request.args.get('materialisation', default='Existance')
        itemsets = request.args.get('itemsets', default='[]')
        index = request.args.get('index', default=1)
        freq_item_filter = json.loads(request.args.get('filter', default='{}'))
        # time_hierarchy = request.args.get('time_hierarchy', default='Month')

        print("Itensets as str: " + itemsets)
        print("Intex: " + str(index))
        print("Filter: " + str(freq_item_filter))


        # PARSE STR TO LIST
        itemsets = ast.literal_eval(itemsets)
        itemsets = [n.strip() for n in itemsets]

        print("Itensets as list: " + str(itemsets))


        filtered_df, filtered_obj_df = ocel_importer.apply("instance/logs/filteredOCEL" + str(index) + ".jsonocel")
        # ocel = pm4py.read_ocel(os.path.join("instance", 'logs', "filteredOCEL" + str(index) + ".jsonocel"))

        print("Ocel Event Dataframe")
        print(filtered_df)

        fItems = freqItems[index]
        print("Frequent Items for Analysis: " + str(index))
        # print(fItems)
        for i in fItems['data']:
            print(i)

        # with open('instance/freq_itemsets/filteredOCEL' + str(index) + '.json', 'r') as f:  # Opening JSON file
        #     # returns JSON object as
        #     # a dictionary
        #     print("FILE READ")
        #     print(f)
        #     print(f.read())
        #
        #     data = f.read()
        #
        # print("DATA")
        # print(data)
        # data = json.loads(data)

        fItems = [x[0] for x in fItems['data']]
        for i in fItems:
            i.sort()
        print("Sorted Frequent Items")
        for i in fItems:
            print(i)
        hashed_data = [Counter(s) for s in fItems]
        print("Hashed Sorted Frequent Items")
        for i in hashed_data:
            print(i)
        freq_items_filtered_df = filtered_df.copy()

        # for i in filtered_df.index:
        for i in range(len(filtered_df.index) - 1, -1, -1):
            print("Event in iterator:")
            print(filtered_df.loc[i])
            print("Event in copy:")
            print(freq_items_filtered_df.loc[i])
            e_fprint = fi.get_events_freq_fingerprints(freq_items_filtered_df.loc[i], freq_item_filter, filtered_obj_df)

            # e_fprint = [str(int)x) for x in e_fprint]
            temp = []
            for x in e_fprint:
                print(x)
                if isinstance(x, str):
                    temp.append(x)
                else:
                    temp.append(str(int(x)))
            e_fprint = temp

            print("Counter(e_fprint)")
            print(Counter(e_fprint))

            print("Counter( Sourted e_fprint)")
            e_fprint.sort()
            print(Counter(e_fprint))

            if not Counter(e_fprint) in hashed_data:
                print("e_fprint")
                print(e_fprint)
                print("hashed_data")
                # print(hashed_data)
                for x in hashed_data:
                    print(x)
                freq_items_filtered_df.drop(i, inplace=True)
                print('deleted')

        print('Result')
        print(freq_items_filtered_df)

        print("Num Logs left: " + str(len(freq_items_filtered_df.index)))

        ocel_exporter.apply(freq_items_filtered_df, "instance/logs/freqItemsFilteredOCEL" + str(index) + ".jsonocel",
                            obj_df=filtered_obj_df)

        # index = request.args.get('index', default=0)
        type = request.args.get('type', default='Frequency')
        perf_agr_measure = request.args.get('performace_measure', default='median')

        ocel = pm4py.read_ocel(os.path.join("instance", 'logs', "freqItemsFilteredOCEL" + str(index) + ".jsonocel"))
        edge_threshold = request.args.get('edge_threshold', default=0)

        if isinstance(edge_threshold, str):
            edge_threshold = 0 if edge_threshold == '' or not edge_threshold.isnumeric() else int(edge_threshold)
        act_threshold = request.args.get('act_threshold', default=0)
        if isinstance(act_threshold, str):
            act_threshold = 0 if act_threshold == '' or not act_threshold.isnumeric() else int(act_threshold)

        ocdfg = None
        try:
            ocdfg = pm4py.discover_ocdfg(ocel)
        except:
            return {'error': 'Could not discover a DFG'}

        if ocdfg:
            if type == 'Frequency':
                pm4py.save_vis_ocdfg(ocdfg, file_path='instance/dfgs/freqItemsDfg' + str(index) + '.svg', annotation='frequency',
                                     edge_threshold=edge_threshold, act_threshold=act_threshold)
            else:
                pm4py.save_vis_ocdfg(ocdfg, file_path='instance/dfgs/freqItemsDfg' + str(index) + '.svg', annotation='performance',
                                     edge_threshold=edge_threshold, performance_aggregation=perf_agr_measure,
                                     act_threshold=act_threshold)
            # visualizer.save(gviz, 'instance/dfgs/dfg'+index+'.svg')

            # dfg_name = 'freqItemsDfg' + str(index) + '.svg'
            # print(dfg_name)
            # return send_file('/Users/martinvichev/Desktop/WiSe 21:22/Bachelorarbeit/OCPC/instance/dfgs/' + dfg_name,
            #                  as_attachment=True, cache_timeout=0)
            return {'result': SUCCESS}
        else:
            return {'error': 'No DFG was created'}

    @app.route('/freq_items/get_dfg_svg/<int:index>')
    def getFreqSVG(index):
        dfg_name = 'freqItemsDfg' + str(index) + '.svg'
        print(dfg_name)
        return send_file('/Users/martinvichev/Desktop/WiSe 21:22/Bachelorarbeit/OCPC/instance/dfgs/' + dfg_name, as_attachment=False, cache_timeout=0)

    return app