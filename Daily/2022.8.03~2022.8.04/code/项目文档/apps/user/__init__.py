from flask import Flask, request, jsonify, Blueprint
import json
import sys
sys.path.append("..")
from apps import model

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/registered', methods=['POST', "GET"])
def c_registered():
    register_data = json.loads(request.get_data(as_text=True))
    sin = model.register(register_data)
    print(sin)
    print(type(sin))
    return str(sin)

@user_bp.route('/login', methods=['POST', "GET"])
def c_login():
    # login_data = json.loads(request.get_data(as_text=True))
    print('开始登录')
    login_data = request.form.to_dict()
    """
    print(xxxx)
    print(type(xxxx))
    login_data = json.loads(xxxx)
    print(type(login_data))
    """
    print(type(login_data))
    sin = model.login(login_data)
    print(sin)
    return jsonify(sin)

@user_bp.route('/change_password', methods=["POST", "GET"])
def c_change_password():
    change_data = json.loads(request.get_data(as_text=True))
    sin = model.change_password(change_data)
    return jsonify(sin)

