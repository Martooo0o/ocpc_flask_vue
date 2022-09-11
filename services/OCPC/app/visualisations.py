from flask import send_file, Blueprint, make_response, redirect, url_for, request, jsonify
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
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

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth
from mlxtend.frequent_patterns import association_rules
import pandas as pd
from .helper.cubeUtils import calcFreqCube

visualisations = Blueprint('visualisations', __name__, url_prefix="/visualisations")
CORS(visualisations, supports_credentials=True)

# example code
@visualisations.after_request
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

@visualisations.route('/log', methods=['POST'])
@jwt_required()
def get_flattened_log():
    #needed is the analysis,
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    data = json.loads(request.get_data())
    print(data)
    # name = data.get('name')
    analysis_name = data.get('analysisname')
    print(analysis_name)

    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                for analysis in cube.analyses:
                    if analysis.name == escape(analysis_name):
                        filtered_log_path = os.path.join(current_app.instance_path,
                                                         'logs') + "/" + usr + "_" + log.filename.replace('.jsonocel',
                                                                                                  '') + "_" + "filtered" + ".jsonocel"
                        event_df, obj_df = ocel_importer.apply(filtered_log_path)
                        print(event_df)
                        js = event_df.to_json(orient='columns')
                        print(js)
                        return jsonify({'result': "OCEL was flattened",
                                        'data': js}), 200
        print('error: Analysis not found')
        return jsonify({
            'error': "Analysis not found"
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@visualisations.route('/dfg', methods=['POST'])
@jwt_required()
def get_dfg():
    # Auth
    jwt_data = verify_jwt_in_request()
    print(jwt_data)

    usr = get_jwt_identity()
    print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    # ARGS
    data = json.loads(request.get_data())
    print(data)
    analysis_name = data.get('analysisname', "")
    print("Analysis Name: " + analysis_name)

    vis_index = data.get('vis_index')
    print('Vis Index')
    print(vis_index)
    print(type(vis_index))

    # type = data.get('type')
    # if not type:
    #     type = 'Frequency'
    #
    perf_agr_measure = data.get('performace_measure')
    if not perf_agr_measure:
        perf_agr_measure = 'median'

    #THE GOOD STUFF
    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                for analysis in cube.analyses:
                    if analysis.name == escape(analysis_name):
                        filtered_log_path = os.path.join(current_app.instance_path,
                                                         'logs') + "/" + usr + "_" + log.filename.replace('.jsonocel',
                                                                                                          '') + "_" + "filtered" + ".jsonocel"
                        ocel = pm4py.read_ocel(filtered_log_path)

                        ocdfg = None
                        try:
                            ocdfg = pm4py.discover_ocdfg(ocel)
                        except:
                            return {'error': 'Could not discover a DFG'}

                        import random
                        seed = random.randrange(100000)
                        dfg_file_path = os.path.join(current_app.instance_path,
                                                         'dfgs') + '/' + 'dfg' + '_' + usr + '_' + analysis.name + '_'+ str(seed) + '.svg'
                        if ocdfg:
                            edge_threshold = int(json.loads(analysis.visualisations)[vis_index]['edge_threshold'])
                            act_threshold = int(json.loads(analysis.visualisations)[vis_index]['act_threshold'])
                            dfg_type = json.loads(analysis.visualisations)[vis_index]['dfg_type']

                            if dfg_type == 'Frequency':
                                pm4py.save_vis_ocdfg(ocdfg, file_path=dfg_file_path, annotation='frequency',
                                                     edge_threshold=edge_threshold, act_threshold=act_threshold)
                            elif dfg_type == 'Performance':
                                pm4py.save_vis_ocdfg(ocdfg, file_path=dfg_file_path, annotation='performance',
                                                     edge_threshold=edge_threshold, performance_aggregation=perf_agr_measure,
                                                     act_threshold=act_threshold)
                            else:
                                return {'error': 'No DFG was created. DFG type is missing!'}
                            # visualizer.save(gviz, 'instance/dfgs/dfg'+index+'.svg')

                            return {'result': "DFG generated",
                                    'data': request.base_url + '/get_svg/' + usr + '/' + analysis.name + '_' + str(seed)}
                            # return send_file(dfg_file_path, as_attachment=False, cache_timeout=0)
                        else:
                            return {'error': 'No DFG was created'}
        print('error: Analysis not found')
        return jsonify({
            'error': "Analysis not found, so DFG could not be generated"
        }), 200
    else:
        return jsonify(message="Unauthorized no user found"), 401

@visualisations.route('/dfg/get_svg/<usr>/<analysis>')
def getDFGSVG(usr, analysis):

    # dfg_name = 'freqItemsDfg' + str(index) + '.svg'
    # print(dfg_name)
    dfg_file_path = os.path.join(current_app.instance_path,
                                 'dfgs') + '/' + 'dfg' + '_' + usr + '_' + analysis + '.svg'
    return send_file(dfg_file_path, as_attachment=False, cache_timeout=0)

@visualisations.route('/freq_itemsets', methods=['POST'])
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
    print("Analysis Name: " + analysis_name)

        # sel_freq_attrs is an object with keys logObjType (like items, customers) and values list of seleted attrs for this obj type
        # EX:
        # sel_freq_attrs = {'customers': ['bla', 'bla2'],
        #                   'items' ['mur', 'mur2']}
    # sel_freq_attrs = data.get('freq_attrs')

    vis_index = data.get('index')

    # min_supp = float(data.get('min_supp') if data.get('min_supp') else 0.01)
    # min_conf = float(data.get('min_conf') if data.get('min_conf') else 1) / 100
    # min_lift = float(data.get('min_lift') if data.get('min_lift') else 1) / 100
    # set_size = int(data.get('set_size') if data.get('set_size') else 0)

    freq_set_alg = data.get('freq_set_alg') if data.get('freq_set_alg') else 'apriori'

    #THE GOOD STUFF
    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                for analysis in cube.analyses:
                    if analysis.name == escape(analysis_name):
                        sel_freq_attrs = json.loads(analysis.visualisations)[vis_index]['attrs']
                        min_supp = float(json.loads(analysis.visualisations)[vis_index]['min_supp'])
                        set_size = int(json.loads(analysis.visualisations)[vis_index]['set_size'])

                        print("Attrs: " + str(sel_freq_attrs))
                        print(sel_freq_attrs)
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

                        # if frequent_itemsets:

                        # assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_conf)
                        # assoc_rules_out = []
                        # for i in assoc_rules.index:
                        #     row_out = []
                        #     row = assoc_rules.loc[i]
                        #     row_out.append(list(row['antecedents']))
                        #     row_out.append(list(row['consequents']))
                        #     row_out.append(row['support'])
                        #     row_out.append(row['confidence'])
                        #     row_out.append(row['lift'])
                        #     assoc_rules_out.append(row_out)
                        #
                        # print("Association rules")
                        # print(assoc_rules_out)

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

@visualisations.route('/assoc_rules', methods=['POST'])
@jwt_required()
def get_assoc_rules():
    # Auth
    jwt_data = verify_jwt_in_request()
    # print(jwt_data)

    usr = get_jwt_identity()
    # print("JWT identity: " + usr)
    usr_obj = User.query.filter_by(email=usr).first()

    # ARGS
    data = json.loads(request.get_data())
    analysis_name = data.get('analysisname')
    # print("Analysis Name: " + analysis_name)

        # sel_freq_attrs is an object with keys logObjType (like items, customers) and values list of seleted attrs for this obj type
        # EX:
        # sel_freq_attrs = {'customers': ['bla', 'bla2'],
        #                   'items' ['mur', 'mur2']}
    # sel_freq_attrs = data.get('freq_attrs')

    vis_index = data.get('index')

    min_supp = float(data.get('min_supp') if data.get('min_supp') else 0.01)
    min_conf = float(data.get('min_conf') if data.get('min_conf') else 1) / 100
    min_lift = float(data.get('min_lift') if data.get('min_lift') else 1) / 100
    set_size = int(data.get('set_size') if data.get('set_size') else 0)

    freq_set_alg = data.get('freq_set_alg') if data.get('freq_set_alg') else 'apriori'

    #THE GOOD STUFF
    if usr_obj:
        for log in usr_obj.logs:
            for cube in log.cubes:
                for analysis in cube.analyses:
                    if analysis.name == escape(analysis_name):
                        sel_freq_attrs = json.loads(analysis.visualisations)[vis_index]['attrs']
                        min_supp = float(json.loads(analysis.visualisations)[vis_index]['min_supp'])
                        set_size = int(json.loads(analysis.visualisations)[vis_index]['set_size'])
                        min_conf = float(json.loads(analysis.visualisations)[vis_index]['min_conf'])
                        min_lift = float(json.loads(analysis.visualisations)[vis_index]['min_lift'])

                        # print("Attrs: " + str(sel_freq_attrs))
                        # print(sel_freq_attrs)
                        filtered_log_path = os.path.join(current_app.instance_path,
                                                         'logs') + "/" + usr + "_" + log.filename.replace('.jsonocel',
                                                                                                          '') + "_" + "filtered" + ".jsonocel"
                        original_df, original_obj_df = ocel_importer.apply(filtered_log_path)
                        # PREPARE DATASET FOR FREQ_ITEMS ALG
                        # print("Original DF")
                        # print(original_df)
                        dataset = []
                        # print('\n')
                        # print("Selected Attrs")
                        # print(sel_freq_attrs.keys())
                        for x in original_df.index: #iter evetns
                            event = original_df.loc[x]
                            itemset = []
                            # print('Checking event: ' + event.event_id)
                            for type in sel_freq_attrs.keys(): #iter obj types
                                # print(list(original_df.columns))
                                print('Checking type: ' + type)
                                objs_of_type_for_event = event[type]
                                for obj in objs_of_type_for_event: #iter objects of the selected type
                                    print("Checking Obj: " + str(obj))
                                    # print(obj)
                                    # search in df by 'object_id'
                                    obj_row = original_obj_df.loc[original_obj_df['object_id'] == obj]
                                    # print(obj_row)
                                    # print(obj_row)
                                    for attr in sel_freq_attrs[type]: #iter attrs of the selected type
                                        # print("Adding OBJ Attr: " + attr)
                                        # print(obj_row[attr].item())
                                        # print('\n')
                                        itemset.append(str(obj_row[attr].item()))
                            dataset.append(itemset)
                        # print(dataset)
                        # GENERATING FREQ ITEMSSETS
                        te = TransactionEncoder()
                        te_ary = te.fit(dataset).transform(dataset)
                        df = pd.DataFrame(te_ary, columns=te.columns_)
                        # print("Input DF")
                        # print(df)
                        frequent_itemsets = None
                        if freq_set_alg == "apriori":
                            frequent_itemsets = apriori(df, min_support=min_supp, use_colnames=True)
                        elif freq_set_alg == "fpmax":
                            frequent_itemsets = fpmax(df, min_support=min_supp, use_colnames=True)
                        elif freq_set_alg == "fpgrowth":
                            frequent_itemsets = fpgrowth(df, min_support=min_supp, use_colnames=True)
                        else:
                            print("Wrong algorithm")

                        # print("MlXtend Out")
                        # print(frequent_itemsets)

                        if len(frequent_itemsets.index) > 0 :
                            assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_conf)
                            assoc_rules_out = []
                            for i in assoc_rules.index:
                                row = assoc_rules.loc[i]
                                if len(list(row['antecedents'])) + len(list(row['consequents'])) >= set_size:
                                    row_out = []
                                    row_out.append(len(list(row['antecedents'])) + len(list(row['antecedents'])))
                                    row_out.append(list(row['antecedents']))
                                    row_out.append(list(row['consequents']))
                                    row_out.append(round(row['support'], 2))
                                    row_out.append(round(row['confidence'], 2))
                                    row_out.append(round(row['lift'], 2))
                                    assoc_rules_out.append(row_out)
                        else:
                            return jsonify(result={'assoc_rules': {'data': []},
                                                   # 'assoc_rules': assoc_rules_out
                                                   })
                        # print("Association rules")
                        # print(assoc_rules_out)

                        # trasform set to list and filter out only sets with given size
                        out = {'data': assoc_rules_out}
                        # for itemSetIndex in frequent_itemsets.index:
                        #     row = frequent_itemsets.loc[itemSetIndex]
                        #     if len(row['itemsets']) >= set_size:
                        #         listMappedObjs = []
                        #         for obj in row['itemsets']:
                        #             listMappedObjs.append(obj)
                        #         out['data'].append([len(listMappedObjs), listMappedObjs, round(row['support'], 2)])

                        # print("Flask out: ")
                        # print(out)

                        return jsonify(result={'assoc_rules': out['data'],
                                               # 'assoc_rules': assoc_rules_out
                                               })