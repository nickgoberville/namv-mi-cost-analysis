from argparse import Namespace
from loguru import logger
import json
import pathlib

def to_namespace(in_dict):
    in_dict_copy = in_dict.copy()
    for key, val in in_dict_copy.items():
        if type(val) == dict:
            in_dict_copy[key] = to_namespace(in_dict_copy[key])
    out = Namespace(**in_dict_copy)
    return out

def to_dict(in_namespace):
    in_namespace_dict = in_namespace.__dict__.copy()
    for key, val in in_namespace_dict.items():
        if type(val) == Namespace:
            in_namespace_dict[key] = to_dict(val)
    return in_namespace_dict

def read_json(filename, use_namespace=False):
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        logger.error("(didn't find {})".format(filename))
        #print("(didn't find {}.json)".format(filename))

    if use_namespace: data = to_namespace(data)

    return data

def write_json(filename, dict_to_save):
    pathlib.Path(filename).touch()
    with open(filename, "w") as f:
        f.write(json.dumps(dict_to_save, indent=4))
    logger.success("saved values to {}!".format(filename))


