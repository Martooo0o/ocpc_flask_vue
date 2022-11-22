import pandas as pd
from .create_event_dimensions import create_event_dimensions
from .create_object_event_dimensions import create_object_event_dimensions
from app.helper.create_objects_differentots_dimensions import create_objects_differentots_dimensions
import numpy as np
exitstance = {}
all = {}

#dimens is a dict with keys objTypes and values the attr for this type
def calcFreqCube(event_df, obj_df, dimens):
    # ocel
    testDict = {'Existence':{},
                'All': {}}

    # event_df, obj_df = ocel_importer.apply("instance/logs/filteredOCEL" + index + ".jsonocel")
    # counts_dict = {}
    for x in dimens.keys():
        for attr1 in dimens[x]:
            for y in dimens.keys():
                for attr2 in dimens[y]:
                    if not attr1 + "," + attr2 in testDict['All'].keys() and not attr2 + "," + attr1 in testDict['All'].keys():
                        if x == 'Events':
                            data1 = event_df
                            attr1 = "event_" + attr1
                        else:
                            data1 = obj_df

                        if y == "Events":
                            data2 = event_df
                            attr2 = "event_" + attr2
                        else:
                            data2 = obj_df

                        valuesAttr1 = data1[attr1].dropna().tolist()
                        # valuesAttr1 = [x for x in valuesAttr1 if not pd.isna(x)]
                        valuesAttr2 = data2[attr2].dropna().tolist()
                        # valuesAttr2 = [y for y in valuesAttr2 if not pd.isna(y)]

                        pairDataAll =  {}
                        pairDataExistance = {}
                        counts = {}
                        # countsE = pd.DataFrame()
                        # countsAll = pd.DataFrame()
                        # TODO eventually also just add cases when one dimension is nothing
                        if x == 'Events' and y == 'Events':
                            counts = create_event_dimensions([attr1, attr2], event_df)

                        elif x == 'Events' and y != 'Events':
                            counts = create_object_event_dimensions(y, attr2, attr1, event_df, obj_df)

                        elif x != 'Events' and y == 'Events':
                            counts = create_object_event_dimensions(x, attr1, attr2, event_df, obj_df)

                        elif x != 'Events' and y != 'Events':
                            counts = create_objects_differentots_dimensions(x, attr1, y, attr2, event_df, obj_df)


                        countsE = counts.finaldf
                        if x == 'Events' and y == 'Events':
                            countsAll = counts.finaldf
                        else:
                            countsAll = counts.finaldfall

                        # if x == 'Events' or y == 'Events':
                        #     countsE = countsE.T
                        #     countsAll = countsAll.T

                        # Map Dataframe to dict because this representation is bs
                        for val1 in valuesAttr1:
                            for val2 in valuesAttr2:
                                if str(val2) + ',' + str(val1) in pairDataExistance.keys():
                                    pairDataExistance[str(val1) + ',' + str(val2)] = pairDataExistance[str(val2) + ',' + str(val1) ]
                                    pairDataAll[str(val1) + ',' + str(val2)] = pairDataAll[str(val2) + ',' + str(val1)]
                                    # print("Time Saved")
                                    continue

                                # print("Looking at " + str(val1) + str(val2))
                                if x == y and x == "Events":

                                    # print(countsE.columns[1])
                                    # print(type(countsE.columns[1]))
                                    temp_val1 = str(val1) if isinstance(countsE.columns[1], str) else val1

                                    # print(countsE.loc[1][countsE.columns[0]])
                                    # print(type(countsE.loc[1][countsE.columns[0]]))
                                    temp_val2 = str(val2) if isinstance(countsE.loc[1][countsE.columns[0]], str) else val2
                                    temp_val1 = np.float64(temp_val1) if isinstance(countsE.columns[1],
                                                                                    (np.float64, float)) else temp_val1
                                    temp_val2 = np.float64(temp_val2) if isinstance(countsE.loc[0][countsE.columns[0]],
                                                                                    (np.float64, float)) else temp_val2

                                    # if x == "Events" or y == "Events":
                                    if not temp_val1 in countsE.columns:
                                        # print("Swaping vars")
                                        temp = temp_val1
                                        temp_val1 = temp_val2
                                        temp_val2 = temp

                                    if isinstance(countsE.loc[0][countsE.columns[0]], (np.float64, float)) and isinstance(countsE.columns[1], (np.float64, float)):
                                        selectedCols = [True if isinstance(x, (np.float64, float)) and abs(
                                            x - temp_val1) < 1e-10 else False for x in countsE.columns]
                                        eVal = \
                                            countsE.loc[ abs(countsE[countsE.columns[0]] - temp_val2) < 1e-10, selectedCols].tolist()[0]

                                        # print(countsAll)
                                        allVal = \
                                            countsAll.loc[abs(countsE[countsE.columns[0]] - temp_val2) < 1e-10, selectedCols].tolist()[0]
                                    elif not isinstance(countsE.loc[0][countsE.columns[0]], (np.float64, float)) and isinstance(
                                            countsE.columns[1], (np.float64, float)):
                                        selectedCols = [True if isinstance(x, (np.float64, float)) and abs(
                                            x - temp_val1) < 1e-10 else False for x in countsE.columns]
                                        eVal = \
                                        countsE.loc[countsE[countsE.columns[0]] == temp_val2, selectedCols].tolist()[0]

                                        # print(countsAll)
                                        allVal = \
                                        countsAll.loc[countsAll[countsAll.columns[0]] == temp_val2, selectedCols].tolist()[
                                            0]
                                    elif isinstance(countsE.loc[0][countsE.columns[0]], (np.float64, float)) and not isinstance(
                                            countsE.columns[1], (np.float64, float)):
                                        eVal = countsE.loc[abs(countsAll[countsAll.columns[0]] - temp_val2) < 1e-10, temp_val1].tolist()[0]

                                        # print(countsAll)
                                        allVal = countsAll.loc[abs(countsAll[countsAll.columns[0]] - temp_val2) < 1e-10, temp_val1].tolist()[0]
                                    else:
                                        # print()
                                        eVal = countsE.loc[countsE[countsE.columns[0]] == temp_val2, temp_val1].tolist()[0]

                                        # print(countsAll)
                                        allVal = countsAll.loc[countsAll[countsAll.columns[0]] == temp_val2, temp_val1].tolist()[0]
                                    pairDataExistance[temp_val1 + ',' + temp_val2] = eVal
                                    pairDataAll[temp_val1 + ',' + temp_val2] = allVal
                                else:
                                    # print("First Var")
                                    # print(countsE.columns[1])
                                    # print(type(countsE.columns[1]))
                                    temp_val1 = str(val1) if isinstance(countsE.columns[0], str) else val1

                                    # print("Second Var")
                                    # print(countsE[""][0])
                                    # print(type(countsE[""][0]))

                                    temp_val2 = str(val2) if isinstance(countsE[""][0], str) else val2
                                    # # print(countsE[""])
                                    # # print(countsE[""][1])

                                    # # print(isinstance(countsE[""][1], np.float64))
                                    temp1vals = [str(x) for x in countsE.columns]
                                    temp2vals = [str(x) for x in countsE[""]]
                                    # print(temp2vals)
                                    # if x == "Events" or y == "Events":
                                    if not str(temp_val1) in temp1vals or not str(temp_val2) in temp2vals:
                                        # print("Swaping vars")
                                        temp = temp_val1
                                        temp_val1 = temp_val2
                                        temp_val2 = temp
                                        temp_x = y
                                        temp_y = x
                                    else:
                                        pass
                                        # print("Not Spawwing")
                                        # print(temp_val1)
                                        # print(countsE.columns)

                                    temp_val1 = np.float64(temp_val1) if isinstance(countsE.columns[1],
                                                                                    (np.float64, float)) else temp_val1
                                    temp_val2 = np.float64(temp_val2) if isinstance(countsE[""][1], (np.float64, float)) else temp_val2


                                    if isinstance(countsE[""][1], (np.float64, float)) and isinstance(countsE.columns[1], (np.float64, float)):
                                        # print(countsE)
                                        selectedCols = [True if isinstance(z, (np.float64, float)) and abs(
                                            z - temp_val1) < 1e-10 else False for z in countsE.columns]
                                        # print(selectedCols)
                                        eVal = countsE.loc[abs(countsE[""]-temp_val2) < 1e-10, selectedCols]
                                        # print(eVal)
                                        # print(eVal.index[0])
                                        eVal = eVal.loc[eVal.index[0]].tolist()[0]
                                        # print(eVal)
                                        # print(pairDataExistance)
                                        pairDataExistance[str(temp_val1) + ',' + str(temp_val2)] = eVal
                                        allVal = countsAll.loc[abs(countsAll[""] - temp_val2) < 1e-10, temp_val1].tolist()[0]
                                        pairDataAll[str(temp_val1) + ',' + str(temp_val2)] = allVal
                                    elif not isinstance(countsE[""][1], (np.float64,float) ) and isinstance(countsE.columns[1], (np.float64, float)):

                                        # print("First Float, seond not")
                                        selectedCols = [True if isinstance(z, (np.float64, float)) and abs(
                                            z - temp_val1) < 1e-10 else False for z in countsE.columns]
                                        # print(selectedCols)
                                        eVal = countsE.loc[countsE[""] == temp_val2, selectedCols]
                                        # print(eVal)
                                        eVal = eVal.loc[eVal.index[0]].tolist()[0]
                                        pairDataExistance[str(temp_val1) + ',' + str(temp_val2)] = str(eVal)
                                        allVal = \
                                        countsAll.loc[countsAll[""] == temp_val2, selectedCols]
                                        allVal = allVal.loc[allVal.index[0]].tolist()[0]
                                        pairDataAll[str(temp_val1) + ',' + str(temp_val2)] = allVal
                                    elif isinstance(countsE[""][1], (np.float64, float)) and not isinstance(countsE.columns[1], (np.float64, float)):
                                        # print("First string, seond float")
                                        eVal = countsE.loc[abs(countsE[""] - temp_val2) < 1e-10, temp_val1].tolist()[0]
                                        pairDataExistance[str(temp_val1) + ',' + str(temp_val2)] = int(eVal)
                                        allVal = \
                                        countsAll.loc[abs(countsE[""] - temp_val2) < 1e-10, temp_val1].tolist()[0]
                                        pairDataAll[str(temp_val1) + ',' + str(temp_val2)] = allVal
                                    else:
                                        eVal = countsE.loc[countsE[""] == temp_val2, temp_val1].tolist()[0]
                                        pairDataExistance[temp_val1 + ',' + temp_val2] = str(eVal)
                                        allVal = countsAll.loc[countsAll[""] == temp_val2  , temp_val1].tolist()[0]
                                        pairDataAll[temp_val1+','+temp_val2] = allVal

                        if x == 'Events':
                            attr1 = attr1[6:]

                        if y ==  "Events":
                            attr2 = attr2[6:]

                        testDict['All'][attr1 + "," + attr2] = pairDataAll
                        testDict['Existence'][attr1 + "," + attr2] = pairDataExistance
                    else:
                        pass
                        # print('Time Saved attrs')
    return testDict

def calcEventEventAttrPairs(events, eventDimens):
   for x in eventDimens.keys():
       for y in eventDimens.keys():
           if x+","+y in exitstance.keys() or y+","+x in exitstance.keys():
               break
           xYPairInfo = {}
           xYPairInfo[x+'_values'] = [events.loc[i][x] for i in events.index]
           if not x == y:
               xYPairInfo[y + '_values'] = [events.loc[i][y] for i in events.index]
           xYPairInfo['value_pair_occur'] = {}


def calcEventObjAttrPairs(events, objects):
    pass

def calcObjObjAttrPairs(events, objects):
    pass

