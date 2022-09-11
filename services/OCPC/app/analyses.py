from flask import Blueprint, make_response, redirect, url_for, request, jsonify, current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Analysis
from flask_cors import CORS
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity, verify_jwt_in_request
import json
from markupsafe import escape
import os
import pm4py
from pm4pymdl.objects.ocel.importer import importer as ocel_importer
from pm4pymdl.objects.ocel.exporter import exporter as ocel_exporter
import pandas as pd

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth
from mlxtend.frequent_patterns import association_rules
from . import freq_items as fi

analyses = Blueprint('analyses', __name__, url_prefix="/analyses")
CORS(analyses, supports_credentials=True)

# example code
@analyses.after_request
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

# creates a comparison analysis
@analyses.route('/add_comp', methods=['POST'])
@jwt_required()
def add_comp_analysis():
    data = json.loads(request.get_data())
    print(data)
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()
    if usr_obj:
        pass

@analyses.route('/add', methods=['POST'])
@jwt_required()
def add_analysis():
    data = json.loads(request.get_data())
    print(data)
    name = data.get('name')
    cubename = data.get('cube')
    logname = data.get('logname')
    # filters = data.get()

    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        print(usr_obj.logs)
        print(logname)
        for log in usr_obj.logs:
            if log.filename == logname:
                for cube in log.cubes:
                    if cube.name == cubename:
                        new_analysis = Analysis(name=name, cube_id=cube.id, filters=json.dumps([]), visualisations=json.dumps([]))
                        # add the new user to the database
                        db.session.add(new_analysis)
                        db.session.commit()

                        log_path = os.path.join(current_app.instance_path, 'logs') + "/" + log.filename
                        filtered_log_path = os.path.join(current_app.instance_path,
                                                         'logs') + "/" + usr + "_" + log.filename.replace('.jsonocel',
                                                                                                          '') + "_" + "filtered" + ".jsonocel"
                        original_df, original_obj_df = ocel_importer.apply(log_path)

                        ocel_exporter.apply(original_df, filtered_log_path,
                                            obj_df=original_obj_df)

                        response = make_response({"success": "New Analysis was created successfully"})
                        return response

                response = make_response({"error": "Cube not fund"})
                return response

        response = make_response({"error": "Log not fund"})
        return response
    else:
        return jsonify(message="Unauthorized no user found"), 401

@analyses.route('/delete/<analysisname>', methods=['POST'])
@jwt_required()
def delete_analysis(analysisname):
    data = json.loads(request.get_data())
    print(data)
    cubename = data.get('cube')
    logname = data.get('log')
    analysisname = data.get('analysis')
    print(analysisname)

    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        print(usr_obj.logs)
        # print(usr_obj.cubes)
        # print(logname)
        for log in usr_obj.logs:
            if log.filename == logname:
                for cube in log.cubes:
                    if cube.name == cubename:
                        for analysis in cube.analyses:
                            if analysis.name == analysisname:
                                db.session.delete(analysis)
                                db.session.commit()

                                #TODO delete filtered log used from analysis

                        # new_analysis = Analysis(name=name, cube_id=cube.id, filters=json.dumps([]), visualisations=json.dumps([]))
                        # # add the new user to the database
                        # db.session.add(new_analysis)
                        # db.session.commit()
                        #
                        # log_path = os.path.join(current_app.instance_path, 'logs') + "/" + log.filename
                        # filtered_log_path = os.path.join(current_app.instance_path,
                        #                                  'logs') + "/" + usr + "_" + log.filename.replace('.jsonocel',
                        #                                                                                   '') + "_" + "filtered" + ".jsonocel"
                        # original_df, original_obj_df = ocel_importer.apply(log_path)
                        #
                        # ocel_exporter.apply(original_df, filtered_log_path,
                        #                     obj_df=original_obj_df)

                        response = make_response({"success": "Analysis \"" + analysisname + "\" was deleted successfully"})
                        return response

                response = make_response({"error": "Cube not fund"}, 400)
                return response
        print({"error": "Log not fund"})
        response = make_response({"error": "Log not fund"}, 400)
        return response
    else:
        return jsonify(message="Unauthorized no user found"), 401

@analyses.route('/all', methods=['POST'])
@jwt_required()
def get_analyses():
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        list_analyses = []
        for log in usr_obj.logs:
            for cube in log.cubes:
                for analyses in cube.analyses:
                    list_analyses.append(analyses)
        return jsonify({
            'analyses': list_analyses
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@analyses.route('/get/<analysisname>', methods=['POST'])
@jwt_required()
def get_analysis(analysisname):
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                for analysis in cube.analyses:
                    if analysis.name == escape(analysisname):
                        return jsonify({
                            'sourcelog': log.filename,
                            'cube': {
                                'name': cube.name,
                                'dimens': json.loads(cube.dimens),
                            },
                            'name': analysis.name,
                            'filters': json.loads(analysis.filters),
                            'visualisations': json.loads(analysis.visualisations),
                        }), 200

        return jsonify({
            'error': "Analysis not found"
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@analyses.route('/set/<analysisname>/filters', methods=['POST'])
@jwt_required()
def setAnalysisFilters(analysisname):
    jwt_data = verify_jwt_in_request()
    # print(jwt_data)

    usr = get_jwt_identity()
    # print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    data = json.loads(request.get_data())
    # print(data)
    # name = data.get('name')
    new_filter = data.get('new_filter')
    print(new_filter)

    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                for analysis in cube.analyses:
                    if analysis.name == escape(analysisname):
                        # TODO compute filtered ocel for this cube and store it

                        log_path = os.path.join(current_app.instance_path, 'logs') + "/" + log.filename

                        filtered_log_path = os.path.join(current_app.instance_path,
                                                         'logs') + "/" + usr + "_" + log.filename.replace('.jsonocel', '') + "_" + "filtered" + ".jsonocel"
                        ocel = pm4py.read_ocel(filtered_log_path)  # ORIGINAL LOG

                        original_df, original_obj_df = ocel_importer.apply(filtered_log_path)
                        # print(list(original_obj_df.columns))
                        # print(original_obj_df)
                        # TODO SEE IF THE IS NEEDED AT ALL
                        # FILTER ONLY SELECTED OBJECT TYPES
                        # only_select_types = pm4py.filter_ocel_object_attribute(ocel, "ocel:type", filter['type_filter'],
                        #                                                        positive=True)

                        # 1. FILTER OCELS BASED ON DIM1 VALUES AND DIM2 SEPARATELY
                        # 2. STORE RESULT IN 2 TEMP FILES
                        # 3. LOAD TEMP FILES AS DATAFRAMES
                        # 4. COMBINE THE RESULTING LOGS BASED ON THE MATERIALISATION
                        if new_filter['type'] == 'dims':
                            if len(new_filter['selections']) > 0:  # obj/obj filters
                                selections = [[x.split(',')[0], x.split(',')[1]] for x in new_filter["selections"]]

                                # get and adjust dim1 selected values
                                objAttr = new_filter['dim1']
                                # print("Attr1: " + objAttr)
                                objValues = [x[0] for x in selections]
                                # print("Attr1 Values: " + objAttr)
                                # print(objValues)
                                for i in range(len(objValues)):
                                    if objValues[i].isnumeric():
                                        objValues[i] = float(int(objValues[i]))
                                    elif isfloat(objValues[i]):
                                        objValues[i] = float(objValues[i])
                                # print("Attr1 Values edited: " + objAttr)
                                # print(objValues)

                                # get and adjust dim2 selected values
                                objAttr2 = new_filter['dim2']
                                # print("Attr2: " + objAttr2)
                                objValues2 = [x[1] for x in selections]
                                # print("Attr2 Values: " + str(objValues2))
                                for i in range(len(objValues2)):
                                    if objValues2[i].isnumeric():
                                        objValues2[i] = float(int(objValues2[i]))
                                    elif isfloat(objValues2[i]):
                                        objValues2[i] = float(objValues2[i])
                                print("Attr2 Values edited: " + str(objValues2))

                                #FILTER OCEL TO INCLUDE OBJECT OF TYPE_DIM1
                                #AND THEN SELECT ONLY THE OBJECT THAT HAVE VALUES ONE OF THE SPECIFIED VALUES
                                filtered_ocel1 = pm4py.filter_ocel_object_attribute(ocel, "ocel:type",
                                                                                    [new_filter['type_dim1']],
                                                   positive=True)
                                print(filtered_ocel1)
                                objAttr = objAttr[7:]
                                filtered_ocel1 = pm4py.filter_ocel_object_attribute(filtered_ocel1, objAttr, objValues,
                                                                                    positive=True)
                                print(filtered_ocel1)

                                # FILTER OCEL TO INCLUDE OBJECT OF TYPE_DIM2
                                # AND THEN SELECT ONLY THE OBJECT THAT HAVE VALUES ONE OF THE SPECIFIED VALUES
                                filtered_ocel2 = pm4py.filter_ocel_object_attribute(ocel, "ocel:type",
                                                                                    [new_filter['type_dim2']],
                                                                             positive=True)
                                objAttr2 = objAttr2[7:]
                                filtered_ocel2 = pm4py.filter_ocel_object_attribute(filtered_ocel2, objAttr2, objValues2,
                                                                                    positive=True)

                                # STORE RESULT IN TEMP FILES
                                temp1_log_path = os.path.join(current_app.instance_path, 'logs') + "/" +usr + "_temp1" + ".jsonocel"
                                pm4py.write_ocel(filtered_ocel1, temp1_log_path)

                                temp2_log_path = os.path.join(current_app.instance_path, 'logs') + "/" +usr + "_temp2" + ".jsonocel"
                                pm4py.write_ocel(filtered_ocel2, temp2_log_path)

                                # LOAD THE STORED TYPE-FILTERED OCELs AS DATAFRAMES AND COMBINE THEM
                                filtered1_df, filtered1_obj_df = ocel_importer.apply(temp1_log_path)
                                filtered2_df, filtered2_obj_df = ocel_importer.apply(temp2_log_path)
                                # events_combined = pd.merge(filtered1_df, filtered2_df, on='event_id')
                                events_combined = filtered1_df.append(filtered2_df, ignore_index=True)
                                objs_combined = filtered1_obj_df.append(filtered2_obj_df, ignore_index=True)

                                # BASED ON THE MATERIALISATION
                                # CHECK EVERY EVENT AND WHETHER IT INCLUDES AN OBJECT FROM THE COMBINED TEMP FILTERED OBJECTS
                                if new_filter['mat'] == 'Existence':
                                    # print(list(events_combined.columns))
                                    for e in events_combined.index:
                                        event = events_combined.loc[e]
                                        # IN THE DATAFRAME THE LIST THE OBJECTS OF SPECIFIC TYPE ARE STORES AS A LIST WITH KEY=OBJECT_TYPE

                                        objs1_list = event[new_filter['type_dim1']]
                                        objs2_list = event[new_filter['type_dim2']]

                                        is_allowed = False
                                        # TODO SEPARATE THIS TO 2 SEPARATE LOOPS TO MAKE FASTER
                                        print(objs1_list)
                                        print(objs2_list)
                                        if not pd.isna(objs1_list).any() and not pd.isna(objs2_list).any():
                                            for x in objs1_list:
                                                for y in objs2_list:
                                                    obj1_row = objs_combined.loc[objs_combined['object_id'] == x]
                                                    obj2_row = objs_combined.loc[objs_combined['object_id'] == y]

                                                    if not obj1_row.empty and not obj2_row.empty:
                                                        obj1_value = obj1_row.iloc[0]['object_' + objAttr]
                                                        # if isinstance(obj1_value, float):
                                                        #     obj1_value = int(obj1_value)
                                                        obj2_value = obj2_row.iloc[0]['object_' + objAttr2]
                                                        # if isinstance(obj2_value, float):
                                                        #     obj2_value = int(obj2_value)
                                                        print([str(obj1_value), str(obj2_value)])
                                                        print(new_filter['selections'])
                                                        if str(str(obj1_value)+ "," +str(obj2_value)) in new_filter['selections']:
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
                                        objs1_list = event[new_filter['type_dim1']]
                                        objs2_list = event[new_filter['type_dim2']]

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
                                                    print(new_filter['selections'])
                                                if not str(str(obj1_value)+","+str(obj2_value)) in new_filter['selections']:
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

                                #
                                for x in original_df.index:
                                    x_id = original_df.loc[x]['event_id']

                                    rows_in_filtered = events_combined.loc[events_combined['event_id'] == x_id]
                                    if len(rows_in_filtered) == 0:
                                        original_df.drop(x, inplace=True)

                                ocel_exporter.apply(original_df, filtered_log_path,
                                                        obj_df=original_obj_df)

                                #TODO DELETE THE CREATED TEMP FILES
                            else:
                                pm4py.write_ocel(ocel, filtered_log_path)
                        # FILTER ALL ROWS FROM DF BASED ON EVENT FOOTPRINT : see fi.get_events_freq_fingerprints
                        elif new_filter['type'] == 'freq_items':
                            filtered_df, filtered_obj_df = ocel_importer.apply(filtered_log_path)
                            itemsets = new_filter['selections'];
                            filter_attrs = new_filter['attrs']

                            # print(itemsets)
                            temp = []
                            for set in itemsets:
                                newSet = []
                                for item in set:
                                    print(item)
                                    print(is_number_regex(item))
                                    if is_number_regex(item):
                                        print("converted")
                                        newSet.append(float(item))
                                    else:
                                        newSet.append(item)
                                temp.append(newSet)

                            itemsets = temp
                            # print(itemsets)
                            # filtered_df = filtered_df.loc[fi.get_events_freq_fingerprints(filtered_df, filter_attrs, filtered_obj_df) in itemsets]
                            # filtered_df = filtered_df.apply(lambda row:
                            #     row if fi.get_events_freq_fingerprints(row, filter_attrs, filtered_obj_df) in itemsets, axis=1))=
                            #
                            print(filtered_df)
                            print('Filtering')
                            # for x in filtered_df.index:
                            #     filtered_df.loc[x]


                            # filtered_df = filtered_df[filtered_df.apply(lambda row: isSubsetOfASet(fi.get_events_freq_fingerprints(row, filter_attrs, filtered_obj_df), itemsets), axis=1)]

                            freq_items_filtered_df = filtered_df.copy()
                            for i in range(len(filtered_df.index) - 1, -1, -1):
                                print("Event in iterator:")
                                print(filtered_df.loc[i])
                                print("Event in copy:")
                                print(freq_items_filtered_df.loc[i])
                                e_fprint = fi.get_events_freq_fingerprints(freq_items_filtered_df.loc[i], filter_attrs, filtered_obj_df)
                                print(e_fprint)
                                if not isSubsetOfASet(e_fprint, itemsets):
                                    freq_items_filtered_df.drop(i, inplace=True)
                                    print('deleted')

                            print(freq_items_filtered_df)
                            # print(filtered_log_path)
                            ocel_exporter.apply(freq_items_filtered_df, filtered_log_path, obj_df=original_obj_df)

                        # Save new Filter in the given analysis's list
                        new_list_filters = json.loads(analysis.filters)
                        new_list_filters.append(new_filter)
                        # print("New Filter LIst: "+ json.dumps(new_list_filters))
                        analysis.filters = json.dumps(new_list_filters)
                        # print(analysis.id)
                        # print(analysis.filters)
                        db.session.commit()
                        return jsonify({
                            'message': "Filters saved"
                        }), 200

        return jsonify({
            'error': "Analysis not found"
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

import re
def is_number_regex(s):
    """ Returns True is string is a number. """
    if re.match("^\d+?\.\d+?$", s) is None:
        return s.isdigit()
    return True

# Takes a set 'a' and a Set of sets 'b' and then checks if any of the sets in 'b' is a subset of 'a'
def isSubsetOfASet(mySet, setOfSets):
    for x in setOfSets:
        print(mySet)
        print(setOfSets)
        if set(x).issubset(set(mySet)):
            print('added')
            return True
    print('Not added')
    return False


@analyses.route('/set/<analysisname>/visualisations', methods=['POST'])
@jwt_required()
def setAnalysisVis(analysisname):
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    data = json.loads(request.get_data())
    print(data)
    # name = data.get('name')
    vis_list = data.get('visualisations')
    print(vis_list)

    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                for analysis in cube.analyses:
                    if analysis.name == escape(analysisname):
                        analysis.visualisations = json.dumps(vis_list)
                        print(analysis.id)
                        print(analysis.visualisations)
                        db.session.commit()
                        return jsonify({
                            'message': "Visualisations saved"
                        }), 200

        return jsonify({
            'error': "Analysis not found"
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@analyses.route('/freq_itemsets', methods=['POST'])
@jwt_required()
def get_freq_itemsets():
    # Auth
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    # ARGS
    data = json.loads(request.get_data())
    analysis_name = data.get('analysisname')
    print("Analysis Name: ")
    print(analysis_name)

    # vis_index = data.get('index')

    freq_set_alg = data.get('freq_set_alg') if data.get('freq_set_alg') else 'apriori'

    #THE GOOD STUFF
    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                for analysis in cube.analyses:
                    if analysis.name == escape(analysis_name):
                        sel_freq_attrs = data.get('attrs')
                        min_supp = data.get('min_supp')
                        set_size = data.get('set_size')

                        print("Attrs: " + str(sel_freq_attrs))
                        print(sel_freq_attrs)

                        print("Supp: " + str(min_supp))
                        print(min_supp)

                        print("Size: " + str(set_size))
                        print(set_size)

                        filtered_log_path = os.path.join(current_app.instance_path,
                                                         'logs') + "/" + usr + "_" + log.filename.replace('.jsonocel',
                                                                                                          '') + "_" + "filtered" + ".jsonocel"
                        original_df, original_obj_df = ocel_importer.apply(filtered_log_path)
                        # PREPARE DATASET FOR FREQ_ITEMS ALG
                        print("Original DF")
                        print(original_df)
                        dataset = []
                        print('\n')
                        print("Selected Attrs")
                        print(sel_freq_attrs.keys())
                        for x in original_df.index: #iter evetns
                            event = original_df.loc[x]
                            itemset = []
                            print('Checking event: ' + event.event_id)
                            for type in sel_freq_attrs.keys(): #iter obj types
                                # print(list(original_df.columns))
                                print('Checking type: ' + type)
                                objs_of_type_for_event = event[type]
                                for obj in objs_of_type_for_event: #iter objects of the selected type
                                    print("Checking Obj: " + str(obj))
                                    # print(obj)
                                    # search in df by 'object_id'
                                    obj_row = original_obj_df.loc[original_obj_df['object_id'] == obj]
                                    print(obj_row)
                                    # print(obj_row)
                                    for attr in sel_freq_attrs[type]: #iter attrs of the selected type
                                        print("Adding OBJ Attr: " + attr)
                                        print(obj_row[attr].item())
                                        print('\n')
                                        itemset.append(str(obj_row[attr].item()))
                            dataset.append(itemset)
                        # print(dataset)
                        # GENERATING FREQ ITEMSSETS
                        te = TransactionEncoder()
                        te_ary = te.fit(dataset).transform(dataset)
                        df = pd.DataFrame(te_ary, columns=te.columns_)
                        print("Input DF")
                        print(df)
                        frequent_itemsets = None
                        if freq_set_alg == "apriori":
                            frequent_itemsets = apriori(df, min_support=min_supp, use_colnames=True)
                        elif freq_set_alg == "fpmax":
                            frequent_itemsets = fpmax(df, min_support=min_supp, use_colnames=True)
                        elif freq_set_alg == "fpgrowth":
                            frequent_itemsets = fpgrowth(df, min_support=min_supp, use_colnames=True)
                        else:
                            print("Wrong algorithm")

                        print("MlXtend Out")
                        print(frequent_itemsets)


                        # trasform set to list and filter out only sets with given size
                        out = {'data': []}
                        for itemSetIndex in frequent_itemsets.index:
                            row = frequent_itemsets.loc[itemSetIndex]
                            if len(row['itemsets']) >= set_size:
                                listMappedObjs = []
                                for obj in row['itemsets']:
                                    listMappedObjs.append(obj)
                                out['data'].append([len(listMappedObjs), listMappedObjs, round(row['support'], 2)])

                        print("Flask out: ")
                        print(out)

                        return jsonify(result={'freq_itemsets': out['data'],
                                               # 'assoc_rules': assoc_rules_out
                                               })


def isfloat(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b

