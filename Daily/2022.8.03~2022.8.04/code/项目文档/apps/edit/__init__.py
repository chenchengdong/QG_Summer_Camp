import json
from flask import Flask, request, jsonify, Blueprint
import datetime
import sys
sys.path.append('..')
from apps import model

edit_bp = Blueprint("edit_bp", __name__)

@edit_bp.route('/user=<user>/edit/logout')
def c_logout(user):
    print(type(user))
    print(user)
    user_name = model.de_ctry(user)
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logout_data = tuple((user_name, time_now, 'logout'))
    print(type(logout_data))
    model.logout(logout_data)
    return jsonify({'LOGOUT SUCCESS'})


@edit_bp.route('/user=<user>/edit/password', methods=['POST'])
def c_change_password(user):
    way = json.loads(request.get_data(as_text=True))
    sin = model.change_password(way)
    return jsonify(sin)


@edit_bp.route('/user=<user>/edit/intro=<intro>')
def c_signature_edit(user, intro):
    model.signature_edit(intro, user)


@edit_bp.route('/user=<user>/edit/newurl', methods=['POST'])
def c_update_user_url(user):
    newurl = json.loads(request.get_data(as_text=True))
    user = model.de_ctry(user)
    url = tuple((newurl['user_url'], user))
    model.update_user_url(url)








