from enum import Enum
from pm4py.util import exec_utils, constants
from pm4py.objects.ocel.util import filtering_utils
from copy import copy
from typing import Dict, Any, Optional, Collection
from pm4py.objects.ocel.obj import OCEL


class Parameters(Enum):
    ATTRIBUTE_KEY = constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY
    POSITIVE = "positive"

def filter_ocel_object_attribute(ocel: OCEL, attribute_key: str, attribute_values: Collection[Any], positive: bool = True) -> OCEL:
    """
    Filters the object-centric event log on the provided object attributes values
    Parameters
    ----------------
    ocel
        Object-centric event log
    attribute_key
        Attribute at the event level
    attribute_values
        Attribute values
    positive
        Decides if the values should be kept (positive=True) or removed (positive=False)
    Returns
    ----------------
    filtered_ocel
        Filtered object-centric event log
    """
    from pm4py.algo.filtering.ocel import object_attributes

    return apply_filter(ocel, attribute_values, parameters={object_attributes.Parameters.ATTRIBUTE_KEY: attribute_key, object_attributes.Parameters.POSITIVE: positive})

def apply_filter(ocel: OCEL, values: Collection[Any], parameters: Optional[Dict[Any, Any]] = None) -> OCEL:
    """
    Filters the object-centric event log on the provided object attributes values
    Parameters
    ----------------
    ocel
        Object-centric event log
    values
        Collection of values
    parameters
        Parameters of the algorithm, including:
        - Parameters.ATTRIBUTE_KEY => the attribute that should be filtered
        - Parameters.POSITIVE => decides if the values should be kept (positive=True) or removed (positive=False)
    Returns
    ----------------
    ocel
        Filtered object-centric event log
    """
    if parameters is None:
        parameters = {}

    attribute_key = exec_utils.get_param_value(Parameters.ATTRIBUTE_KEY, parameters, ocel.object_type_column)
    positive = exec_utils.get_param_value(Parameters.POSITIVE, parameters, True)

    ocel = copy(ocel)
    if positive:
        ocel.objects = ocel.objects[ocel.objects[attribute_key].isin(values)]
    else:
        ocel.objects = ocel.objects[~ocel.objects[attribute_key].isin(values)]

    return filtering_utils.propagate_object_filtering(ocel, parameters=parameters)

def filterNonTrivialAttrs(materialisation, attr):
    pass

def prepDataForFreqSetMining(ocel):
    # esentially what I already did in JS but for the filtered ocel
    pass

