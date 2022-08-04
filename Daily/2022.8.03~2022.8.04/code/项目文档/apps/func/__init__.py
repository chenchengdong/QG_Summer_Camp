import json
from flask import Flask, request, jsonify, Blueprint
import sys
sys.path.append("..")
from apps import model

func_bp = Blueprint('func_bp', __name__)

@func_bp.route('/user=<user>/main')
def func_main(user):
    return json.dumps({"hot_book": model.hot_book(), "like_book": model.like_book(model.de_stry(user))})

@func_bp.route('/user=<user>/find=<message>')
def c_find(user, message):
    return json.dumps(model.find(message))

@func_bp.route('/user=<user>/kind=<kind>')
def c_kind(user, kind):
    return jsonify(model.kind(kind))


@func_bp.route('/user=<user>/sort=<sort>')
def c_sort(user, sort):
    return json.dumps(model.ranking(sort))